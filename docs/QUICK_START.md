# 🚀 AegisTrader Quick Start Guide

Get AegisTrader running in under 10 minutes!

## ⚡ Super Quick Start (Docker)

**Prerequisites**: Docker and Docker Compose installed

```bash
# 1. Clone repository
git clone https://github.com/yourusername/aegistrader.git
cd aegistrader

# 2. Configure environment
cp .env.example .env
# Edit .env with your preferences (defaults work for paper trading)

# 3. Start with Docker
docker-compose up -d

# 4. Check logs
docker-compose logs -f aegistrader
```

That's it! AegisTrader is now running in paper trading mode.

## 🐍 Python Installation (5 minutes)

**Prerequisites**: Python 3.8+, Git

### Windows
```powershell
# 1. Clone and enter directory
git clone https://github.com/yourusername/aegistrader.git
cd aegistrader

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Tesseract OCR
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install to default location

# 5. Configure
copy .env.example .env
# Edit .env if needed

# 6. Create directories
mkdir data logs models screenshots

# 7. Run
python main.py
```

### macOS/Linux
```bash
# 1. Clone and enter directory
git clone https://github.com/yourusername/aegistrader.git
cd aegistrader

# 2. Install system dependencies
# macOS:
brew install python tesseract
# Ubuntu/Debian:
sudo apt install python3 python3-pip python3-venv tesseract-ocr

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure
cp .env.example .env
# Edit .env if needed

# 6. Create directories
mkdir -p data logs models screenshots

# 7. Run
python main.py
```

## ⚙️ Essential Configuration

Edit `.env` file for basic setup:

```env
# Trading mode (IMPORTANT: Keep false for testing!)
LIVE_TRADING=false

# Markets to trade
DEFAULT_MARKETS=crypto,stocks,commodities

# Browser settings
BROWSER_TYPE=chrome
HEADLESS_BROWSER=false  # Set true for servers

# Risk management
MAX_POSITION_SIZE=0.1    # 10% max position
MAX_DAILY_LOSS=0.05      # 5% max daily loss
STOP_LOSS_PERCENTAGE=0.02 # 2% stop loss

# Audio feedback
TTS_ENABLED=true

# Scanning
SCAN_INTERVAL=60  # Scan every 60 seconds
```

## 🎯 First Run Checklist

When you run `python main.py`, you should see:

✅ **Configuration validation passed**
✅ **All components initialized**
✅ **Market status displayed**
✅ **Trading loop started**
✅ **Browser opens TradingView** (if not headless)

### Expected Output
```
Starting AegisTrader...
============================================================
🛡️  AEGIS TRADER - Vision-Based Trading Bot
============================================================
Trading Mode: PAPER
Markets: crypto, stocks, commodities
Browser: chrome (visible)
Max Position Size: 10.0%
Max Daily Loss: 5.0%
TTS Enabled: True
Scan Interval: 60s
============================================================

📊 Market Status (2024-01-15 10:30:00 GMT)
----------------------------------------
CRYPTO: 🟢 OPEN
STOCKS: 🟢 OPEN
COMMODITIES: 🟢 OPEN

Initializing AegisTrader components...
🚀 Starting trading operations...
```

## 🔧 Common Issues & Quick Fixes

### Issue: "TesseractNotFoundError"
**Fix**: Install Tesseract OCR
- **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt install tesseract-ocr`

### Issue: "ChromeDriver not found"
**Fix**: Already handled automatically! The system downloads ChromeDriver automatically.

### Issue: Browser doesn't open
**Fix**: Check browser settings
```env
HEADLESS_BROWSER=false  # Make browser visible
BROWSER_TYPE=chrome     # Try different browser
```

### Issue: No trading signals
**Normal**: This is expected initially. The system needs to:
1. Scan markets (takes 1-2 minutes)
2. Find opportunities (may take 5-10 minutes)
3. Generate signals (depends on market conditions)

### Issue: Permission errors
**Fix**: Run with proper permissions
```bash
# Linux/macOS
chmod +x main.py
sudo chown -R $USER:$USER .

# Windows: Run PowerShell as Administrator
```

## 📊 Monitoring Your Bot

### Check Logs
```bash
# Main application log
tail -f logs/aegistrader.log

# Trade log
tail -f logs/trades.log

# Performance log
tail -f logs/performance.log
```

### View Screenshots
Screenshots are saved in `screenshots/` directory to see what the bot is analyzing.

### Check Performance
The bot displays performance summary on shutdown or you can check logs for real-time metrics.

## 🎮 Testing the System

### Test Individual Components
```bash
# Test YOLO detector
python -m vision.yolo_detector

# Test OCR reader
python -m vision.ocr_reader

# Test browser automation
python -m browser.selenium_controller

# Test configuration
python -c "from config import validate_config; print(validate_config())"
```

### Run Unit Tests
```bash
pip install pytest
pytest tests/
```

## 🔄 Next Steps

1. **Let it run for 30 minutes** to see how it performs
2. **Check the logs** to understand what it's doing
3. **Review screenshots** to see chart analysis
4. **Adjust configuration** based on your preferences
5. **Read the full documentation** for advanced features

### Recommended Reading Order
1. [Troubleshooting Guide](TROUBLESHOOTING.md) - If you encounter issues
2. [Strategy Guide](STRATEGY_GUIDE.md) - To understand trading strategies
3. [API Integration Guide](API_INTEGRATION.md) - To add real brokers
4. [Deployment Guide](DEPLOYMENT.md) - For production deployment

## ⚠️ Important Safety Notes

- **Always start with paper trading** (`LIVE_TRADING=false`)
- **Never risk more than you can afford to lose**
- **Test thoroughly before considering live trading**
- **Keep API keys secure** and never commit them to version control
- **Monitor the bot regularly** - it's not "set and forget"

## 🆘 Getting Help

If you're stuck:

1. **Check logs**: `tail -f logs/aegistrader.log`
2. **Enable debug mode**: Set `LOG_LEVEL=DEBUG` in `.env`
3. **Review troubleshooting guide**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
4. **Create GitHub issue**: Include logs and configuration (remove sensitive data)

## 🎉 Success!

If you see trading signals being generated and the bot is scanning markets, congratulations! You've successfully set up AegisTrader.

**Remember**: This is paper trading mode. No real money is at risk. Take time to understand how the system works before considering live trading.

---

**Next**: Read the [Strategy Guide](STRATEGY_GUIDE.md) to understand how the trading strategies work and how to create your own.
