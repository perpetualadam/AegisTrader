"""
Configuration module for AegisTrader.
Handles environment variables, trading modes, and credential management.
"""

import os
import logging
from typing import Optional
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment variables from {env_path}")
except ImportError:
    print("python-dotenv not installed. Using system environment variables only.")

# Trading Mode Configuration
LIVE_TRADING = os.getenv("LIVE_TRADING", "False").lower() in ("true", "1", "yes")
PAPER_TRADING = not LIVE_TRADING

# Broker API Credentials
BROKER_API_KEY = os.getenv("BROKER_API_KEY")
BROKER_API_SECRET = os.getenv("BROKER_API_SECRET")
BROKER_API_PASSPHRASE = os.getenv("BROKER_API_PASSPHRASE")  # For some exchanges
BROKER_SANDBOX = os.getenv("BROKER_SANDBOX", "True").lower() in ("true", "1", "yes")

# TradingView Configuration
TRADINGVIEW_USERNAME = os.getenv("TRADINGVIEW_USERNAME")
TRADINGVIEW_PASSWORD = os.getenv("TRADINGVIEW_PASSWORD")

# Vision System Configuration
YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "models/yolo_chart_patterns.pt")
OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")  # tesseract, easyocr, paddleocr
SCREENSHOT_INTERVAL = float(os.getenv("SCREENSHOT_INTERVAL", "5.0"))  # seconds

# Browser Configuration
BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chrome")  # chrome, firefox, edge
HEADLESS_BROWSER = os.getenv("HEADLESS_BROWSER", "False").lower() in ("true", "1", "yes")
BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30"))  # seconds

# Risk Management Configuration
MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "0.02"))  # 2% of portfolio
MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "0.05"))  # 5% daily loss limit
STOP_LOSS_PERCENTAGE = float(os.getenv("STOP_LOSS_PERCENTAGE", "0.02"))  # 2% stop loss
TAKE_PROFIT_PERCENTAGE = float(os.getenv("TAKE_PROFIT_PERCENTAGE", "0.04"))  # 4% take profit

# Market Configuration
DEFAULT_MARKETS = os.getenv("DEFAULT_MARKETS", "crypto,stocks,commodities").split(",")
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "60"))  # seconds between scans

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", "logs/aegis_trader.log")
LOG_MAX_SIZE = int(os.getenv("LOG_MAX_SIZE", "10485760"))  # 10MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

# TTS Configuration
TTS_ENABLED = os.getenv("TTS_ENABLED", "True").lower() in ("true", "1", "yes")
TTS_VOICE_RATE = int(os.getenv("TTS_VOICE_RATE", "200"))  # words per minute

# Data Storage Configuration
DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
MODELS_DIR = Path(os.getenv("MODELS_DIR", "models"))
LOGS_DIR = Path(os.getenv("LOGS_DIR", "logs"))

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Validation
def validate_config() -> bool:
    """Validate configuration settings."""
    errors = []
    
    if LIVE_TRADING:
        if not BROKER_API_KEY:
            errors.append("BROKER_API_KEY is required for live trading")
        if not BROKER_API_SECRET:
            errors.append("BROKER_API_SECRET is required for live trading")
    
    if not (0 < MAX_POSITION_SIZE <= 1):
        errors.append("MAX_POSITION_SIZE must be between 0 and 1")
    
    if not (0 < MAX_DAILY_LOSS <= 1):
        errors.append("MAX_DAILY_LOSS must be between 0 and 1")
    
    if errors:
        for error in errors:
            logging.error(f"Configuration error: {error}")
        return False
    
    return True

# Configuration summary
def get_config_summary() -> dict:
    """Get a summary of current configuration (excluding sensitive data)."""
    return {
        "trading_mode": "LIVE" if LIVE_TRADING else "PAPER",
        "broker_sandbox": BROKER_SANDBOX,
        "browser_type": BROWSER_TYPE,
        "headless_browser": HEADLESS_BROWSER,
        "markets": DEFAULT_MARKETS,
        "max_position_size": MAX_POSITION_SIZE,
        "max_daily_loss": MAX_DAILY_LOSS,
        "tts_enabled": TTS_ENABLED,
        "log_level": LOG_LEVEL,
        "scan_interval": SCAN_INTERVAL,
    }

# Startup warning for live trading
def show_live_trading_warning() -> bool:
    """Show warning and get confirmation for live trading mode."""
    if not LIVE_TRADING:
        return True
    
    print("\n" + "="*60)
    print("⚠️  LIVE TRADING MODE ENABLED ⚠️")
    print("="*60)
    print("This will execute REAL trades with REAL money!")
    print("Make sure you understand the risks involved.")
    print(f"Broker Sandbox Mode: {'ON' if BROKER_SANDBOX else 'OFF'}")
    print("="*60)
    
    while True:
        response = input("Type 'I UNDERSTAND THE RISKS' to continue: ").strip()
        if response == "I UNDERSTAND THE RISKS":
            print("Live trading mode confirmed. Starting AegisTrader...")
            return True
        elif response.lower() in ['exit', 'quit', 'no', 'cancel']:
            print("Exiting AegisTrader.")
            return False
        else:
            print("Invalid response. Please type exactly 'I UNDERSTAND THE RISKS' or 'exit'")

if __name__ == "__main__":
    print("AegisTrader Configuration")
    print("=" * 30)
    
    config = get_config_summary()
    for key, value in config.items():
        print(f"{key}: {value}")
    
    print(f"\nConfiguration valid: {validate_config()}")
