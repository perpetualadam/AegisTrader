"""
Market session management for AegisTrader.
Handles UK timezone awareness, market hours, and holiday support.
"""

import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import pytz
import logging

logger = logging.getLogger(__name__)

class MarketType(Enum):
    """Market types supported by AegisTrader."""
    CRYPTO = "crypto"
    STOCKS = "stocks"
    COMMODITIES = "commodities"
    FOREX = "forex"

class MarketSession:
    """Manages market session times and availability."""
    
    def __init__(self):
        # UK timezone
        self.uk_tz = pytz.timezone('Europe/London')
        self.utc_tz = pytz.UTC
        
        # Market hours (in UK time)
        self.market_hours = {
            MarketType.STOCKS: {
                'open': datetime.time(8, 0),    # 08:00 UK time
                'close': datetime.time(16, 30), # 16:30 UK time
                'days': [0, 1, 2, 3, 4]        # Monday to Friday
            },
            MarketType.COMMODITIES: {
                'open': datetime.time(8, 0),    # 08:00 UK time
                'close': datetime.time(16, 30), # 16:30 UK time
                'days': [0, 1, 2, 3, 4]        # Monday to Friday
            },
            MarketType.CRYPTO: {
                'open': datetime.time(0, 0),    # 24/7
                'close': datetime.time(23, 59),
                'days': [0, 1, 2, 3, 4, 5, 6]  # All days
            },
            MarketType.FOREX: {
                'open': datetime.time(0, 0),    # 24/5
                'close': datetime.time(23, 59),
                'days': [0, 1, 2, 3, 4]        # Monday to Friday
            }
        }
        
        # UK market holidays (basic list - can be extended)
        self.uk_holidays_2024 = [
            datetime.date(2024, 1, 1),   # New Year's Day
            datetime.date(2024, 3, 29),  # Good Friday
            datetime.date(2024, 4, 1),   # Easter Monday
            datetime.date(2024, 5, 6),   # Early May Bank Holiday
            datetime.date(2024, 5, 27),  # Spring Bank Holiday
            datetime.date(2024, 8, 26),  # Summer Bank Holiday
            datetime.date(2024, 12, 25), # Christmas Day
            datetime.date(2024, 12, 26), # Boxing Day
        ]
        
        self.uk_holidays_2025 = [
            datetime.date(2025, 1, 1),   # New Year's Day
            datetime.date(2025, 4, 18),  # Good Friday
            datetime.date(2025, 4, 21),  # Easter Monday
            datetime.date(2025, 5, 5),   # Early May Bank Holiday
            datetime.date(2025, 5, 26),  # Spring Bank Holiday
            datetime.date(2025, 8, 25),  # Summer Bank Holiday
            datetime.date(2025, 12, 25), # Christmas Day
            datetime.date(2025, 12, 26), # Boxing Day
        ]
    
    def get_current_uk_time(self) -> datetime.datetime:
        """Get current time in UK timezone."""
        return datetime.datetime.now(self.uk_tz)
    
    def is_uk_holiday(self, date: datetime.date) -> bool:
        """Check if a given date is a UK market holiday."""
        if date.year == 2024:
            return date in self.uk_holidays_2024
        elif date.year == 2025:
            return date in self.uk_holidays_2025
        else:
            # For other years, only check major holidays
            return (date.month == 1 and date.day == 1) or \
                   (date.month == 12 and date.day in [25, 26])
    
    def is_market_open(self, market_type: MarketType, 
                      check_time: Optional[datetime.datetime] = None) -> bool:
        """
        Check if a specific market is currently open.
        
        Args:
            market_type: Type of market to check
            check_time: Time to check (defaults to current UK time)
        
        Returns:
            True if market is open, False otherwise
        """
        if check_time is None:
            check_time = self.get_current_uk_time()
        elif check_time.tzinfo is None:
            # Assume UTC if no timezone info
            check_time = self.utc_tz.localize(check_time).astimezone(self.uk_tz)
        elif check_time.tzinfo != self.uk_tz:
            # Convert to UK timezone
            check_time = check_time.astimezone(self.uk_tz)
        
        market_info = self.market_hours[market_type]
        
        # Check if it's a valid trading day
        if check_time.weekday() not in market_info['days']:
            return False
        
        # Check for holidays (only for traditional markets)
        if market_type in [MarketType.STOCKS, MarketType.COMMODITIES]:
            if self.is_uk_holiday(check_time.date()):
                return False
        
        # Check if within trading hours
        current_time = check_time.time()
        return market_info['open'] <= current_time <= market_info['close']
    
    def get_market_status(self) -> Dict[MarketType, bool]:
        """Get the current status of all markets."""
        current_time = self.get_current_uk_time()
        return {
            market_type: self.is_market_open(market_type, current_time)
            for market_type in MarketType
        }
    
    def get_next_market_open(self, market_type: MarketType) -> datetime.datetime:
        """Get the next time a market will open."""
        current_time = self.get_current_uk_time()
        market_info = self.market_hours[market_type]
        
        # Start checking from tomorrow if market is closed today
        check_date = current_time.date()
        if not self.is_market_open(market_type, current_time):
            check_date += datetime.timedelta(days=1)
        
        # Find next valid trading day
        for _ in range(7):  # Check up to a week ahead
            if check_date.weekday() in market_info['days']:
                if market_type not in [MarketType.STOCKS, MarketType.COMMODITIES] or \
                   not self.is_uk_holiday(check_date):
                    next_open = self.uk_tz.localize(
                        datetime.datetime.combine(check_date, market_info['open'])
                    )
                    return next_open
            check_date += datetime.timedelta(days=1)
        
        # Fallback - return a week from now
        return current_time + datetime.timedelta(days=7)
    
    def get_time_until_market_open(self, market_type: MarketType) -> datetime.timedelta:
        """Get time remaining until market opens."""
        if self.is_market_open(market_type):
            return datetime.timedelta(0)
        
        next_open = self.get_next_market_open(market_type)
        current_time = self.get_current_uk_time()
        return next_open - current_time
    
    def get_trading_session_info(self) -> Dict:
        """Get comprehensive trading session information."""
        current_time = self.get_current_uk_time()
        market_status = self.get_market_status()
        
        session_info = {
            'current_time_uk': current_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'current_time_utc': current_time.astimezone(self.utc_tz).strftime('%Y-%m-%d %H:%M:%S %Z'),
            'is_uk_holiday': self.is_uk_holiday(current_time.date()),
            'markets': {}
        }
        
        for market_type in MarketType:
            is_open = market_status[market_type]
            session_info['markets'][market_type.value] = {
                'is_open': is_open,
                'next_open': None if is_open else self.get_next_market_open(market_type).strftime('%Y-%m-%d %H:%M:%S %Z'),
                'time_until_open': None if is_open else str(self.get_time_until_market_open(market_type))
            }
        
        return session_info

# Global instance
market_session = MarketSession()

def get_active_markets() -> List[MarketType]:
    """Get list of currently active markets."""
    return [
        market_type for market_type, is_open 
        in market_session.get_market_status().items() 
        if is_open
    ]

def should_trade_market(market_type: MarketType) -> bool:
    """Determine if we should trade a specific market right now."""
    return market_session.is_market_open(market_type)

if __name__ == "__main__":
    # Test the market session functionality
    session = MarketSession()
    
    print("Market Session Information")
    print("=" * 40)
    
    info = session.get_trading_session_info()
    print(f"Current UK Time: {info['current_time_uk']}")
    print(f"Current UTC Time: {info['current_time_utc']}")
    print(f"UK Holiday: {info['is_uk_holiday']}")
    print()
    
    for market, details in info['markets'].items():
        print(f"{market.upper()}:")
        print(f"  Open: {details['is_open']}")
        if not details['is_open']:
            print(f"  Next Open: {details['next_open']}")
            print(f"  Time Until Open: {details['time_until_open']}")
        print()
