"""
YOLO-based chart pattern detection for AegisTrader.
Detects trading patterns and chart elements from screenshots.
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
import logging
from pathlib import Path
import time

try:
    import torch
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logging.warning("YOLO dependencies not available. Install ultralytics package.")

from config import YOLO_MODEL_PATH, MODELS_DIR

logger = logging.getLogger(__name__)

@dataclass
class Detection:
    """Represents a detected pattern or chart element."""
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2
    center: Tuple[int, int]
    area: float
    timestamp: float

class ChartPattern:
    """Chart pattern types that can be detected."""
    SUPPORT_RESISTANCE = "support_resistance"
    TREND_LINE = "trend_line"
    TRIANGLE = "triangle"
    HEAD_SHOULDERS = "head_shoulders"
    DOUBLE_TOP = "double_top"
    DOUBLE_BOTTOM = "double_bottom"
    FLAG = "flag"
    PENNANT = "pennant"
    WEDGE = "wedge"
    CHANNEL = "channel"
    CANDLESTICK_PATTERN = "candlestick_pattern"
    VOLUME_SPIKE = "volume_spike"
    PRICE_LEVEL = "price_level"
    CHART_ELEMENT = "chart_element"

class YOLODetector:
    """YOLO-based detector for chart patterns and trading signals."""
    
    def __init__(self, model_path: Optional[str] = None, confidence_threshold: float = 0.5):
        self.model_path = model_path or YOLO_MODEL_PATH
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.is_initialized = False
        
        # Pattern confidence thresholds
        self.pattern_thresholds = {
            ChartPattern.SUPPORT_RESISTANCE: 0.6,
            ChartPattern.TREND_LINE: 0.5,
            ChartPattern.TRIANGLE: 0.7,
            ChartPattern.HEAD_SHOULDERS: 0.8,
            ChartPattern.DOUBLE_TOP: 0.7,
            ChartPattern.DOUBLE_BOTTOM: 0.7,
            ChartPattern.FLAG: 0.6,
            ChartPattern.PENNANT: 0.6,
            ChartPattern.WEDGE: 0.6,
            ChartPattern.CHANNEL: 0.5,
            ChartPattern.CANDLESTICK_PATTERN: 0.4,
            ChartPattern.VOLUME_SPIKE: 0.5,
            ChartPattern.PRICE_LEVEL: 0.3,
            ChartPattern.CHART_ELEMENT: 0.3,
        }
        
        self.initialize_model()
    
    def initialize_model(self) -> bool:
        """Initialize the YOLO model."""
        if not YOLO_AVAILABLE:
            logger.error("YOLO not available. Cannot initialize detector.")
            return False
        
        try:
            # Check if custom model exists
            model_path = Path(self.model_path)
            if model_path.exists():
                logger.info(f"Loading custom YOLO model from {model_path}")
                self.model = YOLO(str(model_path))
            else:
                # Use a pre-trained model as fallback
                logger.warning(f"Custom model not found at {model_path}. Using YOLOv8n as fallback.")
                self.model = YOLO('yolov8n.pt')
                
                # Create models directory if it doesn't exist
                MODELS_DIR.mkdir(exist_ok=True)
                
                # Save the model to the expected location for future use
                fallback_path = MODELS_DIR / "yolov8n_fallback.pt"
                if not fallback_path.exists():
                    self.model.save(str(fallback_path))
                    logger.info(f"Saved fallback model to {fallback_path}")
            
            self.is_initialized = True
            logger.info("YOLO detector initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize YOLO model: {e}")
            return False
    
    def detect_patterns(self, image: np.ndarray) -> List[Detection]:
        """
        Detect chart patterns in an image.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of detected patterns
        """
        if not self.is_initialized:
            logger.warning("YOLO detector not initialized")
            return []
        
        try:
            # Run inference
            results = self.model(image, conf=self.confidence_threshold, verbose=False)
            
            detections = []
            timestamp = time.time()
            
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        # Extract detection data
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = float(box.conf[0].cpu().numpy())
                        class_id = int(box.cls[0].cpu().numpy())
                        
                        # Get class name (use index if names not available)
                        if hasattr(self.model, 'names') and class_id < len(self.model.names):
                            class_name = self.model.names[class_id]
                        else:
                            class_name = f"class_{class_id}"
                        
                        # Calculate center and area
                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1 + y2) / 2)
                        area = (x2 - x1) * (y2 - y1)
                        
                        # Create detection object
                        detection = Detection(
                            class_name=class_name,
                            confidence=confidence,
                            bbox=(int(x1), int(y1), int(x2), int(y2)),
                            center=(center_x, center_y),
                            area=area,
                            timestamp=timestamp
                        )
                        
                        detections.append(detection)
            
            logger.debug(f"Detected {len(detections)} patterns")
            return detections
            
        except Exception as e:
            logger.error(f"Error during pattern detection: {e}")
            return []
    
    def filter_detections_by_confidence(self, detections: List[Detection]) -> List[Detection]:
        """Filter detections based on pattern-specific confidence thresholds."""
        filtered = []
        
        for detection in detections:
            threshold = self.pattern_thresholds.get(detection.class_name, self.confidence_threshold)
            if detection.confidence >= threshold:
                filtered.append(detection)
        
        return filtered
    
    def get_strongest_signals(self, detections: List[Detection], max_signals: int = 5) -> List[Detection]:
        """Get the strongest trading signals from detections."""
        # Sort by confidence and return top signals
        sorted_detections = sorted(detections, key=lambda x: x.confidence, reverse=True)
        return sorted_detections[:max_signals]
    
    def analyze_chart_screenshot(self, screenshot_path: str) -> Dict[str, Any]:
        """
        Analyze a chart screenshot and return trading insights.
        
        Args:
            screenshot_path: Path to the screenshot image
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Load image
            image = cv2.imread(screenshot_path)
            if image is None:
                logger.error(f"Could not load image from {screenshot_path}")
                return {"error": "Could not load image"}
            
            # Convert BGR to RGB for YOLO
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect patterns
            raw_detections = self.detect_patterns(image_rgb)
            filtered_detections = self.filter_detections_by_confidence(raw_detections)
            strong_signals = self.get_strongest_signals(filtered_detections)
            
            # Analyze patterns for trading signals
            analysis = {
                "timestamp": time.time(),
                "image_path": screenshot_path,
                "total_detections": len(raw_detections),
                "filtered_detections": len(filtered_detections),
                "strong_signals": len(strong_signals),
                "patterns": [],
                "trading_signals": self._generate_trading_signals(strong_signals),
                "confidence_score": self._calculate_overall_confidence(strong_signals)
            }
            
            # Add pattern details
            for detection in strong_signals:
                pattern_info = {
                    "pattern": detection.class_name,
                    "confidence": detection.confidence,
                    "location": detection.center,
                    "bbox": detection.bbox,
                    "area": detection.area
                }
                analysis["patterns"].append(pattern_info)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing chart screenshot: {e}")
            return {"error": str(e)}
    
    def _generate_trading_signals(self, detections: List[Detection]) -> Dict[str, Any]:
        """Generate trading signals from detected patterns."""
        signals = {
            "bullish_signals": 0,
            "bearish_signals": 0,
            "neutral_signals": 0,
            "overall_sentiment": "neutral",
            "signal_strength": 0.0,
            "recommended_action": "hold"
        }
        
        # Pattern sentiment mapping
        bullish_patterns = [
            ChartPattern.DOUBLE_BOTTOM,
            ChartPattern.SUPPORT_RESISTANCE,
            ChartPattern.TRIANGLE,  # Assuming ascending triangle
            ChartPattern.FLAG,      # Assuming bullish flag
            ChartPattern.VOLUME_SPIKE
        ]
        
        bearish_patterns = [
            ChartPattern.DOUBLE_TOP,
            ChartPattern.HEAD_SHOULDERS,
            ChartPattern.WEDGE      # Assuming falling wedge
        ]
        
        total_confidence = 0.0
        
        for detection in detections:
            if detection.class_name in bullish_patterns:
                signals["bullish_signals"] += 1
                total_confidence += detection.confidence
            elif detection.class_name in bearish_patterns:
                signals["bearish_signals"] += 1
                total_confidence += detection.confidence
            else:
                signals["neutral_signals"] += 1
                total_confidence += detection.confidence * 0.5
        
        # Calculate overall sentiment
        if signals["bullish_signals"] > signals["bearish_signals"]:
            signals["overall_sentiment"] = "bullish"
            signals["recommended_action"] = "buy"
        elif signals["bearish_signals"] > signals["bullish_signals"]:
            signals["overall_sentiment"] = "bearish"
            signals["recommended_action"] = "sell"
        
        # Calculate signal strength
        total_signals = len(detections)
        if total_signals > 0:
            signals["signal_strength"] = min(total_confidence / total_signals, 1.0)
        
        return signals
    
    def _calculate_overall_confidence(self, detections: List[Detection]) -> float:
        """Calculate overall confidence score for the analysis."""
        if not detections:
            return 0.0
        
        # Weight by confidence and number of detections
        total_confidence = sum(d.confidence for d in detections)
        avg_confidence = total_confidence / len(detections)
        
        # Boost confidence if multiple patterns detected
        pattern_bonus = min(len(detections) * 0.1, 0.3)
        
        return min(avg_confidence + pattern_bonus, 1.0)

# Global detector instance
yolo_detector = None

def get_yolo_detector() -> Optional[YOLODetector]:
    """Get the global YOLO detector instance."""
    global yolo_detector
    if yolo_detector is None:
        yolo_detector = YOLODetector()
    return yolo_detector if yolo_detector.is_initialized else None

if __name__ == "__main__":
    # Test the YOLO detector
    detector = YOLODetector()
    
    if detector.is_initialized:
        print("YOLO Detector initialized successfully")
        print(f"Model path: {detector.model_path}")
        print(f"Confidence threshold: {detector.confidence_threshold}")
        print("Pattern thresholds:")
        for pattern, threshold in detector.pattern_thresholds.items():
            print(f"  {pattern}: {threshold}")
    else:
        print("Failed to initialize YOLO detector")
