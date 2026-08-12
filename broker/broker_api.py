"""
Broker API interface for AegisTrader.
Abstract interface for live trading integration with various brokers/exchanges.
"""

import time
import logging
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class OrderSide(Enum):
    """Order sides."""
    BUY = "buy"
    SELL = "sell"

class OrderType(Enum):
    """Order types."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

@dataclass
class OrderResult:
    """Result of placing an order."""
    success: bool
    order_id: Optional[str] = None
    status: Optional[str] = None
    fill_price: Optional[float] = None
    filled_quantity: Optional[float] = None
    fees: Optional[float] = None
    error_message: Optional[str] = None
    timestamp: float = 0.0

@dataclass
class AccountInfo:
    """Account information."""
    balance: float
    available_balance: float
    positions: List[Dict] = None
    margin_used: float = 0.0
    margin_available: float = 0.0

class BrokerAPI(ABC):
    """Abstract base class for broker API implementations."""
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.sandbox = sandbox
        self.is_connected = False
        
    @abstractmethod
    def connect(self) -> bool:
        """Connect to the broker API."""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Disconnect from the broker API."""
        pass
    
    @abstractmethod
    def place_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        order_type: str = "market",
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        client_order_id: Optional[str] = None,
    ) -> OrderResult:
        """Place a trading order. client_order_id enables venue idempotency / OMS correlation."""
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str, symbol: Optional[str] = None) -> bool:
        """Cancel an existing order. Some venues require ``symbol`` (e.g. Binance spot)."""
        pass

    @abstractmethod
    def get_order_status(self, order_id: str, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Order lookup; pass ``symbol`` when the venue requires it."""
        pass
    
    @abstractmethod
    def get_account_info(self) -> AccountInfo:
        """Get account information."""
        pass
    
    @abstractmethod
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get current positions."""
        pass
    
    @abstractmethod
    def get_balance(self) -> float:
        """Get account balance."""
        pass

class MockBrokerAPI(BrokerAPI):
    """Mock broker API for testing and development."""
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        super().__init__(api_key, api_secret, sandbox)
        self.orders = {}
        self.positions = {}
        self.balance = 10000.0
        self.order_counter = 0
        # Idempotent replay for same client_order_id (institutional OMS pattern)
        self._idempotent: Dict[str, OrderResult] = {}
        
    def connect(self) -> bool:
        """Connect to the mock broker."""
        logger.info("Connected to Mock Broker API")
        self.is_connected = True
        return True
    
    def disconnect(self):
        """Disconnect from the mock broker."""
        logger.info("Disconnected from Mock Broker API")
        self.is_connected = False
    
    def place_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        order_type: str = "market",
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        client_order_id: Optional[str] = None,
    ) -> OrderResult:
        """Place a mock trading order."""
        if not self.is_connected:
            return OrderResult(
                success=False,
                error_message="Not connected to broker",
                timestamp=time.time()
            )

        if client_order_id and client_order_id in self._idempotent:
            return self._idempotent[client_order_id]
        
        # Generate order ID
        self.order_counter += 1
        order_id = f"mock_order_{self.order_counter}"
        
        # Simulate order execution
        if order_type == "market":
            # Simulate immediate fill at current "market" price
            fill_price = price or 100.0  # Mock price
            filled_quantity = quantity
            fees = quantity * fill_price * 0.001  # 0.1% fee
            
            # Update mock balance
            if side == "buy":
                cost = filled_quantity * fill_price + fees
                if cost <= self.balance:
                    self.balance -= cost
                    success = True
                else:
                    success = False
                    error_message = "Insufficient balance"
            else:  # sell
                proceeds = filled_quantity * fill_price - fees
                self.balance += proceeds
                success = True
            
            if success:
                # Store order
                self.orders[order_id] = {
                    'id': order_id,
                    'symbol': symbol,
                    'side': side,
                    'quantity': quantity,
                    'order_type': order_type,
                    'status': 'filled',
                    'fill_price': fill_price,
                    'filled_quantity': filled_quantity,
                    'fees': fees,
                    'timestamp': time.time()
                }
                
                result = OrderResult(
                    success=True,
                    order_id=order_id,
                    status='filled',
                    fill_price=fill_price,
                    filled_quantity=filled_quantity,
                    fees=fees,
                    timestamp=time.time()
                )
                if client_order_id:
                    self._idempotent[client_order_id] = result
                return result
            else:
                return OrderResult(
                    success=False,
                    error_message=error_message,
                    timestamp=time.time()
                )
        
        else:
            # For limit orders, just store as pending
            self.orders[order_id] = {
                'id': order_id,
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'order_type': order_type,
                'price': price,
                'stop_price': stop_price,
                'status': 'pending',
                'timestamp': time.time()
            }
            
            result = OrderResult(
                success=True,
                order_id=order_id,
                status='pending',
                timestamp=time.time()
            )
            if client_order_id:
                self._idempotent[client_order_id] = result
            return result
    
    def cancel_order(self, order_id: str, symbol: Optional[str] = None) -> bool:
        """Cancel a mock order."""
        if order_id in self.orders:
            self.orders[order_id]["status"] = "cancelled"
            logger.info(f"Cancelled mock order {order_id}")
            return True
        return False

    def get_order_status(self, order_id: str, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get mock order status."""
        return self.orders.get(order_id, {})
    
    def get_account_info(self) -> AccountInfo:
        """Get mock account information."""
        return AccountInfo(
            balance=self.balance,
            available_balance=self.balance,
            positions=[],
            margin_used=0.0,
            margin_available=self.balance
        )
    
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get mock positions."""
        return list(self.positions.values())
    
    def get_balance(self) -> float:
        """Get mock balance."""
        return self.balance

def create_broker_api(broker_name: str, api_key: str, api_secret: str, 
                     sandbox: bool = True) -> BrokerAPI:
    """
    Factory function to create broker API instances.
    
    Args:
        broker_name: Name of the broker ('mock', 'binance', etc.)
        api_key: API key
        api_secret: API secret
        sandbox: Whether to use sandbox/testnet
        
    Returns:
        BrokerAPI instance
    """
    broker_name = broker_name.lower()
    
    if broker_name == 'mock':
        return MockBrokerAPI(api_key, api_secret, sandbox)
    elif broker_name == "binance":
        from broker.binance_spot import BinanceSpotBroker

        return BinanceSpotBroker(api_key, api_secret, sandbox)
    elif broker_name == "mcp":
        from mcp_bridge.broker import MCPBroker

        return MCPBroker(api_key, api_secret, sandbox)
    else:
        logger.warning(f"Unknown broker '{broker_name}', using mock broker")
        return MockBrokerAPI(api_key, api_secret, sandbox)

if __name__ == "__main__":
    # Test the broker API
    print("Broker API Test")
    print("=" * 20)
    
    # Test mock broker
    mock_broker = MockBrokerAPI("test_key", "test_secret")
    
    if mock_broker.connect():
        print("Mock broker connected")
        
        # Test order placement
        result = mock_broker.place_order("BTCUSDT", "buy", 0.1, "market", 50000.0)
        print(f"Order result: {result.success}")
        
        # Test account info
        account = mock_broker.get_account_info()
        print(f"Balance: ${account.balance:.2f}")
        
        mock_broker.disconnect()
    
    print("\nBroker API test completed")
