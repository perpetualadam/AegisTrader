# 🔧 AegisTrader Troubleshooting Guide

This guide covers common issues and their solutions when running AegisTrader.

## 📋 Table of Contents

- [Installation Issues](#installation-issues)
- [Vision System Problems](#vision-system-problems)
- [Browser Automation Errors](#browser-automation-errors)
- [Trading Execution Issues](#trading-execution-issues)
- [Configuration Problems](#configuration-problems)
- [Performance Issues](#performance-issues)
- [Log File Interpretation](#log-file-interpretation)
- [Debug Mode](#debug-mode)

## 🛠️ Installation Issues

### Python Dependencies

**Problem**: `pip install -r requirements.txt` fails
```bash
ERROR: Could not find a version that satisfies the requirement...
```

**Solutions**:
1. **Update pip**: `python -m pip install --upgrade pip`
2. **Use Python 3.8+**: Check version with `python --version`
3. **Create virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
4. **Install dependencies individually** if bulk install fails

### Tesseract OCR Installation

**Problem**: `TesseractNotFoundError` or OCR not working

**Windows Solutions**:
1. Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install to default location: `C:\Program Files\Tesseract-OCR\`
3. Add to PATH or set environment variable:
   ```bash
   set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

**macOS Solutions**:
```bash
brew install tesseract
# If brew not available
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Linux Solutions**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr

# CentOS/RHEL
sudo yum install tesseract
```

### Browser Driver Issues

**Problem**: `WebDriverException: 'chromedriver' executable needs to be in PATH`

**Solutions**:
1. **Automatic driver management** (recommended):
   ```python
   # Already implemented in selenium_controller.py
   from webdriver_manager.chrome import ChromeDriverManager
   ```

2. **Manual driver installation**:
   - Download ChromeDriver from [official site](https://chromedriver.chromium.org/)
   - Place in PATH or project directory
   - Ensure version matches your Chrome browser

3. **Alternative browsers**:
   ```env
   # In .env file
   BROWSER_TYPE=firefox  # or edge
   ```

### YOLO/Ultralytics Issues

**Problem**: `ModuleNotFoundError: No module named 'ultralytics'`

**Solutions**:
1. **Install ultralytics**:
   ```bash
   pip install ultralytics
   ```

2. **GPU support** (optional):
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

3. **Model download issues**:
   - Check internet connection
   - Clear cache: `rm -rf ~/.cache/torch/hub/ultralytics_yolov8*`

## 👁️ Vision System Problems

### YOLO Model Loading

**Problem**: Custom YOLO model fails to load

**Diagnostic Steps**:
1. Check model file exists:
   ```python
   import os
   print(os.path.exists("models/custom_chart_patterns.pt"))
   ```

2. **Verify model format**:
   - Must be `.pt` file
   - Compatible with ultralytics YOLO

**Solutions**:
1. **Use default model**:
   ```env
   # Comment out or remove from .env
   # YOLO_MODEL_PATH=models/custom_chart_patterns.pt
   ```

2. **Download pre-trained model**:
   ```python
   from ultralytics import YOLO
   model = YOLO('yolov8n.pt')  # Downloads automatically
   ```

### OCR Failures

**Problem**: OCR returns empty results or low confidence

**Diagnostic Steps**:
1. **Test OCR engines**:
   ```python
   from vision.ocr_reader import OCRReader
   reader = OCRReader(engine='tesseract')
   # Try different engines: 'easyocr', 'paddleocr'
   ```

2. **Check image quality**:
   - Screenshots should be clear and high contrast
   - Text should be readable by human eye

**Solutions**:
1. **Adjust OCR confidence threshold**:
   ```env
   OCR_CONFIDENCE_THRESHOLD=0.5  # Lower threshold
   ```

2. **Try different OCR engines**:
   ```env
   OCR_ENGINE=easyocr  # or paddleocr
   ```

3. **Improve image preprocessing**:
   - Increase screenshot resolution
   - Adjust contrast/brightness settings

### Screenshot Issues

**Problem**: Screenshots are blank or corrupted

**Solutions**:
1. **Check browser visibility**:
   ```env
   HEADLESS_BROWSER=false  # Make browser visible
   ```

2. **Increase wait times**:
   ```env
   BROWSER_TIMEOUT=60  # Increase timeout
   ```

3. **Verify TradingView access**:
   - Test manually opening TradingView URLs
   - Check for CAPTCHA or login requirements

## 🌐 Browser Automation Errors

### Selenium WebDriver Issues

**Problem**: `SessionNotCreatedException` or browser crashes

**Solutions**:
1. **Update browser and driver**:
   - Chrome: Help → About Google Chrome
   - Download matching ChromeDriver version

2. **Browser options troubleshooting**:
   ```python
   # Add to selenium_controller.py for debugging
   options.add_argument("--disable-dev-shm-usage")
   options.add_argument("--disable-gpu")
   options.add_argument("--no-sandbox")
   ```

3. **Memory issues**:
   ```python
   options.add_argument("--memory-pressure-off")
   options.add_argument("--max_old_space_size=4096")
   ```

### TradingView Connection Problems

**Problem**: Cannot load TradingView charts

**Diagnostic Steps**:
1. **Test URL manually**:
   ```
   https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval=1h
   ```

2. **Check network connectivity**:
   ```bash
   ping tradingview.com
   ```

**Solutions**:
1. **Handle rate limiting**:
   ```env
   SCAN_INTERVAL=120  # Increase interval
   ```

2. **Use different TradingView domains**:
   - Try `www.tradingview.com`
   - Try `uk.tradingview.com`

3. **Proxy configuration** (if behind firewall):
   ```python
   # Add to selenium options
   options.add_argument("--proxy-server=http://proxy:port")
   ```

## ⚡ Trading Execution Issues

### Broker API Errors

**Problem**: `ConnectionError` or `AuthenticationError`

**Diagnostic Steps**:
1. **Test API credentials**:
   ```python
   from broker.broker_api import create_broker_api
   broker = create_broker_api('mock', 'test', 'test')
   print(broker.connect())
   ```

2. **Check API status**:
   - Binance: https://status.binance.com/
   - Alpaca: https://status.alpaca.markets/

**Solutions**:
1. **Verify credentials**:
   ```env
   BROKER_API_KEY=your_actual_key
   BROKER_API_SECRET=your_actual_secret
   ```

2. **Use sandbox mode**:
   ```env
   BROKER_SANDBOX=true
   LIVE_TRADING=false
   ```

3. **Check IP whitelist** (for some brokers)

### Order Placement Failures

**Problem**: Orders rejected or fail to execute

**Solutions**:
1. **Check account balance**:
   ```python
   broker = get_broker_api()
   print(broker.get_balance())
   ```

2. **Verify market hours**:
   ```python
   from market_sessions import get_active_markets
   print(get_active_markets())
   ```

3. **Adjust position sizes**:
   ```env
   MAX_POSITION_SIZE=0.05  # Reduce position size
   ```

## ⚙️ Configuration Problems

### Environment Variables

**Problem**: Settings not loading from `.env` file

**Solutions**:
1. **Check file location**:
   ```bash
   ls -la .env  # Should be in project root
   ```

2. **Verify file format**:
   ```env
   # Correct format (no spaces around =)
   LIVE_TRADING=false
   
   # Incorrect format
   LIVE_TRADING = false
   ```

3. **Test configuration loading**:
   ```python
   from config import get_config_summary
   print(get_config_summary())
   ```

### Invalid Settings

**Problem**: `ConfigurationError` on startup

**Solutions**:
1. **Run configuration validation**:
   ```python
   from config import validate_config
   print(validate_config())
   ```

2. **Reset to defaults**:
   ```bash
   cp .env.example .env
   # Edit with your specific settings
   ```

## 🚀 Performance Issues

### Slow Scanning

**Problem**: Market scanning takes too long

**Solutions**:
1. **Reduce asset count**:
   ```python
   # In assets.py, comment out unused assets
   ```

2. **Increase scan interval**:
   ```env
   SCAN_INTERVAL=300  # 5 minutes instead of 1
   ```

3. **Optimize browser settings**:
   ```env
   HEADLESS_BROWSER=true
   MAX_BROWSER_INSTANCES=1
   ```

### Memory Usage

**Problem**: High memory consumption

**Solutions**:
1. **Enable headless mode**:
   ```env
   HEADLESS_BROWSER=true
   ```

2. **Limit concurrent operations**:
   ```env
   MAX_BROWSER_INSTANCES=2
   ```

3. **Clear browser cache periodically**:
   ```python
   # Implemented in selenium_controller.py
   driver.delete_all_cookies()
   ```

### CPU Optimization

**Problem**: High CPU usage

**Solutions**:
1. **Reduce image processing**:
   ```env
   SCREENSHOT_QUALITY=70  # Lower quality
   ```

2. **Optimize YOLO inference**:
   ```python
   # Use smaller model
   model = YOLO('yolov8n.pt')  # nano version
   ```

## 📝 Log File Interpretation

### Log Locations
```
logs/
├── aegistrader.log      # Main application log
├── trades.log           # Trade execution log
└── performance.log      # Performance metrics
```

### Common Log Messages

**INFO Messages** (Normal operation):
```
2024-01-15 10:30:00 - AegisTrader - INFO - Market scanner initialized
2024-01-15 10:30:05 - AegisTrader - INFO - Found 3 trading opportunities
```

**WARNING Messages** (Attention needed):
```
2024-01-15 10:30:10 - AegisTrader - WARNING - Signal rejected by risk manager
2024-01-15 10:30:15 - AegisTrader - WARNING - OCR confidence below threshold
```

**ERROR Messages** (Problems):
```
2024-01-15 10:30:20 - AegisTrader - ERROR - Failed to connect to broker API
2024-01-15 10:30:25 - AegisTrader - ERROR - Screenshot capture failed
```

### Debug Log Analysis

**Enable debug logging**:
```env
LOG_LEVEL=DEBUG
```

**Key debug patterns**:
- `Browser automation:` - Selenium operations
- `Vision processing:` - YOLO/OCR operations
- `Strategy analysis:` - Trading signal generation
- `Risk validation:` - Risk management decisions

## 🐛 Debug Mode

### Enable Debug Features

1. **Environment settings**:
   ```env
   DEBUG_MODE=true
   SAVE_DEBUG_SCREENSHOTS=true
   LOG_LEVEL=DEBUG
   ```

2. **Manual debugging**:
   ```python
   # Run individual components
   python -m vision.yolo_detector
   python -m vision.ocr_reader
   python -m browser.selenium_controller
   ```

### Debug Output Locations
```
screenshots/debug/       # Debug screenshots
logs/debug/             # Detailed debug logs
data/debug/             # Debug data files
```

### Common Debug Commands

```bash
# Test OCR
python -c "from vision.ocr_reader import OCRReader; r=OCRReader(); print(r.engine)"

# Test YOLO
python -c "from vision.yolo_detector import YOLODetector; d=YOLODetector(); print('YOLO OK')"

# Test browser
python -c "from browser.selenium_controller import SeleniumController; s=SeleniumController(); print(s.connect())"

# Test configuration
python -c "from config import validate_config; print(validate_config())"
```

## 🆘 Getting Help

If you're still experiencing issues:

1. **Check logs** in `logs/` directory
2. **Enable debug mode** for detailed output
3. **Test individual components** using debug commands
4. **Create GitHub issue** with:
   - Error messages from logs
   - System information (OS, Python version)
   - Configuration settings (remove sensitive data)
   - Steps to reproduce the issue

## 📞 Emergency Procedures

### Safe Shutdown
```bash
# Graceful shutdown
Ctrl+C  # Send interrupt signal

# Force shutdown if needed
Ctrl+Break  # Windows
Ctrl+Z      # Unix/Linux
```

### Reset to Factory Settings
```bash
# Backup current settings
cp .env .env.backup

# Reset configuration
cp .env.example .env

# Clear data and logs
rm -rf data/* logs/*

# Restart with clean state
python main.py
```
