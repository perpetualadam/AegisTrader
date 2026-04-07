# 🛡️ AegisTrader - Vision-Based Trading Bot

A sophisticated Python trading bot that uses computer vision to analyze TradingView charts and execute trades across multiple markets (crypto, stocks, commodities).

## ⚠️ Important Disclaimer

**This software is for educational and research purposes only. Trading involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Use at your own risk.**

## 🚀 Features

- **Vision-Based Analysis**: Uses YOLO for chart pattern detection and OCR for price extraction
- **Multi-Market Support**: Crypto (24/7), UK stocks, and commodities with timezone awareness
- **Browser Automation**: Selenium-based TradingView chart navigation
- **Multiple Strategies**: Momentum, mean reversion, breakout, pattern recognition, multi-timeframe
- **Risk Management**: Position sizing, stop losses, daily loss limits
- **Live/Paper Trading**: Switch between simulation and live trading modes
- **TTS Feedback**: Audio notifications for trades and alerts
- **Comprehensive Logging**: Detailed trade and performance logging

## 📋 Requirements

- Python 3.8+
- Chrome/Firefox browser
- TradingView account (free tier works)
- Tesseract OCR (optional: EasyOCR, PaddleOCR)

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/aegistrader.git
cd aegistrader
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Tesseract OCR**:
   - **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

4. **Setup configuration**:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Create required directories**:
```bash
mkdir -p data logs models screenshots
```

## ⚙️ Configuration

Edit the `.env` file to configure your settings:

### Trading Mode
```env
# IMPORTANT: Only set to true for live trading with real money
LIVE_TRADING=false
```

### Broker Configuration
```env
BROKER_NAME=mock  # or binance, alpaca, etc.
BROKER_API_KEY=your_api_key
BROKER_API_SECRET=your_api_secret
```

### Risk Management
```env
MAX_POSITION_SIZE=0.1      # 10% max position size
MAX_DAILY_LOSS=0.05        # 5% max daily loss
STOP_LOSS_PERCENTAGE=0.02  # 2% stop loss
```

### Markets and Strategies
```env
DEFAULT_MARKETS=crypto,stocks,commodities
ENABLED_STRATEGIES=momentum,breakout,pattern_recognition
```

## 🏃‍♂️ Quick Start

**New to AegisTrader?** → **[📖 Quick Start Guide](docs/QUICK_START.md)** (5-minute setup!)

### Super Quick Start (Docker)
```bash
git clone https://github.com/yourusername/aegistrader.git
cd aegistrader
cp .env.example .env
docker-compose up -d
```

### Python Installation
1. **Paper Trading (Recommended)**:
```bash
python main.py
```

2. **Live Trading** (⚠️ Use with caution):
   - Set `LIVE_TRADING=true` in `.env`
   - Configure broker credentials
   - Run: `python main.py`

## 📊 Market Sessions

AegisTrader is timezone-aware and respects market hours:

- **Crypto**: 24/7 trading
- **UK Stocks**: 08:00-16:30 GMT/BST (LSE hours)
- **Commodities**: 08:00-16:30 GMT/BST
- **UK Holidays**: Automatically detected and respected

## 🧠 Trading Strategies

### 1. Momentum Strategy
- Identifies trending markets
- Enters positions in direction of momentum
- Uses moving averages and price velocity

### 2. Mean Reversion Strategy
- Identifies overbought/oversold conditions
- Enters counter-trend positions
- Uses RSI and Bollinger Bands concepts

### 3. Breakout Strategy
- Detects price breakouts from consolidation
- Enters positions on volume confirmation
- Uses support/resistance levels

### 4. Pattern Recognition
- Uses YOLO to detect chart patterns
- Recognizes triangles, head & shoulders, flags
- Combines with technical indicators

### 5. Multi-Timeframe Analysis
- Analyzes multiple timeframes
- Confirms signals across different periods
- Reduces false signals

## 🔍 Vision System

### YOLO Pattern Detection
- Detects chart patterns in screenshots
- Supports custom model training
- Fallback to YOLOv8n if custom model unavailable

### OCR Price Extraction
- Extracts prices, volumes, and percentages
- Supports multiple OCR engines
- Preprocessing for better accuracy

## 🛡️ Risk Management

