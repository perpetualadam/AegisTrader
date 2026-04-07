"""
Risk management system for AegisTrader.
Position sizing, stop losses, and risk controls.
"""

import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

from config import (
    MAX_POSITION_SIZE,
    MAX_DAILY_LOSS,
    STOP_LOSS_PERCENTAGE,
    TAKE_PROFIT_PERCENTAGE,
    RISK_APPLY_FRICTION,
    RISK_FRICTION_BPS,
)
from assets import Asset
from strategy.strategy_engine import TradingSignal

logger = logging.getLogger(__name__)

@dataclass
class RiskMetrics:
    """Risk metrics for portfolio."""
    total_exposure: float
    max_position_risk: float
    daily_pnl: float
    max_drawdown: float
    var_95: float  # Value at Risk 95%
    sharpe_ratio: float
    risk_score: float  # Overall risk score 0-1

class RiskManager:
    """Risk management system."""
    
    def __init__(self):
        self.max_position_size = MAX_POSITION_SIZE
        self.max_daily_loss = MAX_DAILY_LOSS
        self.stop_loss_pct = STOP_LOSS_PERCENTAGE
        self.take_profit_pct = TAKE_PROFIT_PERCENTAGE
        
        # Risk tracking
        self.daily_pnl = 0.0
        self.daily_start_balance = 0.0
        self.max_drawdown = 0.0
        self.peak_balance = 0.0
        
        # Position limits
        self.max_positions = 5
        self.max_correlation = 0.7
        
        # Risk events log
        self.risk_events: List[Dict] = []
    
    def validate_signal(self, signal: TradingSignal, account_balance: float, 
                       current_positions: Dict) -> Dict[str, Any]:
        """
        Validate a trading signal against risk parameters.
        
        Returns:
            Dictionary with validation result and risk assessment
        """
        validation = {
            'approved': False,
            'risk_score': 0.0,
            'warnings': [],
            'position_size': 0.0,
            'stop_loss': None,
            'take_profit': None
        }
        
        try:
            # Check position limits
            if len(current_positions) >= self.max_positions:
                validation['warnings'].append("Maximum positions reached")
                return validation
            
            # Check if already have position in this asset
            if signal.asset.symbol in current_positions:
                validation['warnings'].append(f"Already have position in {signal.asset.symbol}")
                return validation
            
            # Calculate position size
            position_size = self._calculate_position_size(signal, account_balance)
            if position_size <= 0:
                validation['warnings'].append("Invalid position size calculated")
                return validation
            
            # Check daily loss limit
            if self._check_daily_loss_limit(account_balance):
                validation['warnings'].append("Daily loss limit reached")
                return validation
            
            # Calculate stop loss and take profit
            stop_loss, take_profit = self._calculate_risk_levels(signal)
            
            # Calculate risk score
            risk_score = self._calculate_risk_score(signal, position_size, account_balance)
            
            # Final approval
            if risk_score <= 0.8:  # Risk score threshold
                validation.update({
                    'approved': True,
                    'risk_score': risk_score,
                    'position_size': position_size,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                })
            else:
                validation['warnings'].append(f"Risk score too high: {risk_score:.2f}")
            
        except Exception as e:
            logger.error(f"Error validating signal: {e}")
            validation['warnings'].append(f"Validation error: {str(e)}")
        
        return validation
    
    def _calculate_position_size(self, signal: TradingSignal, account_balance: float) -> float:
        """Calculate position size based on risk management rules."""
        if not signal.entry_price or not signal.stop_loss:
            return 0.0
        
        # Risk amount (2% of balance)
        risk_amount = account_balance * 0.02
        
        # Price risk per unit (widen by fees/spread/slippage when RISK_APPLY_FRICTION)
        price_risk = abs(signal.entry_price - signal.stop_loss)
        if RISK_APPLY_FRICTION and signal.entry_price and RISK_FRICTION_BPS > 0:
            friction = signal.entry_price * (RISK_FRICTION_BPS / 10000.0)
            price_risk += friction
        if price_risk <= 0:
            return 0.0
        
        # Position size based on risk
        risk_based_size = risk_amount / price_risk
        
        # Maximum position size (% of balance)
        max_position_value = account_balance * self.max_position_size
        max_size = max_position_value / signal.entry_price
        
        # Return smaller of the two
        return min(risk_based_size, max_size)
    
    def _calculate_risk_levels(self, signal: TradingSignal) -> tuple:
        """Calculate stop loss and take profit levels."""
        if not signal.entry_price:
            return None, None
        
        entry_price = signal.entry_price
        
        if signal.signal_type.value in ['buy', 'strong_buy']:
            stop_loss = entry_price * (1 - self.stop_loss_pct)
            take_profit = entry_price * (1 + self.take_profit_pct)
        else:  # sell signals
            stop_loss = entry_price * (1 + self.stop_loss_pct)
            take_profit = entry_price * (1 - self.take_profit_pct)
        
        return stop_loss, take_profit
    
    def _calculate_risk_score(self, signal: TradingSignal, position_size: float, 
                            account_balance: float) -> float:
        """Calculate overall risk score for the signal."""
        risk_factors = []
        
        # Confidence factor (lower confidence = higher risk)
        confidence_risk = 1.0 - signal.confidence
        risk_factors.append(confidence_risk * 0.3)
        
        # Position size factor
        position_value = position_size * signal.entry_price
        size_risk = (position_value / account_balance) / self.max_position_size
        risk_factors.append(size_risk * 0.2)
        
        # Market type factor
        market_risk = {
            'crypto': 0.8,
            'stocks': 0.4,
            'commodities': 0.5,
            'forex': 0.6
        }.get(signal.asset.market_type.value, 0.5)
        risk_factors.append(market_risk * 0.2)
        
        # Volatility factor (simplified)
        volatility_risk = 0.5  # Would be calculated from historical data
        risk_factors.append(volatility_risk * 0.3)
        
        return sum(risk_factors)
    
    def _check_daily_loss_limit(self, account_balance: float) -> bool:
        """Check if daily loss limit has been reached."""
        if self.daily_start_balance == 0:
            self.daily_start_balance = account_balance
        
        daily_loss = (self.daily_start_balance - account_balance) / self.daily_start_balance
        return daily_loss >= self.max_daily_loss
    
    def update_daily_pnl(self, current_balance: float):
        """Update daily P&L tracking."""
        if self.daily_start_balance == 0:
            self.daily_start_balance = current_balance
        
        self.daily_pnl = current_balance - self.daily_start_balance
        
        # Update drawdown
        if current_balance > self.peak_balance:
            self.peak_balance = current_balance
        
        if self.peak_balance > 0:
            drawdown = (self.peak_balance - current_balance) / self.peak_balance
            self.max_drawdown = max(self.max_drawdown, drawdown)
    
    def reset_daily_metrics(self):
        """Reset daily metrics (call at start of new trading day)."""
        self.daily_pnl = 0.0
        self.daily_start_balance = 0.0
    
    def log_risk_event(self, event_type: str, description: str, severity: str = "info"):
        """Log a risk management event."""
        event = {
            'timestamp': time.time(),
            'type': event_type,
            'description': description,
            'severity': severity
        }
        self.risk_events.append(event)
        
        if severity == "warning":
            logger.warning(f"Risk event: {description}")
        elif severity == "error":
            logger.error(f"Risk event: {description}")
        else:
            logger.info(f"Risk event: {description}")
    
    def get_risk_metrics(self, account_balance: float, positions: Dict) -> RiskMetrics:
        """Calculate current risk metrics."""
        total_exposure = sum(
            pos.get('quantity', 0) * pos.get('current_price', 0) 
            for pos in positions.values()
        )
        
        max_position_risk = 0.0
        if positions:
            position_values = [
                pos.get('quantity', 0) * pos.get('current_price', 0) 
                for pos in positions.values()
            ]
            max_position_risk = max(position_values) / account_balance if account_balance > 0 else 0
        
        # Simplified risk metrics
        return RiskMetrics(
            total_exposure=total_exposure / account_balance if account_balance > 0 else 0,
            max_position_risk=max_position_risk,
            daily_pnl=self.daily_pnl,
            max_drawdown=self.max_drawdown,
            var_95=0.0,  # Would calculate from historical data
            sharpe_ratio=0.0,  # Would calculate from returns
            risk_score=min(total_exposure / account_balance, 1.0) if account_balance > 0 else 0
        )
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Get risk management summary."""
        return {
            'max_position_size': self.max_position_size,
            'max_daily_loss': self.max_daily_loss,
            'daily_pnl': self.daily_pnl,
            'max_drawdown': self.max_drawdown,
            'max_positions': self.max_positions,
            'recent_events': self.risk_events[-10:],  # Last 10 events
            'risk_controls_active': True
        }

# Global risk manager instance
risk_manager = None

def get_risk_manager() -> RiskManager:
    """Get the global risk manager instance."""
    global risk_manager
    if risk_manager is None:
        risk_manager = RiskManager()
    return risk_manager

if __name__ == "__main__":
    # Test risk manager
    rm = RiskManager()
    print("Risk Manager Test")
    print("=" * 20)
    print(f"Max position size: {rm.max_position_size * 100}%")
    print(f"Max daily loss: {rm.max_daily_loss * 100}%")
    print(f"Stop loss: {rm.stop_loss_pct * 100}%")
    print(f"Take profit: {rm.take_profit_pct * 100}%")
