"""
Execution system for AegisTrader.
Handles both simulated (paper) and live trading execution.
"""

import time
import logging
import uuid
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
from pathlib import Path

from config import (
    LIVE_TRADING,
    BROKER_API_KEY,
    BROKER_API_SECRET,
    BROKER_NAME,
    BROKER_SANDBOX,
    BROKER_MAX_RETRIES,
    BROKER_RETRY_BACKOFF_BASE_SEC,
)
from broker.symbol_resolver import resolve_venue_symbol
from assets import Asset
from strategy.strategy_engine import TradingSignal, SignalType

logger = logging.getLogger(__name__)

class OrderType(Enum):
    """Types of orders."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderStatus(Enum):
    """Order status types."""
    PENDING = "pending"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class PositionSide(Enum):
    """Position sides."""
    LONG = "long"
    SHORT = "short"

@dataclass
class Order:
    """Represents a trading order."""
    id: str
    asset: Asset
    side: str  # 'buy' or 'sell'
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: float = 0.0
    filled_price: Optional[float] = None
    timestamp: float = field(default_factory=time.time)
    fill_timestamp: Optional[float] = None
    fees: float = 0.0
    signal_id: Optional[str] = None
    client_order_id: str = ""
    exchange_order_id: Optional[str] = None

@dataclass
class Position:
    """Represents a trading position."""
    asset: Asset
    side: PositionSide
    quantity: float
    entry_price: float
    current_price: float
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0
    timestamp: float = field(default_factory=time.time)
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

@dataclass
class Trade:
    """Represents a completed trade."""
    id: str
    asset: Asset
    side: str
    quantity: float
    entry_price: float
    exit_price: float
    pnl: float
    fees: float
    entry_time: float
    exit_time: float
    duration: float
    signal_id: Optional[str] = None

class Execution:
    """Main execution engine for handling trades."""
    
    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.available_balance = initial_balance
        
        # Trading state
        self.orders: Dict[str, Order] = {}
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.order_counter = 0
        
        # Performance tracking
        self.total_pnl = 0.0
        self.total_fees = 0.0
        self.win_rate = 0.0
        self.max_drawdown = 0.0
        self.peak_balance = initial_balance
        
        # Risk management
        self.max_position_size = 0.1  # 10% of balance per position
        self.max_total_exposure = 0.5  # 50% total exposure
        
        # Initialize broker connection if live trading
        self.broker = None
        if LIVE_TRADING:
            self._initialize_live_trading()
        
        logger.info(f"Execution engine initialized - Mode: {'LIVE' if LIVE_TRADING else 'PAPER'}")
    
    def _initialize_live_trading(self):
        """Initialize live trading broker connection."""
        try:
            from broker.broker_api import create_broker_api
            from institutional.resilient_broker import ResilientBrokerAdapter
            from institutional.audit_log import get_audit_log

            base = create_broker_api(
                BROKER_NAME,
                BROKER_API_KEY or "",
                BROKER_API_SECRET or "",
                BROKER_SANDBOX,
            )
            if not base.connect():
                raise RuntimeError("Broker connect() returned False")
            self.broker = ResilientBrokerAdapter(
                base,
                max_retries=BROKER_MAX_RETRIES,
                backoff_base_sec=BROKER_RETRY_BACKOFF_BASE_SEC,
                audit=get_audit_log(),
            )
            logger.info("Live trading broker initialized (%s)", BROKER_NAME)
        except Exception as e:
            logger.error(f"Failed to initialize live trading: {e}")
            raise

    def get_broker(self):
        """Return broker adapter when live trading; None in paper mode."""
        return self.broker if LIVE_TRADING else None
    
    def place_order(self, signal: TradingSignal, quantity: Optional[float] = None) -> Optional[str]:
        """
        Place a trading order based on a signal.
        
        Args:
            signal: Trading signal to execute
            quantity: Optional quantity override
            
        Returns:
            Order ID if successful, None otherwise
        """
        try:
            # Calculate position size if not provided
            if quantity is None:
                quantity = self._calculate_position_size(signal)
            
            if quantity <= 0:
                logger.warning(f"Invalid quantity for {signal.asset.symbol}: {quantity}")
                return None
            
            # Validate order
            if not self._validate_order(signal, quantity):
                return None
            
            # Create order (client_order_id for venue idempotency / OMS)
            order_id = self._generate_order_id()
            client_order_id = str(uuid.uuid4())
            order = Order(
                id=order_id,
                asset=signal.asset,
                side="buy" if signal.signal_type in [SignalType.BUY, SignalType.STRONG_BUY] else "sell",
                order_type=OrderType.MARKET,  # Default to market orders
                quantity=quantity,
                price=signal.entry_price,
                signal_id=str(signal.timestamp),
                client_order_id=client_order_id,
            )

            try:
                from oms.order_registry import OrderRecord, LocalOrderState, get_order_registry
                from institutional.controls import get_institutional_controls

                venue_symbol = resolve_venue_symbol(signal.asset.tradingview_ticker, BROKER_NAME)
                get_order_registry().register_intent(
                    OrderRecord(
                        client_order_id=client_order_id,
                        symbol=signal.asset.symbol,
                        side=order.side,
                        quantity=quantity,
                        state=LocalOrderState.PENDING_SUBMIT,
                        tradingview_ticker=signal.asset.tradingview_ticker,
                        venue=BROKER_NAME,
                        venue_symbol=venue_symbol,
                    ),
                    internal_order_id=order_id,
                )
                get_institutional_controls().audit.append(
                    "order_intent",
                    {
                        "internal_order_id": order_id,
                        "client_order_id": client_order_id,
                        "symbol": signal.asset.symbol,
                        "side": order.side,
                        "quantity": quantity,
                    },
                )
            except Exception as e:
                logger.warning("OMS/audit registration failed (non-fatal): %s", e)

            # Execute order
            if LIVE_TRADING and self.broker:
                success = self._execute_live_order(order)
            else:
                success = self._execute_simulated_order(order)

            if success:
                self.orders[order_id] = order
                logger.info(f"Placed {order.side} order for {order.quantity} {order.asset.symbol}")
                if not LIVE_TRADING:
                    try:
                        from oms.order_registry import LocalOrderState, get_order_registry

                        r = get_order_registry()
                        r.mark_submitted(order.client_order_id, "paper")
                        r.mark_terminal(order.client_order_id, LocalOrderState.FILLED)
                    except Exception:
                        pass
                try:
                    from institutional.controls import get_institutional_controls

                    get_institutional_controls().circuit_breaker.record_success()
                except Exception:
                    pass
                return order_id
            else:
                logger.error(f"Failed to execute order for {signal.asset.symbol}")
                try:
                    from institutional.controls import get_institutional_controls

                    get_institutional_controls().circuit_breaker.record_failure()
                except Exception:
                    pass
                return None

        except Exception as e:
            logger.error(f"Error placing order: {e}")
            try:
                from institutional.controls import get_institutional_controls

                get_institutional_controls().circuit_breaker.record_failure()
            except Exception:
                pass
            return None
    
    def _calculate_position_size(self, signal: TradingSignal) -> float:
        """Calculate position size based on risk management rules."""
        if not signal.entry_price or not signal.stop_loss:
            return 0.0
        
        # Calculate risk amount (2% of balance)
        risk_amount = self.available_balance * 0.02
        
        # Calculate price risk
        if signal.signal_type in [SignalType.BUY, SignalType.STRONG_BUY]:
            price_risk = signal.entry_price - signal.stop_loss
        else:
            price_risk = signal.stop_loss - signal.entry_price
        
        if price_risk <= 0:
            return 0.0
        
        # Calculate position size
        position_size = risk_amount / price_risk
        
        # Apply maximum position size limit
        max_position_value = self.available_balance * self.max_position_size
        max_quantity = max_position_value / signal.entry_price
        
        return min(position_size, max_quantity)
    
    def _validate_order(self, signal: TradingSignal, quantity: float) -> bool:
        """Validate if an order can be placed."""
        # Check available balance
        required_balance = quantity * signal.entry_price
        if required_balance > self.available_balance:
            logger.warning(f"Insufficient balance: {required_balance} > {self.available_balance}")
            return False
        
        # Check position limits
        current_exposure = sum(
            pos.quantity * pos.current_price for pos in self.positions.values()
        )
        
        if (current_exposure + required_balance) > (self.current_balance * self.max_total_exposure):
            logger.warning("Maximum total exposure reached")
            return False
        
        # Check if already have position in this asset
        if signal.asset.symbol in self.positions:
            logger.warning(f"Already have position in {signal.asset.symbol}")
            return False
        
        return True
    
    def _execute_live_order(self, order: Order) -> bool:
        """Execute order through live broker."""
        try:
            from oms.order_registry import LocalOrderState, get_order_registry

            venue_symbol = resolve_venue_symbol(order.asset.tradingview_ticker, BROKER_NAME)
            result = self.broker.place_order(
                symbol=venue_symbol,
                side=order.side,
                quantity=order.quantity,
                order_type=order.order_type.value,
                price=order.price,
                client_order_id=order.client_order_id or None,
            )

            if result and result.success:
                order.status = OrderStatus.FILLED
                order.filled_quantity = result.filled_quantity or order.quantity
                order.filled_price = result.fill_price if result.fill_price is not None else order.price
                order.fill_timestamp = time.time()
                order.fees = result.fees or 0.0
                order.exchange_order_id = result.order_id

                reg = get_order_registry()
                reg.mark_submitted(order.client_order_id, result.order_id)
                reg.mark_terminal(order.client_order_id, LocalOrderState.FILLED)

                self._update_position(order)
                logger.info(f"Live order executed: {order.id} exchange_id={result.order_id}")
                return True
            else:
                order.status = OrderStatus.REJECTED
                err = result.error_message if result else "unknown"
                logger.error("Live order rejected: %s", err)
                try:
                    get_order_registry().mark_terminal(
                        order.client_order_id, LocalOrderState.REJECTED
                    )
                except Exception:
                    pass
                return False

        except Exception as e:
            logger.error(f"Error executing live order: {e}")
            order.status = OrderStatus.REJECTED
            return False
    
    def _execute_simulated_order(self, order: Order) -> bool:
        """Execute order in simulation mode."""
        try:
            # Simulate immediate fill at market price
            order.status = OrderStatus.FILLED
            order.filled_quantity = order.quantity
            order.filled_price = order.price or 0.0
            order.fill_timestamp = time.time()
            
            # Simulate fees (0.1% for simulation)
            order.fees = order.filled_quantity * order.filled_price * 0.001
            
            self._update_position(order)
            self._update_balance(order)
            
            logger.info(f"Simulated order executed: {order.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error executing simulated order: {e}")
            return False
    
    def _update_position(self, order: Order):
        """Update position based on filled order."""
        symbol = order.asset.symbol
        
        if order.side == "buy":
            if symbol in self.positions:
                # Add to existing position
                pos = self.positions[symbol]
                total_cost = (pos.quantity * pos.entry_price) + (order.filled_quantity * order.filled_price)
                total_quantity = pos.quantity + order.filled_quantity
                pos.entry_price = total_cost / total_quantity
                pos.quantity = total_quantity
            else:
                # Create new long position
                self.positions[symbol] = Position(
                    asset=order.asset,
                    side=PositionSide.LONG,
                    quantity=order.filled_quantity,
                    entry_price=order.filled_price,
                    current_price=order.filled_price
                )
        
        elif order.side == "sell":
            if symbol in self.positions:
                pos = self.positions[symbol]
                if pos.quantity >= order.filled_quantity:
                    # Reduce or close position
                    pos.quantity -= order.filled_quantity
                    if pos.quantity <= 0:
                        # Position closed - record trade
                        self._record_trade(pos, order)
                        del self.positions[symbol]
                else:
                    logger.warning(f"Trying to sell more than position size for {symbol}")
            else:
                # Create new short position
                self.positions[symbol] = Position(
                    asset=order.asset,
                    side=PositionSide.SHORT,
                    quantity=order.filled_quantity,
                    entry_price=order.filled_price,
                    current_price=order.filled_price
                )

    def _update_balance(self, order: Order):
        """Update account balance after order execution."""
        if order.side == "buy":
            cost = order.filled_quantity * order.filled_price + order.fees
            self.available_balance -= cost
        elif order.side == "sell":
            proceeds = order.filled_quantity * order.filled_price - order.fees
            self.available_balance += proceeds

        self.total_fees += order.fees

    def _record_trade(self, position: Position, exit_order: Order):
        """Record a completed trade."""
        trade_id = f"trade_{len(self.trades) + 1}"

        # Calculate PnL
        if position.side == PositionSide.LONG:
            pnl = (exit_order.filled_price - position.entry_price) * position.quantity
        else:
            pnl = (position.entry_price - exit_order.filled_price) * position.quantity

        pnl -= exit_order.fees  # Subtract exit fees

        trade = Trade(
            id=trade_id,
            asset=position.asset,
            side=position.side.value,
            quantity=position.quantity,
            entry_price=position.entry_price,
            exit_price=exit_order.filled_price,
            pnl=pnl,
            fees=exit_order.fees,
            entry_time=position.timestamp,
            exit_time=exit_order.fill_timestamp or time.time(),
            duration=time.time() - position.timestamp,
            signal_id=exit_order.signal_id
        )

        self.trades.append(trade)
        self.total_pnl += pnl
        self.current_balance += pnl

        logger.info(f"Trade completed: {trade.asset.symbol} PnL: {pnl:.2f}")

    def _generate_order_id(self) -> str:
        """Generate unique order ID."""
        self.order_counter += 1
        return f"order_{int(time.time())}_{self.order_counter}"

    def update_positions(self, price_updates: Dict[str, float]):
        """Update position prices and unrealized PnL."""
        for symbol, current_price in price_updates.items():
            if symbol in self.positions:
                pos = self.positions[symbol]
                pos.current_price = current_price

                # Calculate unrealized PnL
                if pos.side == PositionSide.LONG:
                    pos.unrealized_pnl = (current_price - pos.entry_price) * pos.quantity
                else:
                    pos.unrealized_pnl = (pos.entry_price - current_price) * pos.quantity

    def close_position(self, symbol: str, reason: str = "manual") -> Optional[str]:
        """Close a position manually."""
        if symbol not in self.positions:
            logger.warning(f"No position found for {symbol}")
            return None

        position = self.positions[symbol]

        # Create closing order
        order_id = self._generate_order_id()
        side = "sell" if position.side == PositionSide.LONG else "buy"

        order = Order(
            id=order_id,
            asset=position.asset,
            side=side,
            order_type=OrderType.MARKET,
            quantity=position.quantity,
            price=position.current_price,
            client_order_id=str(uuid.uuid4()),
        )

        # Execute closing order
        if LIVE_TRADING and self.broker:
            success = self._execute_live_order(order)
        else:
            success = self._execute_simulated_order(order)

        if success:
            logger.info(f"Closed position {symbol} - Reason: {reason}")
            return order_id

        return None

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get current portfolio summary."""
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in self.positions.values())
        total_position_value = sum(
            pos.quantity * pos.current_price for pos in self.positions.values()
        )

        # Calculate performance metrics
        total_return = (self.current_balance + total_unrealized_pnl - self.initial_balance) / self.initial_balance

        # Calculate win rate
        winning_trades = len([t for t in self.trades if t.pnl > 0])
        total_trades = len(self.trades)
        win_rate = winning_trades / total_trades if total_trades > 0 else 0.0

        # Update peak balance and max drawdown
        current_equity = self.current_balance + total_unrealized_pnl
        if current_equity > self.peak_balance:
            self.peak_balance = current_equity

        drawdown = (self.peak_balance - current_equity) / self.peak_balance if self.peak_balance > 0 else 0.0
        self.max_drawdown = max(self.max_drawdown, drawdown)

        return {
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'available_balance': self.available_balance,
            'total_position_value': total_position_value,
            'total_unrealized_pnl': total_unrealized_pnl,
            'total_realized_pnl': self.total_pnl,
            'total_fees': self.total_fees,
            'current_equity': current_equity,
            'total_return': total_return,
            'win_rate': win_rate,
            'max_drawdown': self.max_drawdown,
            'total_trades': total_trades,
            'open_positions': len(self.positions),
            'pending_orders': len([o for o in self.orders.values() if o.status == OrderStatus.PENDING])
        }

    def get_positions(self) -> List[Dict[str, Any]]:
        """Get current positions."""
        return [
            {
                'symbol': pos.asset.symbol,
                'side': pos.side.value,
                'quantity': pos.quantity,
                'entry_price': pos.entry_price,
                'current_price': pos.current_price,
                'unrealized_pnl': pos.unrealized_pnl,
                'timestamp': pos.timestamp
            }
            for pos in self.positions.values()
        ]

    def get_recent_trades(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent trades."""
        recent_trades = sorted(self.trades, key=lambda t: t.exit_time, reverse=True)[:limit]

        return [
            {
                'id': trade.id,
                'symbol': trade.asset.symbol,
                'side': trade.side,
                'quantity': trade.quantity,
                'entry_price': trade.entry_price,
                'exit_price': trade.exit_price,
                'pnl': trade.pnl,
                'duration': trade.duration,
                'exit_time': trade.exit_time
            }
            for trade in recent_trades
        ]

    def save_state(self, filepath: str):
        """Save execution state to file."""
        state = {
            'balance': self.current_balance,
            'available_balance': self.available_balance,
            'total_pnl': self.total_pnl,
            'total_fees': self.total_fees,
            'trades': [
                {
                    'id': t.id,
                    'symbol': t.asset.symbol,
                    'side': t.side,
                    'quantity': t.quantity,
                    'entry_price': t.entry_price,
                    'exit_price': t.exit_price,
                    'pnl': t.pnl,
                    'fees': t.fees,
                    'entry_time': t.entry_time,
                    'exit_time': t.exit_time,
                    'duration': t.duration
                }
                for t in self.trades
            ]
        }

        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)

        logger.info(f"Execution state saved to {filepath}")

# Global execution instance
execution_engine = None

def get_execution_engine() -> Execution:
    """Get the global execution engine instance."""
    global execution_engine
    if execution_engine is None:
        execution_engine = Execution()
    return execution_engine

if __name__ == "__main__":
    # Test the execution engine
    execution = Execution(initial_balance=10000.0)

    print("Execution Engine Test")
    print("=" * 30)
    print(f"Mode: {'LIVE' if LIVE_TRADING else 'PAPER'}")
    print(f"Initial balance: ${execution.initial_balance:,.2f}")

    summary = execution.get_portfolio_summary()
    print(f"Current equity: ${summary['current_equity']:,.2f}")
    print(f"Total trades: {summary['total_trades']}")
    print(f"Open positions: {summary['open_positions']}")