- **Position Sizing**: Based on account balance and stop loss distance
- **Stop Losses**: Automatic stop loss placement
- **Daily Limits**: Maximum daily loss protection
- **Position Limits**: Maximum number of concurrent positions
- **Exposure Limits**: Maximum portfolio exposure

## 📈 Performance Tracking

- Real-time P&L tracking
- Win rate and drawdown metrics
- Trade history and analytics
- Performance logging and reporting

## 🔊 TTS Feedback

Audio notifications for:
- Trade executions
- Signal alerts
- Risk events
- System status changes

## 📁 Project Structure

```
aegistrader/
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── assets.py              # Asset definitions and management
├── market_sessions.py     # Market hours and timezone handling
├── vision/                # Computer vision modules
│   ├── yolo_detector.py   # YOLO pattern detection
│   └── ocr_reader.py      # OCR price extraction
├── browser/               # Browser automation
│   └── selenium_controller.py
├── scanner/               # Market scanning
│   └── market_scanner.py
├── strategy/              # Trading strategies
│   └── strategy_engine.py
├── execution/             # Trade execution
│   └── execution.py
├── broker/                # Broker API interfaces
│   └── broker_api.py
├── risk/                  # Risk management
│   └── risk_manager.py
├── utils/                 # Utilities
│   ├── logger.py          # Logging system
│   └── tts_feedback.py    # Text-to-speech
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── data/                  # Trading data storage
├── logs/                  # Log files
├── models/                # AI models
└── screenshots/           # Chart screenshots
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=. tests/
```

## 📝 Logging

Logs are stored in the `logs/` directory:
- `aegistrader.log`: Main application log
- `trades.log`: Trade execution log
- `performance.log`: Performance metrics log

## 🔧 Development

### Adding New Strategies
1. Implement strategy in `strategy/strategy_engine.py`
2. Add strategy type to `StrategyType` enum
3. Update configuration options

### Adding New Brokers
1. Implement broker API in `broker/broker_api.py`
2. Inherit from `BrokerAPI` base class
3. Update factory function

### Custom YOLO Models
1. Train custom model for chart patterns
2. Save model to `models/` directory
3. Update `YOLO_MODEL_PATH` in `.env`

## ⚠️ Safety Features

- **Paper Trading Default**: Starts in simulation mode
- **Live Trading Warnings**: Multiple confirmations required
- **Risk Limits**: Hard-coded maximum limits
- **Emergency Stop**: Graceful shutdown on signals
- **State Persistence**: Saves trading state on shutdown

## 📚 Documentation

### Core Documentation
- **[📖 Quick Start Guide](docs/QUICK_START.md)** - Get running in 5 minutes
- **[🔧 Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[🚀 Deployment Guide](docs/DEPLOYMENT.md)** - Local and cloud deployment instructions
- **[🔗 API Integration Guide](docs/API_INTEGRATION.md)** - Broker API setup and integration
- **[🧠 Strategy Development Guide](docs/STRATEGY_GUIDE.md)** - Creating custom trading strategies

### Quick Links
- [Installation Issues](docs/TROUBLESHOOTING.md#installation-issues) - Python, OCR, browser setup
- [Docker Deployment](docs/DEPLOYMENT.md#docker-deployment) - Containerized deployment
- [Adding New Brokers](docs/API_INTEGRATION.md#adding-new-brokers) - Broker integration
- [Custom Strategies](docs/STRATEGY_GUIDE.md#creating-custom-strategies) - Strategy development
- [Backtesting](docs/STRATEGY_GUIDE.md#backtesting-framework) - Strategy testing

## 📞 Support

For issues and questions:
1. **Check Documentation**: Review relevant guides above
2. **Check Logs**: Examine files in `logs/` directory
3. **Verify Configuration**: Review settings in `.env`
4. **Test Paper Trading**: Always test in simulation mode first
5. **Create GitHub Issue**: Include logs, config (remove sensitive data), and steps to reproduce

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚖️ Legal Notice

This software is provided "as is" without warranty. Users are responsible for compliance with applicable laws and regulations. The authors are not responsible for any financial losses incurred through the use of this software.

---

**Remember: Never risk more than you can afford to lose. Always test thoroughly in paper trading mode before considering live trading.**
