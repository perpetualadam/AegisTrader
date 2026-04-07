"""
OCR-based price and chart data reading for AegisTrader.
Extracts numerical data and text from trading charts.
"""

import cv2
import numpy as np
import re
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
import logging
from pathlib import Path
import time

# OCR engine imports with fallbacks
OCR_ENGINES = {}

try:
    import pytesseract
    OCR_ENGINES['tesseract'] = True
except ImportError:
    OCR_ENGINES['tesseract'] = False

try:
    import easyocr
    OCR_ENGINES['easyocr'] = True
except ImportError:
    OCR_ENGINES['easyocr'] = False

try:
    import paddleocr
    OCR_ENGINES['paddleocr'] = True
except ImportError:
    OCR_ENGINES['paddleocr'] = False

from config import OCR_ENGINE

logger = logging.getLogger(__name__)

@dataclass
class OCRResult:
    """Represents OCR extraction result."""
    text: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2
    data_type: str  # 'price', 'volume', 'percentage', 'time', 'text'
    value: Optional[float] = None
    timestamp: float = 0.0

@dataclass
class PriceData:
    """Represents extracted price information."""
    current_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    open_price: Optional[float] = None
    close_price: Optional[float] = None
    volume: Optional[float] = None
    change_percent: Optional[float] = None
    change_value: Optional[float] = None
    timestamp: float = 0.0

