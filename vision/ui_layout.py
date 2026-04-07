"""
TradingView (and generic) UI layout: normalized regions scale to any screenshot size.

Edit ``tradingview_ui_layout.default.json`` (or set TRADINGVIEW_UI_LAYOUT_PATH) to match
your monitor resolution, theme, and panel layout.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

NormBox = Tuple[float, float, float, float]  # x1, y1, x2, y2 in 0..1


@dataclass
class UILayout:
    """Normalized layout: regions and optional semantic hints."""

    reference_resolution: Tuple[int, int]
    regions: Dict[str, NormBox]
    semantic_hints: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    version: str = "1"

    def pixel_box(self, name: str, width: int, height: int) -> Optional[Tuple[int, int, int, int]]:
        """Map normalized region name to pixel (x1, y1, x2, y2)."""
        if name not in self.regions:
            return None
        x1, y1, x2, y2 = self.regions[name]
        return (
            int(x1 * width),
            int(y1 * height),
            int(x2 * width),
            int(y2 * height),
        )

    def all_pixel_regions(
        self, width: int, height: int
    ) -> List[Tuple[str, Tuple[int, int, int, int]]]:
        out: List[Tuple[str, Tuple[int, int, int, int]]] = []
        for name in self.regions:
            box = self.pixel_box(name, width, height)
            if box and box[2] > box[0] and box[3] > box[1]:
                out.append((name, box))
        return out


def load_ui_layout(path: Optional[Path] = None) -> UILayout:
    """Load layout JSON; falls back to packaged default."""
    from config import TRADINGVIEW_UI_LAYOUT_PATH

    p = Path(path or TRADINGVIEW_UI_LAYOUT_PATH)
    if not p.is_file():
        default = Path(__file__).resolve().parent / "tradingview_ui_layout.default.json"
        if default.is_file():
            logger.warning("UI layout not found at %s — using %s", p, default)
            p = default
        else:
            logger.warning("No UI layout file — using single full-screen region")
            return UILayout(
                reference_resolution=(1920, 1080),
                regions={"full_panel": (0.0, 0.0, 1.0, 1.0)},
            )

    with open(p, encoding="utf-8") as f:
        raw = json.load(f)

    ref = tuple(raw.get("reference_resolution", [1920, 1080]))
    regions: Dict[str, NormBox] = {}
    for k, v in raw.get("regions", {}).items():
        if isinstance(v, dict) and "norm" in v:
            regions[k] = tuple(v["norm"])  # type: ignore
        elif isinstance(v, list) and len(v) == 4:
            regions[k] = tuple(float(x) for x in v)  # type: ignore

    hints = raw.get("semantic_hints", {})
    return UILayout(
        reference_resolution=(int(ref[0]), int(ref[1])),
        regions=regions,
        semantic_hints=hints,
        version=str(raw.get("version", "1")),
    )
