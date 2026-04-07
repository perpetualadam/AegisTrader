"""
Market scanner for AegisTrader.
Multi-market scanning and opportunity scoring system.
"""

import time
import logging
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

from market_sessions import MarketSession, MarketType, get_active_markets
from assets import Asset, AssetManager, get_tradeable_assets
from vision.yolo_detector import YOLODetector, get_yolo_detector
from vision.ocr_reader import OCRReader, get_ocr_reader, PriceData
from vision.semantic_reader import UISemanticReading, get_semantic_reader
from browser.selenium_controller import SeleniumController, get_selenium_controller

logger = logging.getLogger(__name__)


def _merge_price_data(sem: Optional[PriceData], leg: Optional[PriceData]) -> Optional[PriceData]:
    """Prefer semantic fields; fill gaps from legacy full-image OCR."""
    if sem is None and leg is None:
        return None
    if sem is None:
        return leg
    if leg is None:
        return sem
    out = PriceData(timestamp=max(sem.timestamp, leg.timestamp))
    for attr in (
        "current_price",
        "high_price",
        "low_price",
        "open_price",
        "close_price",
        "volume",
        "change_percent",
        "change_value",
    ):
        sv = getattr(sem, attr, None)
        lv = getattr(leg, attr, None)
        setattr(out, attr, sv if sv is not None else lv)
    return out

@dataclass
class ScanResult:
    """Result of scanning a single asset."""
    asset: Asset
    timestamp: float
    price_data: Optional[PriceData] = None
    ui_semantic: Optional[UISemanticReading] = None
    pattern_analysis: Optional[Dict] = None
    technical_score: float = 0.0
    fundamental_score: float = 0.0
    overall_score: float = 0.0
    trading_signals: Optional[Dict] = None
    screenshot_path: Optional[str] = None
    scan_duration: float = 0.0
    errors: List[str] = field(default_factory=list)

@dataclass
class MarketOpportunity:
    """Represents a trading opportunity."""
    asset: Asset
    signal_type: str  # 'buy', 'sell', 'hold'
    confidence: float
    entry_price: Optional[float]
    target_price: Optional[float]
    stop_loss: Optional[float]
    risk_reward_ratio: Optional[float]
    timeframe: str
    reasoning: List[str]
    timestamp: float

