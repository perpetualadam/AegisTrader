"""
Logging system for AegisTrader.
Comprehensive trade logging and system monitoring.
"""

import logging
import logging.handlers
import json
import time
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from config import LOG_LEVEL, LOG_FILE, LOG_MAX_SIZE, LOG_BACKUP_COUNT, LOGS_DIR

class TradeLogger:
    """Specialized logger for trading activities."""
    
    def __init__(self):
        self.setup_logging()
        self.trade_log_file = LOGS_DIR / "trades.log"
        self.performance_log_file = LOGS_DIR / "performance.log"
        
    def setup_logging(self):
        """Setup logging configuration."""
        # Create logs directory
        LOGS_DIR.mkdir(exist_ok=True)
        
        # Main logger
        self.logger = logging.getLogger('AegisTrader')
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=LOG_MAX_SIZE,
            backupCount=LOG_BACKUP_COUNT
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOG_LEVEL))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info("Logging system initialized")
    
    def log_trade(self, trade_data: Dict[str, Any]):
        """Log a completed trade."""
        trade_entry = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'type': 'TRADE',
            'data': trade_data
        }
        
        with open(self.trade_log_file, 'a') as f:
            f.write(json.dumps(trade_entry) + '\n')
        
        self.logger.info(f"Trade logged: {trade_data.get('symbol')} "
                        f"PnL: {trade_data.get('pnl', 0):.2f}")
    
    def log_signal(self, signal_data: Dict[str, Any]):
        """Log a trading signal."""
        self.logger.info(f"Signal: {signal_data.get('action')} "
                        f"{signal_data.get('symbol')} "
                        f"Confidence: {signal_data.get('confidence', 0):.2f}")
    
    def log_performance(self, performance_data: Dict[str, Any]):
        """Log performance metrics."""
        perf_entry = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'type': 'PERFORMANCE',
            'data': performance_data
        }
        
        with open(self.performance_log_file, 'a') as f:
            f.write(json.dumps(perf_entry) + '\n')
    
    def log_error(self, error_msg: str, context: Optional[Dict] = None):
        """Log an error with context."""
        error_data = {
            'error': error_msg,
            'context': context or {},
            'timestamp': time.time()
        }
        self.logger.error(f"Error: {error_msg} Context: {context}")
    
    def log_risk_event(self, event_type: str, description: str, severity: str = "info"):
        """Log a risk management event."""
        if severity == "warning":
            self.logger.warning(f"Risk {event_type}: {description}")
        elif severity == "error":
            self.logger.error(f"Risk {event_type}: {description}")
        else:
            self.logger.info(f"Risk {event_type}: {description}")

# Global logger instance
trade_logger = None

def get_logger() -> TradeLogger:
    """Get the global trade logger instance."""
    global trade_logger
    if trade_logger is None:
        trade_logger = TradeLogger()
    return trade_logger

class Logger:
    """Main logger class for backward compatibility."""
    
    def __init__(self):
        self.trade_logger = get_logger()
    
    def info(self, message: str):
        self.trade_logger.logger.info(message)
    
    def warning(self, message: str):
        self.trade_logger.logger.warning(message)
    
    def error(self, message: str):
        self.trade_logger.logger.error(message)
    
    def debug(self, message: str):
        self.trade_logger.logger.debug(message)

if __name__ == "__main__":
    # Test logging
    logger = get_logger()
    
    print("Testing AegisTrader Logging System")
    logger.logger.info("Test info message")
    logger.logger.warning("Test warning message")
    logger.logger.error("Test error message")
    
    # Test trade logging
    test_trade = {
        'symbol': 'BTCUSDT',
        'side': 'buy',
        'quantity': 0.1,
        'entry_price': 50000,
        'exit_price': 51000,
        'pnl': 100.0
    }
    logger.log_trade(test_trade)
    
    print("Logging test completed")