class OCRReader:
    """OCR-based reader for extracting data from trading charts."""
    
    def __init__(self, engine: str = None):
        self.engine = engine or OCR_ENGINE
        self.ocr_instance = None
        self.is_initialized = False
        
        # Price patterns for different formats
        self.price_patterns = [
            r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2,8})?)',  # $1,234.56 or 1,234.56789
            r'(\d+\.\d{2,8})',                          # 1234.56789
            r'(\d{1,3}(?:,\d{3})+)',                    # 1,234,567
            r'(\d+)',                                   # 1234
        ]
        
        # Percentage patterns
        self.percentage_patterns = [
            r'([+-]?\d+\.?\d*)\s*%',                    # +5.67% or -2.34%
            r'([+-]?\d+\.?\d*)\s*percent',              # 5.67 percent
        ]
        
        # Volume patterns
        self.volume_patterns = [
            r'(\d+\.?\d*)\s*[KMBkmb]',                  # 1.5K, 2.3M, 1.1B
            r'Vol:?\s*(\d+\.?\d*)\s*[KMBkmb]?',        # Vol: 1.5K
            r'Volume:?\s*(\d+\.?\d*)\s*[KMBkmb]?',     # Volume: 1.5M
        ]
        
        self.initialize_ocr()
    
    def initialize_ocr(self) -> bool:
        """Initialize the OCR engine."""
        try:
            if self.engine == 'tesseract' and OCR_ENGINES['tesseract']:
                # Tesseract is ready to use
                self.is_initialized = True
                logger.info("Tesseract OCR initialized")
                
            elif self.engine == 'easyocr' and OCR_ENGINES['easyocr']:
                self.ocr_instance = easyocr.Reader(['en'])
                self.is_initialized = True
                logger.info("EasyOCR initialized")
                
            elif self.engine == 'paddleocr' and OCR_ENGINES['paddleocr']:
                self.ocr_instance = paddleocr.PaddleOCR(use_angle_cls=True, lang='en')
                self.is_initialized = True
                logger.info("PaddleOCR initialized")
                
            else:
                # Fallback to available engine
                for engine_name, available in OCR_ENGINES.items():
                    if available:
                        logger.warning(f"Requested engine '{self.engine}' not available. Using {engine_name}")
                        self.engine = engine_name
                        return self.initialize_ocr()
                
                logger.error("No OCR engines available")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize OCR engine '{self.engine}': {e}")
            return False
    
    def preprocess_image(self, image: np.ndarray, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        Preprocess image for better OCR results.
        
        Args:
            image: Input image
            region: Optional region to crop (x1, y1, x2, y2)
            
        Returns:
            Preprocessed image
        """
        # Crop region if specified
        if region:
            x1, y1, x2, y2 = region
            image = image[y1:y2, x1:x2]
        
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply image enhancements
        # 1. Increase contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # 2. Denoise
        denoised = cv2.fastNlMeansDenoising(enhanced)
        
        # 3. Threshold for better text extraction
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def extract_text_tesseract(self, image: np.ndarray) -> List[OCRResult]:
        """Extract text using Tesseract OCR."""
        try:
            # Configure Tesseract for better number recognition
            config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.,$%+-KMBkmb'
            
            # Get detailed data
            data = pytesseract.image_to_data(image, config=config, output_type=pytesseract.Output.DICT)
            
            results = []
            timestamp = time.time()
            
            for i in range(len(data['text'])):
                text = data['text'][i].strip()
                if text and int(data['conf'][i]) > 30:  # Confidence threshold
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    
                    result = OCRResult(
                        text=text,
                        confidence=float(data['conf'][i]) / 100.0,
                        bbox=(x, y, x + w, y + h),
                        data_type=self._classify_text(text),
                        timestamp=timestamp
                    )
                    
                    # Extract numerical value if applicable
                    result.value = self._extract_numerical_value(text, result.data_type)
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Tesseract OCR error: {e}")
            return []
    
    def extract_text_easyocr(self, image: np.ndarray) -> List[OCRResult]:
        """Extract text using EasyOCR."""
        try:
            results_raw = self.ocr_instance.readtext(image)
            results = []
            timestamp = time.time()
            
            for bbox, text, confidence in results_raw:
                if confidence > 0.3:  # Confidence threshold
                    # Convert bbox format
                    x_coords = [point[0] for point in bbox]
                    y_coords = [point[1] for point in bbox]
                    x1, y1, x2, y2 = min(x_coords), min(y_coords), max(x_coords), max(y_coords)
                    
                    result = OCRResult(
                        text=text.strip(),
                        confidence=confidence,
                        bbox=(int(x1), int(y1), int(x2), int(y2)),
                        data_type=self._classify_text(text),
                        timestamp=timestamp
                    )
                    
                    result.value = self._extract_numerical_value(text, result.data_type)
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"EasyOCR error: {e}")
            return []
    
    def extract_text_paddleocr(self, image: np.ndarray) -> List[OCRResult]:
        """Extract text using PaddleOCR."""
        try:
            results_raw = self.ocr_instance.ocr(image, cls=True)
            results = []
            timestamp = time.time()
            
            for line in results_raw:
                for bbox, (text, confidence) in line:
                    if confidence > 0.3:  # Confidence threshold
                        # Convert bbox format
                        x_coords = [point[0] for point in bbox]
                        y_coords = [point[1] for point in bbox]
                        x1, y1, x2, y2 = min(x_coords), min(y_coords), max(x_coords), max(y_coords)
                        
                        result = OCRResult(
                            text=text.strip(),
                            confidence=confidence,
                            bbox=(int(x1), int(y1), int(x2), int(y2)),
                            data_type=self._classify_text(text),
                            timestamp=timestamp
                        )
                        
                        result.value = self._extract_numerical_value(text, result.data_type)
                        results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"PaddleOCR error: {e}")
            return []
    
    def extract_text(self, image: np.ndarray, region: Optional[Tuple[int, int, int, int]] = None) -> List[OCRResult]:
        """
        Extract text from image using the configured OCR engine.
        
        Args:
            image: Input image
            region: Optional region to focus on
            
        Returns:
            List of OCR results
        """
        if not self.is_initialized:
            logger.warning("OCR not initialized")
            return []
        
        # Preprocess image
        processed_image = self.preprocess_image(image, region)
        
        # Extract text based on engine
        if self.engine == 'tesseract':
            return self.extract_text_tesseract(processed_image)
        elif self.engine == 'easyocr':
            return self.extract_text_easyocr(processed_image)
        elif self.engine == 'paddleocr':
            return self.extract_text_paddleocr(processed_image)
        else:
            logger.error(f"Unknown OCR engine: {self.engine}")
            return []
    
    def _classify_text(self, text: str) -> str:
        """Classify extracted text by type."""
        text_clean = text.strip()
        
        # Check for percentage
        if any(re.search(pattern, text_clean) for pattern in self.percentage_patterns):
            return 'percentage'
        
        # Check for volume
        if any(re.search(pattern, text_clean, re.IGNORECASE) for pattern in self.volume_patterns):
            return 'volume'
        
        # Check for price
        if any(re.search(pattern, text_clean) for pattern in self.price_patterns):
            return 'price'
        
        # Check for time patterns
        if re.search(r'\d{1,2}:\d{2}', text_clean) or re.search(r'\d{1,2}/\d{1,2}', text_clean):
            return 'time'
        
        return 'text'
    
    def _extract_numerical_value(self, text: str, data_type: str) -> Optional[float]:
        """Extract numerical value from text based on data type."""
        try:
            text_clean = text.strip()
            
            if data_type == 'percentage':
                match = re.search(r'([+-]?\d+\.?\d*)', text_clean)
                if match:
                    return float(match.group(1))
            
            elif data_type == 'volume':
                # Handle K, M, B suffixes
                match = re.search(r'(\d+\.?\d*)\s*([KMBkmb]?)', text_clean)
                if match:
                    value = float(match.group(1))
                    suffix = match.group(2).upper()
                    multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
                    return value * multipliers.get(suffix, 1)
            
            elif data_type == 'price':
                # Remove currency symbols and commas
                clean_text = re.sub(r'[$,]', '', text_clean)
                match = re.search(r'(\d+\.?\d*)', clean_text)
                if match:
                    return float(match.group(1))
            
            return None
            
        except (ValueError, AttributeError):
            return None
    
    def extract_price_data(self, image: np.ndarray, price_regions: Optional[Dict[str, Tuple[int, int, int, int]]] = None) -> PriceData:
        """
        Extract comprehensive price data from chart image.
        
        Args:
            image: Chart image
            price_regions: Optional dictionary of regions for specific price elements
            
        Returns:
            PriceData object with extracted information
        """
        price_data = PriceData(timestamp=time.time())
        
        if price_regions:
            # Extract from specific regions
            for data_type, region in price_regions.items():
                ocr_results = self.extract_text(image, region)
                for result in ocr_results:
                    if result.data_type == 'price' and result.value:
                        setattr(price_data, data_type, result.value)
                        break
        else:
            # Extract from entire image
            ocr_results = self.extract_text(image)
            
            # Find price-related values
            prices = [r for r in ocr_results if r.data_type == 'price' and r.value]
            volumes = [r for r in ocr_results if r.data_type == 'volume' and r.value]
            percentages = [r for r in ocr_results if r.data_type == 'percentage' and r.value]
            
            # Assign values based on confidence and position
            if prices:
                # Sort by confidence and take the best ones
                prices.sort(key=lambda x: x.confidence, reverse=True)
                price_data.current_price = prices[0].value
                
                if len(prices) > 1:
                    price_data.high_price = max(p.value for p in prices[:4])
                    price_data.low_price = min(p.value for p in prices[:4])
            
            if volumes:
                volumes.sort(key=lambda x: x.confidence, reverse=True)
                price_data.volume = volumes[0].value
            
            if percentages:
                percentages.sort(key=lambda x: x.confidence, reverse=True)
                price_data.change_percent = percentages[0].value
        
        return price_data

# Global OCR reader instance
ocr_reader = None

def get_ocr_reader() -> Optional[OCRReader]:
    """Get the global OCR reader instance."""
    global ocr_reader
    if ocr_reader is None:
        ocr_reader = OCRReader()
    return ocr_reader if ocr_reader.is_initialized else None

if __name__ == "__main__":
    # Test the OCR reader
    reader = OCRReader()
    
    if reader.is_initialized:
        print(f"OCR Reader initialized successfully with {reader.engine}")
        print("Available OCR engines:")
        for engine, available in OCR_ENGINES.items():
            status = "✓" if available else "✗"
            print(f"  {status} {engine}")
    else:
        print("Failed to initialize OCR reader")
