"""Semantic OCR merge and anchor helpers (no screenshot required)."""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vision.ocr_reader import OCRResult
from vision.semantic_reader import (
    UISemanticReading,
    merge_ocr_results,
    _anchor_in_text,
    _cluster_lines,
    _assign_field,
)


def test_merge_ocr_dedupes():
    a = OCRResult(
        text="1.23",
        confidence=0.9,
        bbox=(10, 10, 50, 30),
        data_type="price",
        value=1.23,
        timestamp=time.time(),
    )
    b = OCRResult(
        text="1.23",
        confidence=0.5,
        bbox=(12, 11, 48, 29),
        data_type="price",
        value=1.23,
        timestamp=time.time(),
    )
    m = merge_ocr_results([[a, b]])
    assert len(m) == 1
    assert m[0].confidence == 0.9


def test_anchor_word_boundary():
    assert _anchor_in_text("last price 100", "last")
    assert not _anchor_in_text("lastly noted", "last")
    assert _anchor_in_text("l: 100", "l:")


def test_cluster_lines_order():
    r1 = OCRResult("A", 1.0, (0, 0, 10, 10), "text", None, 0.0)
    r2 = OCRResult("B", 1.0, (15, 0, 25, 10), "text", None, 0.0)
    lines = _cluster_lines([r1, r2])
    assert len(lines) == 1
    assert "A" in lines[0] and "B" in lines[0]


def test_assign_field():
    u = UISemanticReading()
    _assign_field(u, "last_price", 42.5, "Last 42.5")
    assert u.last_price == 42.5
    assert "last_price" in u.raw_labels
