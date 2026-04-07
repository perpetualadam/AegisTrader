"""
Semantic UI reading: anchor labels + layout regions + multi-pass OCR merge.

Turns raw OCR boxes into fields (last, bid, ask, OHLC, etc.) with ambiguity notes.
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

from vision.ocr_reader import OCRReader, OCRResult, PreprocessMode, PriceData
from vision.ui_layout import UILayout, load_ui_layout

logger = logging.getLogger(__name__)

try:
    from config import OCR_FULL_PANEL, OCR_MULTI_PASS, OCR_PREPROCESS_MODE
except ImportError:
    OCR_FULL_PANEL = True
    OCR_MULTI_PASS = False
    OCR_PREPROCESS_MODE = "standard"


@dataclass
class UISemanticReading:
    """Structured interpretation of on-screen trading UI."""

    last_price: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    volume: Optional[float] = None
    change_percent: Optional[float] = None
    change_value: Optional[float] = None
    timestamp: float = 0.0
    raw_labels: Dict[str, str] = field(default_factory=dict)
    ambiguity_notes: List[str] = field(default_factory=list)
    ocr_passes_used: List[str] = field(default_factory=list)

    def to_price_data(self) -> PriceData:
        """Convert to PriceData for strategy/scoring."""
        return PriceData(
            current_price=self.last_price,
            high_price=self.high_price,
            low_price=self.low_price,
            open_price=self.open_price,
            close_price=self.close_price,
            volume=self.volume,
            change_percent=self.change_percent,
            change_value=self.change_value,
            timestamp=self.timestamp or time.time(),
        )


def _iou(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    aa = (ax2 - ax1) * (ay2 - ay1)
    ba = (bx2 - bx1) * (by2 - by1)
    union = aa + ba - inter
    return inter / union if union > 0 else 0.0


def merge_ocr_results(
    batches: List[List[OCRResult]], iou_threshold: float = 0.45
) -> List[OCRResult]:
    """Merge duplicate detections across passes; keep highest confidence."""
    if not batches:
        return []
    pool: List[OCRResult] = []
    for batch in batches:
        pool.extend(batch)
    kept: List[OCRResult] = []
    for r in sorted(pool, key=lambda x: -x.confidence):
        dup = False
        for k in kept:
            if r.text.strip().lower() == k.text.strip().lower() and _iou(r.bbox, k.bbox) > iou_threshold:
                dup = True
                break
        if not dup:
            kept.append(r)
    return kept


def _num_from_text(text: str) -> List[float]:
    out: List[float] = []
    for m in re.finditer(r"[\+\-]?[\d,]+\.?\d*", text.replace(" ", "")):
        s = m.group().replace(",", "")
        try:
            if re.match(r"^[\+\-]?\d+\.?\d*$", s):
                out.append(float(s))
        except ValueError:
            continue
    return out


def _best_price_from_line(line: str) -> Optional[float]:
    nums = _num_from_text(line)
    if not nums:
        return None
    # Prefer decimal prices over integers when ambiguous
    for n in nums:
        if abs(n) > 1e-6:
            return n
    return nums[0]


class SemanticReader:
    """
    Full-panel + regional OCR with label anchoring.

    Uses OCR_PREPROCESS_MODE + optional OCR_MULTI_PASS from config.
    """

    def __init__(self, ocr: OCRReader, layout: Optional[UILayout] = None):
        self.ocr = ocr
        self.layout = layout or load_ui_layout()

    def read_screen(self, image: np.ndarray) -> UISemanticReading:
        h, w = image.shape[:2]
        reading = UISemanticReading(timestamp=time.time())
        passes: List[str] = []
        batches: List[List[OCRResult]] = []

        if OCR_MULTI_PASS:
            for mode in (PreprocessMode.STANDARD, PreprocessMode.DARK_UI):
                batches.append(
                    self.ocr.extract_text(
                        image,
                        region=None,
                        full_text=OCR_FULL_PANEL,
                        preprocess_mode=mode,
                    )
                )
                passes.append(str(mode))
        else:
            try:
                pm = PreprocessMode(OCR_PREPROCESS_MODE.lower())
            except ValueError:
                pm = PreprocessMode.STANDARD
            batches.append(
                self.ocr.extract_text(
                    image,
                    region=None,
                    full_text=OCR_FULL_PANEL,
                    preprocess_mode=pm,
                )
            )
            passes.append(str(pm))

        merged = merge_ocr_results(batches)
        reading.ocr_passes_used = passes

        # Regional OCR for semantic hints
        regional: Dict[str, List[OCRResult]] = {}
        for name, box in self.layout.all_pixel_regions(w, h):
            if name == "full_panel":
                continue
            try:
                pm = PreprocessMode(OCR_PREPROCESS_MODE.lower())
            except ValueError:
                pm = PreprocessMode.STANDARD
            regional[name] = self.ocr.extract_text(
                image,
                region=box,
                full_text=True,
                preprocess_mode=pm,
            )

        _apply_anchor_semantics(merged, regional, self.layout, reading)
        _fill_from_regions(regional, reading)

        if reading.last_price is None and merged:
            prices = [r for r in merged if r.data_type == "price" and r.value is not None]
            if prices:
                prices.sort(key=lambda x: x.confidence, reverse=True)
                reading.last_price = prices[0].value
                reading.raw_labels.setdefault("fallback_current", prices[0].text)
                reading.ambiguity_notes.append(
                    "last_price inferred from highest-confidence price token (no anchor)"
                )

        return reading


def _anchor_in_text(text_lower: str, anchor: str) -> bool:
    """Match anchor with word boundaries for single tokens; substring for phrases."""
    a = anchor.strip().lower()
    if not a:
        return False
    if " " in a:
        return a in text_lower
    if ":" in a:
        return a in text_lower
    return re.search(r"\b%s\b" % re.escape(a), text_lower) is not None


def _apply_anchor_semantics(
    full: List[OCRResult],
    regional: Dict[str, List[OCRResult]],
    layout: UILayout,
    out: UISemanticReading,
) -> None:
    """Match labels like Last/Bid/Ask/OHLC to nearby numbers."""
    anchors_map: Dict[str, Tuple[str, List[str]]] = {}
    for field, cfg in layout.semantic_hints.items():
        reg = cfg.get("region", "full_panel")
        anchors = [a.lower() for a in cfg.get("anchors", [])]
        anchors_map[field] = (reg, anchors)

    combined_lines = _cluster_lines(full + [r for rs in regional.values() for r in rs])

    for field, (reg_name, anchors) in anchors_map.items():
        pool = list(full) if reg_name == "full_panel" else regional.get(reg_name, [])
        if not pool:
            continue
        line_texts = _cluster_lines(pool)
        for lt in line_texts:
            low = lt.lower()
            for a in anchors:
                if a and _anchor_in_text(low, a):
                    val = _best_price_from_line(lt)
                    if val is None:
                        continue
                    _assign_field(out, field, val, lt)
                    break

    for lt in combined_lines:
        m = re.search(
            r"\bO\b[\s:]*([\d,\.]+).*?\bH\b[\s:]*([\d,\.]+).*?\bL\b[\s:]*([\d,\.]+).*?\bC\b[\s:]*([\d,\.]+)",
            lt,
            re.I | re.DOTALL,
        )
        if m:
            try:
                out.open_price = float(m.group(1).replace(",", ""))
                out.high_price = float(m.group(2).replace(",", ""))
                out.low_price = float(m.group(3).replace(",", ""))
                out.close_price = float(m.group(4).replace(",", ""))
                out.raw_labels["ohlc_line"] = lt[:200]
            except ValueError:
                pass


def _assign_field(out: UISemanticReading, field: str, val: float, line: str) -> None:
    if field == "last_price":
        out.last_price = val
    elif field == "bid":
        out.bid = val
    elif field == "ask":
        out.ask = val
    elif field == "change_percent":
        out.change_percent = val
    elif field == "volume":
        out.volume = val
    elif field == "ohlc":
        pass
    out.raw_labels[field] = line[:120]


def _fill_from_regions(regional: Dict[str, List[OCRResult]], out: UISemanticReading) -> None:
    """Use typed OCR (price/volume/percent) inside regions when anchors missed."""
    leg = regional.get("legend_top_right", [])
    for r in leg:
        if r.data_type == "volume" and r.value and out.volume is None:
            out.volume = r.value
        if r.data_type == "percentage" and r.value and out.change_percent is None:
            out.change_percent = r.value
        if r.data_type == "price" and r.value and out.last_price is None:
            out.last_price = r.value


def _cluster_lines(ocr_results: List[OCRResult], y_tol: int = 14) -> List[str]:
    """Sort boxes into reading-order lines."""
    if not ocr_results:
        return []
    items = sorted(ocr_results, key=lambda r: (r.bbox[1], r.bbox[0]))
    groups: List[List[OCRResult]] = []
    cur: List[OCRResult] = [items[0]]
    base_y = items[0].bbox[1]
    for r in items[1:]:
        if abs(r.bbox[1] - base_y) <= y_tol:
            cur.append(r)
        else:
            groups.append(cur)
            cur = [r]
            base_y = r.bbox[1]
    groups.append(cur)
    out_lines: List[str] = []
    for grp in groups:
        line_sorted = sorted(grp, key=lambda x: x.bbox[0])
        out_lines.append(" ".join(t.text.strip() for t in line_sorted if t.text.strip()))
    return out_lines


_reader: Optional[SemanticReader] = None


def get_semantic_reader() -> Optional[SemanticReader]:
    global _reader
    try:
        from config import OCR_SEMANTIC_ENABLED
    except ImportError:
        OCR_SEMANTIC_ENABLED = True
    if not OCR_SEMANTIC_ENABLED:
        return None
    if _reader is None:
        from vision.ocr_reader import get_ocr_reader

        ocr = get_ocr_reader()
        if not ocr:
            return None
        _reader = SemanticReader(ocr)
    return _reader


def reset_semantic_reader() -> None:
    global _reader
    _reader = None
