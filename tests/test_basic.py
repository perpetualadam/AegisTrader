"""
Basic tests for AegisTrader components.
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import validate_config, get_config_summary
from assets import AssetManager, Asset, MarketType
from market_sessions import MarketSession, get_active_markets
from vision.yolo_detector import YOLODetector
from vision.ocr_reader import OCRReader
from strategy.strategy_engine import StrategyEngine, SignalType
from execution.execution import Execution, OrderType
from risk.risk_manager import RiskManager
from broker.broker_api import MockBrokerAPI

class TestConfig:
    """Test configuration management."""
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Should pass with default config
        assert validate_config() == True
    
    def test_config_summary(self):
        """Test configuration summary."""
        summary = get_config_summary()
        assert isinstance(summary, dict)
        assert 'trading_mode' in summary
        assert 'markets' in summary

class TestAssets:
    """Test asset management."""
    
    def test_asset_creation(self):
        """Test asset creation."""
        asset = Asset(
            symbol="BTCUSDT",
            name="Bitcoin",
            market_type=MarketType.CRYPTO,
            tradingview_ticker="BINANCE:BTCUSDT",
            exchange="Binance"
        )
        assert asset.symbol == "BTCUSDT"
        assert asset.market_type == MarketType.CRYPTO
    
    def test_asset_manager(self):
        """Test asset manager."""
        manager = AssetManager()
        assets = manager.get_assets_by_market(MarketType.CRYPTO)
        assert len(assets) > 0
        assert all(asset.market_type == MarketType.CRYPTO for asset in assets)

class TestMarketSessions:
    """Test market session management."""
    
    def test_market_session_creation(self):
        """Test market session creation."""
        session = MarketSession()
        assert session.timezone.zone == 'Europe/London'
    
    def test_active_markets(self):
        """Test active markets detection."""
        active = get_active_markets()
        assert isinstance(active, list)

class TestVision:
    """Test vision components."""
    
    @patch('ultralytics.YOLO')
    def test_yolo_detector(self, mock_yolo):
        """Test YOLO detector initialization."""
        detector = YOLODetector()
        assert detector is not None
    
    def test_ocr_reader(self):
        """Test OCR reader initialization."""
        reader = OCRReader()
        assert reader is not None
        assert reader.engine in ['tesseract', 'easyocr', 'paddleocr']

class TestStrategy:
    """Test strategy engine."""
    
    def test_strategy_engine_creation(self):
        """Test strategy engine creation."""
        engine = StrategyEngine()
        assert engine is not None
        assert len(engine.enabled_strategies) > 0
    
    def test_signal_types(self):
        """Test signal type enum."""
        assert SignalType.BUY.value == "buy"
        assert SignalType.SELL.value == "sell"

class TestExecution:
    """Test execution engine."""
    
    def test_execution_creation(self):
        """Test execution engine creation."""
        execution = Execution(initial_balance=10000.0)
        assert execution.initial_balance == 10000.0
        assert execution.current_balance == 10000.0
    
    def test_order_types(self):
        """Test order type enum."""
        assert OrderType.MARKET.value == "market"
        assert OrderType.LIMIT.value == "limit"

class TestRisk:
    """Test risk management."""
    
    def test_risk_manager_creation(self):
        """Test risk manager creation."""
        rm = RiskManager()
        assert rm.max_position_size > 0
        assert rm.max_daily_loss > 0

class TestBroker:
    """Test broker API."""
    
    def test_mock_broker(self):
        """Test mock broker API."""
        broker = MockBrokerAPI("test_key", "test_secret")
        assert broker.connect() == True
        assert broker.is_connected == True
        
        # Test order placement
        result = broker.place_order("BTCUSDT", "buy", 0.1, "market", 50000.0)
        assert result.success == True
        assert result.order_id is not None

if __name__ == "__main__":
    pytest.main([__file__])
