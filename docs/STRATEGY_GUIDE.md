# 🧠 AegisTrader Strategy Development Guide

Complete guide for creating, testing, and optimizing custom trading strategies.

## 📋 Table of Contents

- [Strategy Architecture](#strategy-architecture)
- [Creating Custom Strategies](#creating-custom-strategies)
- [Built-in Strategies](#built-in-strategies)
- [Backtesting Framework](#backtesting-framework)
- [Parameter Optimization](#parameter-optimization)
- [Risk-Reward Analysis](#risk-reward-analysis)
- [Multi-Timeframe Analysis](#multi-timeframe-analysis)
- [Strategy Combination](#strategy-combination)
- [Performance Metrics](#performance-metrics)
- [Best Practices](#best-practices)

## 🏗️ Strategy Architecture

### Strategy Engine Overview

The AegisTrader strategy engine is built around a modular architecture that allows for:

- **Multiple Strategy Types**: Momentum, mean reversion, breakout, pattern recognition, multi-timeframe
- **Signal Generation**: BUY, SELL, STRONG_BUY, STRONG_SELL, HOLD signals
- **Confidence Scoring**: 0.0 to 1.0 confidence levels for each signal
- **Risk Integration**: Automatic position sizing and risk management
- **Multi-Asset Support**: Works across crypto, stocks, and commodities

### Core Components

```python
# strategy/strategy_engine.py
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

class SignalType(Enum):
    BUY = "buy"
    SELL = "sell"
    STRONG_BUY = "strong_buy"
    STRONG_SELL = "strong_sell"
    HOLD = "hold"

class StrategyType(Enum):
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    BREAKOUT = "breakout"
    PATTERN_RECOGNITION = "pattern_recognition"
    MULTI_TIMEFRAME = "multi_timeframe"
    CUSTOM = "custom"

@dataclass
class TradingSignal:
    asset: Asset
    signal_type: SignalType
    strategy: StrategyType
    confidence: float
    entry_price: float
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    timestamp: float = 0.0
    signal_id: str = ""
    metadata: Dict = None
```

## 🔧 Creating Custom Strategies

### Step 1: Define Strategy Class

Create a new strategy by inheriting from the base strategy interface:

```python
# strategy/custom_strategies.py
from .strategy_engine import StrategyEngine, TradingSignal, SignalType, StrategyType
from scanner.market_scanner import ScanResult, MarketOpportunity
import numpy as np

class RSIStrategy:
    """RSI-based mean reversion strategy."""
    
    def __init__(self, rsi_period: int = 14, oversold: float = 30, overbought: float = 70):
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        self.name = "RSI Mean Reversion"
    
    def analyze(self, scan_result: ScanResult, opportunity: MarketOpportunity) -> Optional[TradingSignal]:
        """Analyze market data and generate trading signal."""
        
        # Extract price data
        price_data = scan_result.price_data
        if not price_data or not price_data.current_price:
            return None
        
        # Calculate RSI (simplified implementation)
        rsi = self._calculate_rsi(price_data)
        if rsi is None:
            return None
        
        # Generate signals based on RSI levels
        signal_type = None
        confidence = 0.0
        
        if rsi <= self.oversold:
            signal_type = SignalType.BUY
            confidence = min(0.9, (self.oversold - rsi) / self.oversold + 0.5)
        elif rsi >= self.overbought:
            signal_type = SignalType.SELL
            confidence = min(0.9, (rsi - self.overbought) / (100 - self.overbought) + 0.5)
        else:
            signal_type = SignalType.HOLD
            confidence = 0.3
        
        if signal_type == SignalType.HOLD:
            return None
        
        # Calculate entry, target, and stop loss prices
        entry_price = price_data.current_price
        
        if signal_type == SignalType.BUY:
            target_price = entry_price * 1.02  # 2% target
            stop_loss = entry_price * 0.99     # 1% stop loss
        else:  # SELL
            target_price = entry_price * 0.98  # 2% target
            stop_loss = entry_price * 1.01     # 1% stop loss
        
        return TradingSignal(
            asset=opportunity.asset,
            signal_type=signal_type,
            strategy=StrategyType.CUSTOM,
            confidence=confidence,
            entry_price=entry_price,
            target_price=target_price,
            stop_loss=stop_loss,
            timestamp=time.time(),
            signal_id=f"rsi_{opportunity.asset.symbol}_{int(time.time())}",
            metadata={
                'rsi': rsi,
                'strategy_name': self.name,
                'parameters': {
                    'rsi_period': self.rsi_period,
                    'oversold': self.oversold,
                    'overbought': self.overbought
                }
            }
        )
    
    def _calculate_rsi(self, price_data) -> Optional[float]:
        """Calculate RSI indicator."""
        # This is a simplified implementation
        # In practice, you would need historical price data
        
        # For demonstration, return a random RSI value
        # Replace with actual RSI calculation using historical data
        import random
        return random.uniform(20, 80)

class MACDStrategy:
    """MACD crossover strategy."""
    
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.name = "MACD Crossover"
    
    def analyze(self, scan_result: ScanResult, opportunity: MarketOpportunity) -> Optional[TradingSignal]:
        """Analyze using MACD crossover."""
        
        # Calculate MACD components
        macd_line, signal_line, histogram = self._calculate_macd(scan_result.price_data)
        
        if macd_line is None or signal_line is None:
            return None
        
        # Detect crossovers
        signal_type = None
        confidence = 0.0
        
        # Bullish crossover: MACD line crosses above signal line
        if macd_line > signal_line and histogram > 0:
            signal_type = SignalType.BUY
            confidence = min(0.85, abs(histogram) * 10 + 0.5)
        
        # Bearish crossover: MACD line crosses below signal line
        elif macd_line < signal_line and histogram < 0:
            signal_type = SignalType.SELL
            confidence = min(0.85, abs(histogram) * 10 + 0.5)
        
        if not signal_type or confidence < 0.6:
            return None
        
        entry_price = scan_result.price_data.current_price
        
        if signal_type == SignalType.BUY:
            target_price = entry_price * 1.025  # 2.5% target
            stop_loss = entry_price * 0.985     # 1.5% stop loss
        else:
            target_price = entry_price * 0.975  # 2.5% target
            stop_loss = entry_price * 1.015     # 1.5% stop loss
        
        return TradingSignal(
            asset=opportunity.asset,
            signal_type=signal_type,
            strategy=StrategyType.CUSTOM,
            confidence=confidence,
            entry_price=entry_price,
            target_price=target_price,
            stop_loss=stop_loss,
            timestamp=time.time(),
            signal_id=f"macd_{opportunity.asset.symbol}_{int(time.time())}",
            metadata={
                'macd_line': macd_line,
                'signal_line': signal_line,
                'histogram': histogram,
                'strategy_name': self.name
            }
        )
    
    def _calculate_macd(self, price_data) -> tuple:
        """Calculate MACD components."""
        # Simplified implementation - replace with actual calculation
        import random
        macd_line = random.uniform(-0.5, 0.5)
        signal_line = random.uniform(-0.5, 0.5)
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
```

### Step 2: Register Custom Strategy

Add your custom strategy to the strategy engine:

```python
# strategy/strategy_engine.py (modification)
class StrategyEngine:
    def __init__(self):
        # ... existing code ...
        
        # Initialize custom strategies
        self.custom_strategies = {
            'rsi': RSIStrategy(),
            'macd': MACDStrategy(),
            # Add more custom strategies here
        }
    
    def analyze_opportunity(self, opportunity: MarketOpportunity, scan_result: ScanResult) -> Optional[TradingSignal]:
        """Enhanced analysis including custom strategies."""
        signals = []
        
        # Run built-in strategies
        for strategy_type in self.enabled_strategies:
            signal = self._run_strategy(strategy_type, opportunity, scan_result)
            if signal:
                signals.append(signal)
        
        # Run custom strategies
        for strategy_name, strategy in self.custom_strategies.items():
            if self._is_strategy_enabled(strategy_name):
                signal = strategy.analyze(scan_result, opportunity)
                if signal:
                    signals.append(signal)
        
        # Combine signals
        return self._combine_signals(signals) if signals else None
```

### Step 3: Configuration

Add custom strategy configuration to `.env`:

```env
# Custom strategy settings
CUSTOM_STRATEGIES=rsi,macd
RSI_PERIOD=14
RSI_OVERSOLD=30
RSI_OVERBOUGHT=70
MACD_FAST_PERIOD=12
MACD_SLOW_PERIOD=26
MACD_SIGNAL_PERIOD=9
```

## 📊 Built-in Strategies

### 1. Momentum Strategy

Identifies trending markets and enters positions in the direction of momentum:

```python
def _momentum_strategy(self, opportunity: MarketOpportunity, scan_result: ScanResult) -> Optional[TradingSignal]:
    """Momentum-based strategy implementation."""
    
    price_data = scan_result.price_data
    if not price_data:
        return None
    
    # Calculate momentum indicators
    price_change = price_data.change_percent or 0
    volume_ratio = self._calculate_volume_ratio(price_data)
    
    # Momentum scoring
    momentum_score = 0.0
    
    # Price momentum (40% weight)
    if abs(price_change) > 2.0:  # Significant price movement
        momentum_score += 0.4 * min(abs(price_change) / 5.0, 1.0)
    
    # Volume confirmation (30% weight)
    if volume_ratio > 1.5:  # Above average volume
        momentum_score += 0.3 * min(volume_ratio / 3.0, 1.0)
    
    # Pattern confirmation (30% weight)
    if scan_result.pattern_analysis:
        pattern_score = scan_result.pattern_analysis.get('confidence', 0)
        momentum_score += 0.3 * pattern_score
    
    # Generate signal
    if momentum_score >= 0.7:
        signal_type = SignalType.STRONG_BUY if price_change > 0 else SignalType.STRONG_SELL
        confidence = min(momentum_score, 0.95)
    elif momentum_score >= 0.5:
        signal_type = SignalType.BUY if price_change > 0 else SignalType.SELL
        confidence = momentum_score
    else:
        return None
    
    return self._create_signal(opportunity.asset, signal_type, StrategyType.MOMENTUM, confidence, price_data.current_price)
```

### 2. Mean Reversion Strategy

Identifies overbought/oversold conditions for counter-trend entries:

```python
def _mean_reversion_strategy(self, opportunity: MarketOpportunity, scan_result: ScanResult) -> Optional[TradingSignal]:
    """Mean reversion strategy implementation."""
    
    price_data = scan_result.price_data
    if not price_data:
        return None
    
    # Calculate mean reversion indicators
    price_change = price_data.change_percent or 0
    volatility = self._estimate_volatility(price_data)
    
    # Mean reversion scoring
    reversion_score = 0.0
    
    # Extreme price movements (50% weight)
    if abs(price_change) > 3.0:  # Extreme movement
        reversion_score += 0.5 * min(abs(price_change) / 8.0, 1.0)
    
    # Low volume on extreme moves (30% weight)
    volume_ratio = self._calculate_volume_ratio(price_data)
    if volume_ratio < 0.8:  # Below average volume
        reversion_score += 0.3 * (1.0 - volume_ratio)
    
    # Volatility consideration (20% weight)
    if volatility > 0.02:  # High volatility
        reversion_score += 0.2 * min(volatility / 0.05, 1.0)
    
    # Generate counter-trend signal
    if reversion_score >= 0.6:
        # Counter-trend signal
        signal_type = SignalType.SELL if price_change > 0 else SignalType.BUY
        confidence = min(reversion_score, 0.85)
        
        return self._create_signal(opportunity.asset, signal_type, StrategyType.MEAN_REVERSION, confidence, price_data.current_price)
    
    return None
```

### 3. Breakout Strategy

Detects price breakouts from consolidation patterns:

```python
def _breakout_strategy(self, opportunity: MarketOpportunity, scan_result: ScanResult) -> Optional[TradingSignal]:
    """Breakout strategy implementation."""
    
    price_data = scan_result.price_data
    pattern_analysis = scan_result.pattern_analysis
    
    if not price_data or not pattern_analysis:
        return None
    
    # Look for breakout patterns
    breakout_patterns = ['triangle', 'rectangle', 'flag', 'pennant']
    detected_patterns = pattern_analysis.get('patterns', [])
    
    breakout_score = 0.0
    
    # Pattern detection (40% weight)
    for pattern in detected_patterns:
        if pattern.get('type') in breakout_patterns:
            breakout_score += 0.4 * pattern.get('confidence', 0)
    
    # Volume confirmation (35% weight)
    volume_ratio = self._calculate_volume_ratio(price_data)
    if volume_ratio > 1.8:  # High volume breakout
        breakout_score += 0.35 * min(volume_ratio / 3.0, 1.0)
    
    # Price action (25% weight)
    price_change = abs(price_data.change_percent or 0)
    if price_change > 1.5:  # Significant price movement
        breakout_score += 0.25 * min(price_change / 4.0, 1.0)
    
    # Generate breakout signal
    if breakout_score >= 0.65:
        direction = 1 if (price_data.change_percent or 0) > 0 else -1
        signal_type = SignalType.BUY if direction > 0 else SignalType.SELL
        confidence = min(breakout_score, 0.9)
        
        return self._create_signal(opportunity.asset, signal_type, StrategyType.BREAKOUT, confidence, price_data.current_price)
    
    return None
```

## 🧪 Backtesting Framework

### Backtesting Engine

Create a comprehensive backtesting system:

```python
# backtesting/backtest_engine.py
from dataclasses import dataclass
from typing import List, Dict, Any
import pandas as pd
import numpy as np

@dataclass
class BacktestResult:
    """Backtest results container."""
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    profit_factor: float
    total_trades: int
    avg_trade_duration: float
    trades: List[Dict]
    equity_curve: List[float]
    metrics: Dict[str, Any]

class BacktestEngine:
    """Backtesting engine for strategy validation."""
    
    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.commission = 0.001  # 0.1% commission
        
    def run_backtest(self, strategy, historical_data: pd.DataFrame, 
                    start_date: str, end_date: str) -> BacktestResult:
        """Run backtest for a strategy."""
        
        # Initialize backtest state
        capital = self.initial_capital
        positions = {}
        trades = []
        equity_curve = [capital]
        
        # Filter data by date range
        data = historical_data[(historical_data.index >= start_date) & 
                              (historical_data.index <= end_date)]
        
        for timestamp, row in data.iterrows():
            # Create mock scan result
            scan_result = self._create_scan_result(row)
            opportunity = self._create_opportunity(row)
            
            # Generate signal
            signal = strategy.analyze(scan_result, opportunity)
            
            if signal:
                # Execute trade
                trade_result = self._execute_backtest_trade(
                    signal, capital, positions, timestamp
                )
                
                if trade_result:
                    trades.append(trade_result)
                    capital = trade_result['new_capital']
            
            # Update equity curve
            current_equity = self._calculate_equity(capital, positions, row)
            equity_curve.append(current_equity)
        
        # Calculate final metrics
        return self._calculate_backtest_metrics(
            trades, equity_curve, self.initial_capital
        )
    
    def _execute_backtest_trade(self, signal: TradingSignal, capital: float, 
                               positions: Dict, timestamp) -> Optional[Dict]:
        """Execute a trade in backtest."""
        
        symbol = signal.asset.symbol
        entry_price = signal.entry_price
        
        # Calculate position size (2% risk)
        risk_amount = capital * 0.02
        stop_distance = abs(entry_price - signal.stop_loss) if signal.stop_loss else entry_price * 0.02
        position_size = risk_amount / stop_distance
        
        # Check if we have enough capital
        trade_value = position_size * entry_price
        commission_cost = trade_value * self.commission
        
        if trade_value + commission_cost > capital:
            return None  # Insufficient capital
        
        # Record trade
        trade = {
            'timestamp': timestamp,
            'symbol': symbol,
            'signal_type': signal.signal_type.value,
            'entry_price': entry_price,
            'position_size': position_size,
            'stop_loss': signal.stop_loss,
            'target_price': signal.target_price,
            'commission': commission_cost,
            'new_capital': capital - trade_value - commission_cost
        }
        
        return trade
    
    def _calculate_backtest_metrics(self, trades: List[Dict], 
                                   equity_curve: List[float], 
                                   initial_capital: float) -> BacktestResult:
        """Calculate comprehensive backtest metrics."""
        
        if not trades:
            return BacktestResult(
                total_return=0.0, annual_return=0.0, max_drawdown=0.0,
                sharpe_ratio=0.0, win_rate=0.0, profit_factor=0.0,
                total_trades=0, avg_trade_duration=0.0, trades=[],
                equity_curve=equity_curve, metrics={}
            )
        
        # Calculate returns
        final_capital = equity_curve[-1]
        total_return = (final_capital - initial_capital) / initial_capital
        
        # Calculate drawdown
        peak = initial_capital
        max_drawdown = 0.0
        for equity in equity_curve:
            if equity > peak:
                peak = equity
            drawdown = (peak - equity) / peak
            max_drawdown = max(max_drawdown, drawdown)
        
        # Calculate win rate
        winning_trades = len([t for t in trades if t.get('pnl', 0) > 0])
        win_rate = winning_trades / len(trades) if trades else 0.0
        
        # Calculate Sharpe ratio (simplified)
        returns = np.diff(equity_curve) / equity_curve[:-1]
        sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0.0
        
        return BacktestResult(
            total_return=total_return,
            annual_return=total_return,  # Simplified
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            win_rate=win_rate,
            profit_factor=0.0,  # Calculate separately
            total_trades=len(trades),
            avg_trade_duration=0.0,  # Calculate separately
            trades=trades,
            equity_curve=equity_curve,
            metrics={}
        )
```

### Running Backtests

```python
# Example backtest execution
def run_strategy_backtest():
    """Run backtest for custom strategy."""
    
    # Load historical data
    data = pd.read_csv('data/historical_prices.csv', index_col='timestamp', parse_dates=True)
    
    # Initialize strategy
    strategy = RSIStrategy(rsi_period=14, oversold=30, overbought=70)
    
    # Run backtest
    backtest_engine = BacktestEngine(initial_capital=10000.0)
    result = backtest_engine.run_backtest(
        strategy=strategy,
        historical_data=data,
        start_date='2023-01-01',
        end_date='2023-12-31'
    )
    
    # Print results
    print(f"Total Return: {result.total_return:.2%}")
    print(f"Max Drawdown: {result.max_drawdown:.2%}")
    print(f"Sharpe Ratio: {result.sharpe_ratio:.2f}")
    print(f"Win Rate: {result.win_rate:.2%}")
    print(f"Total Trades: {result.total_trades}")
    
    return result
```

## 🎯 Parameter Optimization

### Grid Search Optimization

```python
# optimization/parameter_optimizer.py
from itertools import product
import pandas as pd

class ParameterOptimizer:
    """Parameter optimization for trading strategies."""
    
    def __init__(self, backtest_engine: BacktestEngine):
        self.backtest_engine = backtest_engine
    
    def optimize_rsi_strategy(self, historical_data: pd.DataFrame) -> Dict:
        """Optimize RSI strategy parameters."""
        
        # Define parameter ranges
        rsi_periods = [10, 14, 18, 21]
        oversold_levels = [20, 25, 30, 35]
        overbought_levels = [65, 70, 75, 80]
        
        best_result = None
        best_params = None
        best_sharpe = -999
        
        # Grid search
        for rsi_period, oversold, overbought in product(rsi_periods, oversold_levels, overbought_levels):
            if oversold >= overbought:
                continue
            
            # Create strategy with parameters
            strategy = RSIStrategy(
                rsi_period=rsi_period,
                oversold=oversold,
                overbought=overbought
            )
            
            # Run backtest
            result = self.backtest_engine.run_backtest(
                strategy=strategy,
                historical_data=historical_data,
                start_date='2023-01-01',
                end_date='2023-12-31'
            )
            
            # Check if this is the best result
            if result.sharpe_ratio > best_sharpe:
                best_sharpe = result.sharpe_ratio
                best_result = result
                best_params = {
                    'rsi_period': rsi_period,
                    'oversold': oversold,
                    'overbought': overbought
                }
        
        return {
            'best_params': best_params,
            'best_result': best_result,
            'optimization_metric': 'sharpe_ratio'
        }
```

This strategy guide provides a comprehensive framework for developing, testing, and optimizing custom trading strategies within the AegisTrader ecosystem.