class MarketScanner:
    """Multi-market scanner for identifying trading opportunities."""
    
    def __init__(self, max_workers: int = 4):
        self.asset_manager = AssetManager()
        self.market_session = MarketSession()
        self.yolo_detector = get_yolo_detector()
        self.ocr_reader = get_ocr_reader()
        self.browser_controller = get_selenium_controller()
        
        self.max_workers = max_workers
        self.scan_results: Dict[str, ScanResult] = {}
        self.opportunities: List[MarketOpportunity] = []
        self.is_scanning = False
        self.scan_thread = None
        
        # Scoring weights
        self.scoring_weights = {
            'technical_patterns': 0.4,
            'price_momentum': 0.3,
            'volume_analysis': 0.2,
            'market_session': 0.1
        }
        
        # Minimum scores for opportunities
        self.opportunity_thresholds = {
            'buy': 0.7,
            'sell': 0.7,
            'strong_buy': 0.85,
            'strong_sell': 0.85
        }
    
    def scan_asset(self, asset: Asset, timeframe: str = "1h") -> ScanResult:
        """
        Scan a single asset for trading opportunities.
        
        Args:
            asset: Asset to scan
            timeframe: Chart timeframe to analyze
            
        Returns:
            ScanResult with analysis data
        """
        start_time = time.time()
        result = ScanResult(asset=asset, timestamp=start_time)
        
        try:
            # Check if market is open for this asset
            if not self.market_session.is_market_open(asset.market_type):
                result.errors.append(f"Market {asset.market_type.value} is closed")
                return result
            
            # Open chart in browser
            if self.browser_controller:
                success = self.browser_controller.open_chart(asset.tradingview_ticker, timeframe)
                if not success:
                    result.errors.append("Failed to open chart in browser")
                    return result
                
                # Take screenshot
                result.screenshot_path = self.browser_controller.take_screenshot(
                    f"{asset.symbol}_{timeframe}_{int(start_time)}.png"
                )
                
                if not result.screenshot_path:
                    result.errors.append("Failed to take screenshot")
                    return result
            else:
                result.errors.append("Browser controller not available")
                return result
            
            # Analyze screenshot with YOLO
            if self.yolo_detector and result.screenshot_path:
                result.pattern_analysis = self.yolo_detector.analyze_chart_screenshot(result.screenshot_path)
                if 'error' in result.pattern_analysis:
                    result.errors.append(f"YOLO analysis failed: {result.pattern_analysis['error']}")
            
            # Extract price data: semantic UI reading + legacy OCR merge
            if self.ocr_reader and result.screenshot_path:
                import cv2

                image = cv2.imread(result.screenshot_path)
                if image is not None:
                    legacy_pd = self.ocr_reader.extract_price_data(image)
                    sem = get_semantic_reader()
                    if sem:
                        reading = sem.read_screen(image)
                        result.ui_semantic = reading
                        result.price_data = _merge_price_data(reading.to_price_data(), legacy_pd)
                    else:
                        result.price_data = legacy_pd
                else:
                    result.errors.append("Could not load screenshot for OCR")
            
            # Calculate scores
            result.technical_score = self._calculate_technical_score(result)
            result.fundamental_score = self._calculate_fundamental_score(result)
            result.overall_score = self._calculate_overall_score(result)
            
            # Generate trading signals
            result.trading_signals = self._generate_trading_signals(result)
            
            logger.info(f"Scanned {asset.symbol}: Score {result.overall_score:.2f}")
            
        except Exception as e:
            error_msg = f"Error scanning {asset.symbol}: {str(e)}"
            result.errors.append(error_msg)
            logger.error(error_msg)
        
        finally:
            result.scan_duration = time.time() - start_time
        
        return result
    
    def _calculate_technical_score(self, result: ScanResult) -> float:
        """Calculate technical analysis score."""
        score = 0.0
        
        # Pattern analysis score
        if result.pattern_analysis and 'confidence_score' in result.pattern_analysis:
            pattern_score = result.pattern_analysis['confidence_score']
            signal_strength = result.pattern_analysis.get('trading_signals', {}).get('signal_strength', 0.0)
            score += (pattern_score * 0.6 + signal_strength * 0.4) * self.scoring_weights['technical_patterns']
        
        # Price momentum score
        if result.price_data and result.price_data.change_percent is not None:
            momentum_score = min(abs(result.price_data.change_percent) / 10.0, 1.0)  # Normalize to 0-1
            score += momentum_score * self.scoring_weights['price_momentum']
        
        # Volume analysis score
        if result.price_data and result.price_data.volume is not None:
            # Simple volume score - could be enhanced with historical comparison
            volume_score = min(result.price_data.volume / 1000000, 1.0)  # Basic normalization
            score += volume_score * self.scoring_weights['volume_analysis']
        
        return min(score, 1.0)
    
    def _calculate_fundamental_score(self, result: ScanResult) -> float:
        """Calculate fundamental analysis score."""
        # Basic implementation - can be enhanced with fundamental data
        score = 0.5  # Neutral score
        
        # Market session bonus
        if self.market_session.is_market_open(result.asset.market_type):
            score += 0.1
        
        # Sector-based adjustments could be added here
        
        return min(score, 1.0)
    
    def _calculate_overall_score(self, result: ScanResult) -> float:
        """Calculate overall opportunity score."""
        technical_weight = 0.7
        fundamental_weight = 0.3
        
        overall = (result.technical_score * technical_weight + 
                  result.fundamental_score * fundamental_weight)
        
        # Penalty for errors
        error_penalty = len(result.errors) * 0.1
        overall = max(0.0, overall - error_penalty)
        
        return min(overall, 1.0)

    def _generate_trading_signals(self, result: ScanResult) -> Dict[str, Any]:
        """Generate trading signals from scan result."""
        signals = {
            'action': 'hold',
            'confidence': 0.0,
            'entry_price': None,
            'target_price': None,
            'stop_loss': None,
            'risk_reward_ratio': None,
            'reasoning': []
        }

        # Use pattern analysis signals if available
        if result.pattern_analysis and 'trading_signals' in result.pattern_analysis:
            pattern_signals = result.pattern_analysis['trading_signals']

            if pattern_signals.get('overall_sentiment') == 'bullish':
                signals['action'] = 'buy'
                signals['confidence'] = pattern_signals.get('signal_strength', 0.0)
                signals['reasoning'].append("Bullish chart patterns detected")

            elif pattern_signals.get('overall_sentiment') == 'bearish':
                signals['action'] = 'sell'
                signals['confidence'] = pattern_signals.get('signal_strength', 0.0)
                signals['reasoning'].append("Bearish chart patterns detected")

        # Add price-based signals
        if result.price_data:
            if result.price_data.change_percent and abs(result.price_data.change_percent) > 5:
                if result.price_data.change_percent > 0:
                    signals['reasoning'].append(f"Strong upward momentum: +{result.price_data.change_percent:.1f}%")
                else:
                    signals['reasoning'].append(f"Strong downward momentum: {result.price_data.change_percent:.1f}%")

            # Set price levels if available
            if result.price_data.current_price:
                signals['entry_price'] = result.price_data.current_price

                # Simple target and stop loss calculation
                if signals['action'] == 'buy':
                    signals['target_price'] = result.price_data.current_price * 1.04  # 4% target
                    signals['stop_loss'] = result.price_data.current_price * 0.98    # 2% stop
                elif signals['action'] == 'sell':
                    signals['target_price'] = result.price_data.current_price * 0.96  # 4% target
                    signals['stop_loss'] = result.price_data.current_price * 1.02    # 2% stop

                # Calculate risk-reward ratio
                if signals['target_price'] and signals['stop_loss'] and signals['entry_price']:
                    if signals['action'] == 'buy':
                        reward = signals['target_price'] - signals['entry_price']
                        risk = signals['entry_price'] - signals['stop_loss']
                    else:
                        reward = signals['entry_price'] - signals['target_price']
                        risk = signals['stop_loss'] - signals['entry_price']

                    if risk > 0:
                        signals['risk_reward_ratio'] = reward / risk

        return signals

    def scan_multiple_assets(self, assets: List[Asset], timeframe: str = "1h") -> Dict[str, ScanResult]:
        """
        Scan multiple assets concurrently.

        Args:
            assets: List of assets to scan
            timeframe: Chart timeframe for all assets

        Returns:
            Dictionary mapping asset symbols to scan results
        """
        results = {}

        # Filter assets by market session
        active_assets = [asset for asset in assets
                        if self.market_session.is_market_open(asset.market_type)]

        if not active_assets:
            logger.warning("No assets available for scanning (markets closed)")
            return results

        logger.info(f"Scanning {len(active_assets)} assets across active markets")

        # Use ThreadPoolExecutor for concurrent scanning
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all scan tasks
            future_to_asset = {
                executor.submit(self.scan_asset, asset, timeframe): asset
                for asset in active_assets
            }

            # Collect results as they complete
            for future in future_to_asset:
                asset = future_to_asset[future]
                try:
                    result = future.result(timeout=60)  # 60 second timeout per asset
                    results[asset.symbol] = result
                    self.scan_results[asset.symbol] = result
                except Exception as e:
                    logger.error(f"Failed to scan {asset.symbol}: {e}")
                    error_result = ScanResult(asset=asset, timestamp=time.time())
                    error_result.errors.append(str(e))
                    results[asset.symbol] = error_result

        return results

    def find_best_opportunities(self, min_score: float = 0.7, max_opportunities: int = 10) -> List[MarketOpportunity]:
        """
        Find the best trading opportunities from recent scans.

        Args:
            min_score: Minimum overall score for opportunities
            max_opportunities: Maximum number of opportunities to return

        Returns:
            List of best trading opportunities
        """
        opportunities = []

        for symbol, result in self.scan_results.items():
            if result.overall_score >= min_score and result.trading_signals:
                signals = result.trading_signals

                if signals['action'] in ['buy', 'sell'] and signals['confidence'] > 0.5:
                    opportunity = MarketOpportunity(
                        asset=result.asset,
                        signal_type=signals['action'],
                        confidence=signals['confidence'],
                        entry_price=signals.get('entry_price'),
                        target_price=signals.get('target_price'),
                        stop_loss=signals.get('stop_loss'),
                        risk_reward_ratio=signals.get('risk_reward_ratio'),
                        timeframe="1h",  # Default timeframe
                        reasoning=signals.get('reasoning', []),
                        timestamp=result.timestamp
                    )
                    opportunities.append(opportunity)

        # Sort by overall score and confidence
        opportunities.sort(
            key=lambda x: (self.scan_results[x.asset.symbol].overall_score, x.confidence),
            reverse=True
        )

        self.opportunities = opportunities[:max_opportunities]
        return self.opportunities

    def start_continuous_scanning(self, assets: List[Asset], scan_interval: int = 300, timeframe: str = "1h"):
        """
        Start continuous scanning of assets.

        Args:
            assets: Assets to scan continuously
            scan_interval: Interval between scans in seconds
            timeframe: Chart timeframe to use
        """
        if self.is_scanning:
            logger.warning("Continuous scanning already running")
            return

        self.is_scanning = True

        def scan_loop():
            while self.is_scanning:
                try:
                    logger.info("Starting scan cycle...")
                    start_time = time.time()

                    # Scan all assets
                    results = self.scan_multiple_assets(assets, timeframe)

                    # Find opportunities
                    opportunities = self.find_best_opportunities()

                    scan_duration = time.time() - start_time
                    logger.info(f"Scan cycle completed in {scan_duration:.1f}s. "
                              f"Found {len(opportunities)} opportunities.")

                    # Wait for next scan
                    if self.is_scanning:
                        time.sleep(scan_interval)

                except Exception as e:
                    logger.error(f"Error in scan loop: {e}")
                    if self.is_scanning:
                        time.sleep(60)  # Wait 1 minute before retrying

        self.scan_thread = threading.Thread(target=scan_loop, daemon=True)
        self.scan_thread.start()
        logger.info(f"Started continuous scanning with {scan_interval}s interval")

    def stop_continuous_scanning(self):
        """Stop continuous scanning."""
        if self.is_scanning:
            self.is_scanning = False
            if self.scan_thread:
                self.scan_thread.join(timeout=10)
            logger.info("Stopped continuous scanning")

    def get_scan_summary(self) -> Dict[str, Any]:
        """Get summary of recent scanning activity."""
        if not self.scan_results:
            return {"message": "No scan results available"}

        total_scans = len(self.scan_results)
        successful_scans = len([r for r in self.scan_results.values() if not r.errors])
        avg_score = sum(r.overall_score for r in self.scan_results.values()) / total_scans

        # Group by market type
        market_breakdown = {}
        for result in self.scan_results.values():
            market = result.asset.market_type.value
            if market not in market_breakdown:
                market_breakdown[market] = {'count': 0, 'avg_score': 0.0}
            market_breakdown[market]['count'] += 1

        # Calculate average scores by market
        for market in market_breakdown:
            market_results = [r for r in self.scan_results.values()
                            if r.asset.market_type.value == market]
            market_breakdown[market]['avg_score'] = sum(r.overall_score for r in market_results) / len(market_results)

        return {
            'total_scans': total_scans,
            'successful_scans': successful_scans,
            'success_rate': successful_scans / total_scans if total_scans > 0 else 0,
            'average_score': avg_score,
            'opportunities_found': len(self.opportunities),
            'market_breakdown': market_breakdown,
            'top_opportunities': [
                {
                    'symbol': opp.asset.symbol,
                    'signal': opp.signal_type,
                    'confidence': opp.confidence,
                    'score': self.scan_results[opp.asset.symbol].overall_score
                }
                for opp in self.opportunities[:5]
            ]
        }

# Global scanner instance
market_scanner = None

def get_market_scanner() -> MarketScanner:
    """Get the global market scanner instance."""
    global market_scanner
    if market_scanner is None:
        market_scanner = MarketScanner()
    return market_scanner

if __name__ == "__main__":
    # Test the market scanner
    scanner = MarketScanner()

    print("Market Scanner Test")
    print("=" * 30)

    # Get some test assets
    test_assets = get_tradeable_assets([MarketType.CRYPTO])[:3]  # Test with 3 crypto assets

    if test_assets:
        print(f"Testing with {len(test_assets)} assets:")
        for asset in test_assets:
            print(f"  - {asset.symbol} ({asset.name})")

        # Test single asset scan
        if scanner.browser_controller:
            print(f"\nScanning {test_assets[0].symbol}...")
            result = scanner.scan_asset(test_assets[0])
            print(f"Score: {result.overall_score:.2f}")
            print(f"Errors: {len(result.errors)}")
            if result.trading_signals:
                print(f"Signal: {result.trading_signals['action']}")
        else:
            print("Browser controller not available for testing")
    else:
        print("No test assets available")
