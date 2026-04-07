"""
Selenium-based browser automation for AegisTrader.
Handles automatic TradingView chart switching and navigation.
"""

import time
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import json

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

from config import (
    BROWSER_TYPE, HEADLESS_BROWSER, BROWSER_TIMEOUT,
    TRADINGVIEW_USERNAME, TRADINGVIEW_PASSWORD
)

logger = logging.getLogger(__name__)

@dataclass
class ChartConfig:
    """Configuration for a TradingView chart."""
    symbol: str
    timeframe: str = "1h"
    indicators: List[str] = None
    layout: str = "standard"
    theme: str = "dark"

class SeleniumController:
    """Selenium-based controller for browser automation."""
    
    def __init__(self, browser_type: str = None, headless: bool = None):
        self.browser_type = browser_type or BROWSER_TYPE
        self.headless = headless if headless is not None else HEADLESS_BROWSER
        self.driver = None
        self.wait = None
        self.is_initialized = False
        self.current_symbol = None
        
        # TradingView URLs and selectors
        self.tradingview_base_url = "https://www.tradingview.com"
        self.chart_url = f"{self.tradingview_base_url}/chart/"
        
        # Common selectors (may need updates based on TradingView changes)
        self.selectors = {
            'symbol_search': '[data-name="symbol-search-input"]',
            'symbol_input': 'input[data-role="search"]',
            'symbol_result': '[data-role="search-result"]',
            'timeframe_button': '[data-name="timeframe-button"]',
            'chart_container': '#chart-container',
            'login_button': '[data-name="header-user-menu-sign-in"]',
            'username_input': '[name="username"]',
            'password_input': '[name="password"]',
            'login_submit': '[type="submit"]',
            'chart_screenshot_area': '.chart-container',
            'price_display': '.js-symbol-last',
            'change_display': '.js-symbol-change',
            'volume_display': '.js-symbol-volume'
        }
        
        self.initialize_driver()
    
    def initialize_driver(self) -> bool:
        """Initialize the Selenium WebDriver."""
        if not SELENIUM_AVAILABLE:
            logger.error("Selenium not available. Cannot initialize browser controller.")
            return False
        
        try:
            options = self._get_browser_options()
            
            if self.browser_type.lower() == 'chrome':
                self.driver = webdriver.Chrome(options=options)
            elif self.browser_type.lower() == 'firefox':
                self.driver = webdriver.Firefox(options=options)
            elif self.browser_type.lower() == 'edge':
                self.driver = webdriver.Edge(options=options)
            else:
                logger.error(f"Unsupported browser type: {self.browser_type}")
                return False
            
            self.driver.set_window_size(1920, 1080)
            self.wait = WebDriverWait(self.driver, BROWSER_TIMEOUT)
            self.is_initialized = True
            
            logger.info(f"Browser controller initialized with {self.browser_type}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            return False
    
    def _get_browser_options(self):
        """Get browser-specific options."""
        if self.browser_type.lower() == 'chrome':
            from selenium.webdriver.chrome.options import Options
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
        elif self.browser_type.lower() == 'firefox':
            from selenium.webdriver.firefox.options import Options
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--width=1920')
            options.add_argument('--height=1080')
            
        elif self.browser_type.lower() == 'edge':
            from selenium.webdriver.edge.options import Options
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--window-size=1920,1080')
        
        return options
    
    def navigate_to_tradingview(self) -> bool:
        """Navigate to TradingView main page."""
        try:
            self.driver.get(self.tradingview_base_url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            logger.info("Navigated to TradingView")
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to TradingView: {e}")
            return False
    
    def login_to_tradingview(self, username: str = None, password: str = None) -> bool:
        """Login to TradingView account."""
        username = username or TRADINGVIEW_USERNAME
        password = password or TRADINGVIEW_PASSWORD
        
        if not username or not password:
            logger.warning("TradingView credentials not provided. Continuing without login.")
            return True
        
        try:
            # Click login button
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.selectors['login_button']))
            )
            login_btn.click()
            
            # Enter credentials
            username_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors['username_input']))
            )
            username_field.send_keys(username)
            
            password_field = self.driver.find_element(By.CSS_SELECTOR, self.selectors['password_input'])
            password_field.send_keys(password)
            
            # Submit login
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, self.selectors['login_submit'])
            submit_btn.click()
            
            # Wait for login to complete
            time.sleep(3)
            logger.info("Logged in to TradingView")
            return True
            
        except Exception as e:
            logger.error(f"Failed to login to TradingView: {e}")
            return False
    
    def open_chart(self, symbol: str, timeframe: str = "1h") -> bool:
        """
        Open a specific chart on TradingView.
        
        Args:
            symbol: Trading symbol (e.g., "BINANCE:BTCUSDT")
            timeframe: Chart timeframe (e.g., "1h", "4h", "1D")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Navigate to chart with symbol
            chart_url = f"{self.chart_url}?symbol={symbol}&interval={timeframe}"
            self.driver.get(chart_url)
            
            # Wait for chart to load
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors['chart_container']))
            )
            
            # Additional wait for chart data to load
            time.sleep(5)
            
            self.current_symbol = symbol
            logger.info(f"Opened chart for {symbol} on {timeframe} timeframe")
            return True
            
        except Exception as e:
            logger.error(f"Failed to open chart for {symbol}: {e}")
            return False
    
    def switch_symbol(self, symbol: str) -> bool:
        """Switch to a different trading symbol."""
        try:
            # Click on symbol search
            search_element = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.selectors['symbol_search']))
            )
            search_element.click()
            
            # Clear and enter new symbol
            search_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors['symbol_input']))
            )
            search_input.clear()
            search_input.send_keys(symbol)
            
            # Wait for search results and click first result
            time.sleep(2)
            search_input.send_keys(Keys.ENTER)
            
            # Wait for chart to update
            time.sleep(3)
            
            self.current_symbol = symbol
            logger.info(f"Switched to symbol: {symbol}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to switch to symbol {symbol}: {e}")
            return False
    
    def change_timeframe(self, timeframe: str) -> bool:
        """Change chart timeframe."""
        try:
            # Click timeframe button
            timeframe_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.selectors['timeframe_button']))
            )
            timeframe_btn.click()
            
            # Select specific timeframe (this may need adjustment based on UI)
            timeframe_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//div[text()='{timeframe}']"))
            )
            timeframe_option.click()
            
            # Wait for chart to update
            time.sleep(3)
            
            logger.info(f"Changed timeframe to: {timeframe}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to change timeframe to {timeframe}: {e}")
            return False
    
    def take_screenshot(self, filename: str = None) -> Optional[str]:
        """Take a screenshot of the current chart."""
        try:
            if filename is None:
                timestamp = int(time.time())
                filename = f"chart_screenshot_{timestamp}.png"
            
            # Ensure screenshots directory exists
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            
            filepath = screenshots_dir / filename
            
            # Take full page screenshot
            self.driver.save_screenshot(str(filepath))
            
            logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None
    
    def get_chart_element_screenshot(self, filename: str = None) -> Optional[str]:
        """Take a screenshot of just the chart area."""
        try:
            chart_element = self.driver.find_element(By.CSS_SELECTOR, self.selectors['chart_container'])
            
            if filename is None:
                timestamp = int(time.time())
                filename = f"chart_element_{timestamp}.png"
            
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            filepath = screenshots_dir / filename
            
            chart_element.screenshot(str(filepath))
            
            logger.info(f"Chart element screenshot saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to take chart element screenshot: {e}")
            return None
    
    def scan_multiple_symbols(self, symbols: List[str], timeframe: str = "1h", 
                            screenshot_each: bool = True) -> Dict[str, Optional[str]]:
        """
        Scan multiple symbols and optionally take screenshots.
        
        Args:
            symbols: List of symbols to scan
            timeframe: Timeframe for all charts
            screenshot_each: Whether to take screenshots of each chart
            
        Returns:
            Dictionary mapping symbols to screenshot paths
        """
        results = {}
        
        for symbol in symbols:
            logger.info(f"Scanning symbol: {symbol}")
            
            if self.switch_symbol(symbol):
                if screenshot_each:
                    screenshot_path = self.take_screenshot(f"{symbol.replace(':', '_')}_{timeframe}.png")
                    results[symbol] = screenshot_path
                else:
                    results[symbol] = "success"
                
                # Small delay between symbols
                time.sleep(2)
            else:
                results[symbol] = None
                logger.warning(f"Failed to scan symbol: {symbol}")
        
        return results
    
    def close(self):
        """Close the browser and clean up."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
            finally:
                self.driver = None
                self.is_initialized = False

# Global controller instance
selenium_controller = None

def get_selenium_controller() -> Optional[SeleniumController]:
    """Get the global Selenium controller instance."""
    global selenium_controller
    if selenium_controller is None:
        selenium_controller = SeleniumController()
    return selenium_controller if selenium_controller.is_initialized else None

if __name__ == "__main__":
    # Test the Selenium controller
    controller = SeleniumController()
    
    if controller.is_initialized:
        print(f"Selenium controller initialized with {controller.browser_type}")
        print(f"Headless mode: {controller.headless}")
        
        # Test navigation
        if controller.navigate_to_tradingview():
            print("Successfully navigated to TradingView")
            
            # Test opening a chart
            if controller.open_chart("BINANCE:BTCUSDT"):
                print("Successfully opened BTC chart")
                
                # Take a test screenshot
                screenshot_path = controller.take_screenshot("test_screenshot.png")
                if screenshot_path:
                    print(f"Test screenshot saved: {screenshot_path}")
        
        controller.close()
    else:
        print("Failed to initialize Selenium controller")
