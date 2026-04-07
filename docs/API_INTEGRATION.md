# 🔗 AegisTrader API Integration Guide

Complete guide for integrating AegisTrader with various broker APIs and exchanges.

## 📋 Table of Contents

- [Overview](#overview)
- [Broker API Architecture](#broker-api-architecture)
- [Adding New Brokers](#adding-new-brokers)
- [Binance Integration](#binance-integration)
- [Alpaca Integration](#alpaca-integration)
- [Interactive Brokers Integration](#interactive-brokers-integration)
- [API Authentication](#api-authentication)
- [Testing and Sandbox](#testing-and-sandbox)
- [Rate Limiting](#rate-limiting)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## 🏗️ Overview

AegisTrader uses an abstract broker API interface that allows easy integration with multiple trading platforms. The system supports both paper trading (simulation) and live trading modes.

### Supported Brokers

| Broker | Status | Markets | Sandbox |
|--------|--------|---------|---------|
| Mock Broker | ✅ Complete | All | Yes |
| Binance | 🚧 Template | Crypto | Yes |
| Alpaca | 🚧 Template | US Stocks | Yes |
| Interactive Brokers | 🚧 Template | Global | Yes |
| CCXT (Multi-Exchange) | 📋 Planned | Crypto | Varies |

## 🏛️ Broker API Architecture

### Base Interface

All broker implementations inherit from the `BrokerAPI` abstract base class:

```python
# broker/broker_api.py
from abc import ABC, abstractmethod

class BrokerAPI(ABC):
    """Abstract base class for broker API implementations."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to the broker API."""
        pass
    
    @abstractmethod
    def place_order(self, symbol: str, side: str, quantity: float, 
                   order_type: str = "market", price: Optional[float] = None) -> OrderResult:
        """Place a trading order."""
        pass
    
    @abstractmethod
    def get_account_info(self) -> AccountInfo:
        """Get account information."""
        pass
    
    # ... other required methods
```

### Data Structures

**OrderResult**:
```python
@dataclass
class OrderResult:
    success: bool
    order_id: Optional[str] = None
    status: Optional[str] = None
    fill_price: Optional[float] = None
    filled_quantity: Optional[float] = None
    fees: Optional[float] = None
    error_message: Optional[str] = None
    timestamp: float = 0.0
```

**AccountInfo**:
```python
@dataclass
class AccountInfo:
    balance: float
    available_balance: float
    positions: List[Dict] = None
    margin_used: float = 0.0
    margin_available: float = 0.0
```

## 🔧 Adding New Brokers

### Step 1: Create Broker Class

Create a new file `broker/your_broker_api.py`:

```python
from .broker_api import BrokerAPI, OrderResult, AccountInfo
import logging

logger = logging.getLogger(__name__)

class YourBrokerAPI(BrokerAPI):
    """Your broker API implementation."""
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        super().__init__(api_key, api_secret, sandbox)
        self.client = None
        
    def connect(self) -> bool:
        """Connect to your broker API."""
        try:
            # Initialize your broker's client
            # self.client = YourBrokerClient(self.api_key, self.api_secret, sandbox=self.sandbox)
            
            # Test connection
            # account_info = self.client.get_account()
            
            self.is_connected = True
            logger.info("Connected to Your Broker API")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Your Broker: {e}")
            return False
    
    def place_order(self, symbol: str, side: str, quantity: float, 
                   order_type: str = "market", price: Optional[float] = None) -> OrderResult:
        """Place order with your broker."""
        if not self.is_connected:
            return OrderResult(
                success=False,
                error_message="Not connected to broker",
                timestamp=time.time()
            )
        
        try:
            # Convert AegisTrader format to broker format
            broker_symbol = self._convert_symbol(symbol)
            broker_side = self._convert_side(side)
            broker_order_type = self._convert_order_type(order_type)
            
            # Place order with broker
            # result = self.client.place_order(
            #     symbol=broker_symbol,
            #     side=broker_side,
            #     type=broker_order_type,
            #     quantity=quantity,
            #     price=price
            # )
            
            # Convert broker response to AegisTrader format
            return OrderResult(
                success=True,
                order_id=result.get('orderId'),
                status=self._convert_status(result.get('status')),
                fill_price=float(result.get('fills', [{}])[0].get('price', 0)),
                filled_quantity=float(result.get('executedQty', 0)),
                fees=float(result.get('fills', [{}])[0].get('commission', 0)),
                timestamp=time.time()
            )
            
        except Exception as e:
            logger.error(f"Order placement failed: {e}")
            return OrderResult(
                success=False,
                error_message=str(e),
                timestamp=time.time()
            )
    
    def _convert_symbol(self, symbol: str) -> str:
        """Convert AegisTrader symbol to broker format."""
        # Example: BTCUSDT -> BTC/USDT
        return symbol  # Implement conversion logic
    
    def _convert_side(self, side: str) -> str:
        """Convert side to broker format."""
        return side.upper()  # Most brokers use uppercase
    
    def _convert_order_type(self, order_type: str) -> str:
        """Convert order type to broker format."""
        type_mapping = {
            'market': 'MARKET',
            'limit': 'LIMIT',
            'stop': 'STOP_LOSS',
            'stop_limit': 'STOP_LOSS_LIMIT'
        }
        return type_mapping.get(order_type, 'MARKET')
    
    def _convert_status(self, broker_status: str) -> str:
        """Convert broker status to AegisTrader format."""
        status_mapping = {
            'NEW': 'pending',
            'FILLED': 'filled',
            'PARTIALLY_FILLED': 'partially_filled',
            'CANCELED': 'cancelled',
            'REJECTED': 'rejected'
        }
        return status_mapping.get(broker_status, 'unknown')
    
    # Implement other required methods...
```

### Step 2: Update Factory Function

Add your broker to the factory function in `broker/broker_api.py`:

```python
def create_broker_api(broker_name: str, api_key: str, api_secret: str, 
                     sandbox: bool = True) -> BrokerAPI:
    """Factory function to create broker API instances."""
    broker_name = broker_name.lower()
    
    if broker_name == 'mock':
        return MockBrokerAPI(api_key, api_secret, sandbox)
    elif broker_name == 'binance':
        return BinanceBrokerAPI(api_key, api_secret, sandbox)
    elif broker_name == 'your_broker':
        from .your_broker_api import YourBrokerAPI
        return YourBrokerAPI(api_key, api_secret, sandbox)
    else:
        logger.warning(f"Unknown broker '{broker_name}', using mock broker")
        return MockBrokerAPI(api_key, api_secret, sandbox)
```

### Step 3: Configuration

Add broker configuration to `.env`:

```env
BROKER_NAME=your_broker
BROKER_API_KEY=your_api_key
BROKER_API_SECRET=your_api_secret
BROKER_SANDBOX=true
```

## 🟡 Binance Integration

### Installation

```bash
pip install python-binance
```

### Implementation

```python
# broker/binance_api.py
from binance.client import Client
from binance.exceptions import BinanceAPIException
from .broker_api import BrokerAPI, OrderResult, AccountInfo

class BinanceBrokerAPI(BrokerAPI):
    """Binance API implementation."""
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        super().__init__(api_key, api_secret, sandbox)
        self.client = None
        
    def connect(self) -> bool:
        """Connect to Binance API."""
        try:
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=self.sandbox
            )
            
            # Test connection
            account_info = self.client.get_account()
            
            self.is_connected = True
            logger.info(f"Connected to Binance {'Testnet' if self.sandbox else 'Mainnet'}")
            return True
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to connect to Binance: {e}")
            return False
    
    def place_order(self, symbol: str, side: str, quantity: float, 
                   order_type: str = "market", price: Optional[float] = None) -> OrderResult:
        """Place order on Binance."""
        try:
            order_params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity
            }
            
            if order_type.lower() == 'limit' and price:
                order_params['price'] = str(price)
                order_params['timeInForce'] = 'GTC'
            
            result = self.client.create_order(**order_params)
            
            return OrderResult(
                success=True,
                order_id=str(result['orderId']),
                status=self._convert_status(result['status']),
                fill_price=float(result.get('fills', [{}])[0].get('price', 0)),
                filled_quantity=float(result.get('executedQty', 0)),
                fees=sum(float(fill.get('commission', 0)) for fill in result.get('fills', [])),
                timestamp=result['transactTime'] / 1000
            )
            
        except BinanceAPIException as e:
            return OrderResult(
                success=False,
                error_message=f"Binance API error: {e.message}",
                timestamp=time.time()
            )
    
    def get_account_info(self) -> AccountInfo:
        """Get Binance account information."""
        try:
            account = self.client.get_account()
            
            # Calculate total balance in USDT
            total_balance = 0.0
            available_balance = 0.0
            
            for balance in account['balances']:
                if float(balance['free']) > 0 or float(balance['locked']) > 0:
                    asset = balance['asset']
                    free = float(balance['free'])
                    locked = float(balance['locked'])
                    
                    if asset == 'USDT':
                        total_balance += free + locked
                        available_balance += free
                    else:
                        # Convert to USDT using current price
                        try:
                            ticker = self.client.get_symbol_ticker(symbol=f"{asset}USDT")
                            price = float(ticker['price'])
                            total_balance += (free + locked) * price
                            available_balance += free * price
                        except:
                            pass  # Skip if conversion fails
            
            return AccountInfo(
                balance=total_balance,
                available_balance=available_balance,
                positions=[],
                margin_used=0.0,
                margin_available=available_balance
            )
            
        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            return AccountInfo(balance=0.0, available_balance=0.0)
```

### Binance Configuration

```env
BROKER_NAME=binance
BROKER_API_KEY=your_binance_api_key
BROKER_API_SECRET=your_binance_api_secret
BROKER_SANDBOX=true  # Use testnet

# Binance-specific settings
BINANCE_TESTNET_URL=https://testnet.binance.vision
BINANCE_RECV_WINDOW=5000
```

## 🇺🇸 Alpaca Integration

### Installation

```bash
pip install alpaca-trade-api
```

### Implementation

```python
# broker/alpaca_api.py
import alpaca_trade_api as tradeapi
from .broker_api import BrokerAPI, OrderResult, AccountInfo

class AlpacaBrokerAPI(BrokerAPI):
    """Alpaca API implementation for US stocks."""
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        super().__init__(api_key, api_secret, sandbox)
        self.api = None
        
    def connect(self) -> bool:
        """Connect to Alpaca API."""
        try:
            base_url = 'https://paper-api.alpaca.markets' if self.sandbox else 'https://api.alpaca.markets'
            
            self.api = tradeapi.REST(
                key_id=self.api_key,
                secret_key=self.api_secret,
                base_url=base_url,
                api_version='v2'
            )
            
            # Test connection
            account = self.api.get_account()
            
            self.is_connected = True
            logger.info(f"Connected to Alpaca {'Paper' if self.sandbox else 'Live'} Trading")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Alpaca: {e}")
            return False
    
    def place_order(self, symbol: str, side: str, quantity: float, 
                   order_type: str = "market", price: Optional[float] = None) -> OrderResult:
        """Place order with Alpaca."""
        try:
            order_params = {
                'symbol': symbol,
                'qty': quantity,
                'side': side,
                'type': order_type,
                'time_in_force': 'day'
            }
            
            if order_type == 'limit' and price:
                order_params['limit_price'] = price
            
            order = self.api.submit_order(**order_params)
            
            return OrderResult(
                success=True,
                order_id=order.id,
                status=order.status,
                fill_price=float(order.filled_avg_price or 0),
                filled_quantity=float(order.filled_qty or 0),
                fees=0.0,  # Alpaca has commission-free trading
                timestamp=order.submitted_at.timestamp()
            )
            
        except Exception as e:
            return OrderResult(
                success=False,
                error_message=str(e),
                timestamp=time.time()
            )
    
    def get_account_info(self) -> AccountInfo:
        """Get Alpaca account information."""
        try:
            account = self.api.get_account()
            
            return AccountInfo(
                balance=float(account.equity),
                available_balance=float(account.buying_power),
                positions=[],
                margin_used=0.0,
                margin_available=float(account.buying_power)
            )
            
        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            return AccountInfo(balance=0.0, available_balance=0.0)
```

### Alpaca Configuration

```env
BROKER_NAME=alpaca
BROKER_API_KEY=your_alpaca_key_id
BROKER_API_SECRET=your_alpaca_secret_key
BROKER_SANDBOX=true  # Use paper trading

# Alpaca-specific settings
ALPACA_PAPER_URL=https://paper-api.alpaca.markets
ALPACA_LIVE_URL=https://api.alpaca.markets
```

## 🏦 Interactive Brokers Integration

### Installation

```bash
pip install ib-insync
```

### Implementation

```python
# broker/ib_api.py
from ib_insync import IB, Stock, MarketOrder, LimitOrder
from .broker_api import BrokerAPI, OrderResult, AccountInfo

class IBBrokerAPI(BrokerAPI):
    """Interactive Brokers API implementation."""
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        super().__init__(api_key, api_secret, sandbox)
        self.ib = IB()
        self.port = 7497 if sandbox else 7496  # TWS demo vs live
        
    def connect(self) -> bool:
        """Connect to Interactive Brokers TWS/Gateway."""
        try:
            self.ib.connect('127.0.0.1', self.port, clientId=1)
            
            self.is_connected = True
            logger.info(f"Connected to IB {'Paper' if self.sandbox else 'Live'} Trading")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to IB: {e}")
            return False
    
    def place_order(self, symbol: str, side: str, quantity: float, 
                   order_type: str = "market", price: Optional[float] = None) -> OrderResult:
        """Place order with Interactive Brokers."""
        try:
            # Create contract
            contract = Stock(symbol, 'SMART', 'USD')
            
            # Create order
            if order_type.lower() == 'market':
                order = MarketOrder(side.upper(), quantity)
            elif order_type.lower() == 'limit':
                order = LimitOrder(side.upper(), quantity, price)
            else:
                raise ValueError(f"Unsupported order type: {order_type}")
            
            # Place order
            trade = self.ib.placeOrder(contract, order)
            
            return OrderResult(
                success=True,
                order_id=str(trade.order.orderId),
                status=trade.orderStatus.status,
                fill_price=trade.orderStatus.avgFillPrice,
                filled_quantity=trade.orderStatus.filled,
                fees=0.0,  # Will be updated when filled
                timestamp=time.time()
            )
            
        except Exception as e:
            return OrderResult(
                success=False,
                error_message=str(e),
                timestamp=time.time()
            )
    
    def disconnect(self):
        """Disconnect from IB."""
        if self.ib.isConnected():
            self.ib.disconnect()
        self.is_connected = False
```

## 🔐 API Authentication

### Secure Credential Storage

**Environment Variables**:
```bash
# .env
BROKER_API_KEY=your_api_key
BROKER_API_SECRET=your_api_secret

# Additional security
BROKER_PASSPHRASE=your_passphrase  # For some exchanges
BROKER_SANDBOX=true
```

**Cloud Secret Management**:
```python
# utils/secrets.py
import boto3
import json

def get_broker_credentials(secret_name: str):
    """Get broker credentials from AWS Secrets Manager."""
    client = boto3.client('secretsmanager')
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        return secret['api_key'], secret['api_secret']
    except Exception as e:
        logger.error(f"Failed to get credentials: {e}")
        return None, None
```

### API Key Permissions

**Binance Permissions**:
- ✅ Enable Reading
- ✅ Enable Spot & Margin Trading
- ❌ Enable Withdrawals (not needed)
- ✅ Restrict access to trusted IPs

**Alpaca Permissions**:
- ✅ Account Data
- ✅ Trading
- ❌ Account Configuration

**Interactive Brokers**:
- Configure TWS/Gateway for API access
- Set trusted IP addresses
- Enable paper trading for testing

## 🧪 Testing and Sandbox

### Sandbox Testing

```python
# tests/test_broker_integration.py
import pytest
from broker.broker_api import create_broker_api

def test_broker_connection():
    """Test broker connection in sandbox mode."""
    broker = create_broker_api('binance', 'test_key', 'test_secret', sandbox=True)
    
    # Should connect to testnet
    assert broker.connect() == True
    assert broker.is_connected == True

def test_order_placement():
    """Test order placement in sandbox."""
    broker = create_broker_api('mock', 'test', 'test')
    broker.connect()
    
    result = broker.place_order('BTCUSDT', 'buy', 0.001, 'market', 50000.0)
    
    assert result.success == True
    assert result.order_id is not None

def test_account_info():
    """Test account information retrieval."""
    broker = create_broker_api('mock', 'test', 'test')
    broker.connect()
    
    account = broker.get_account_info()
    
    assert account.balance >= 0
    assert account.available_balance >= 0
```

### Integration Testing

```python
# tests/test_live_integration.py
@pytest.mark.integration
def test_live_broker_connection():
    """Test connection to live broker (requires valid credentials)."""
    api_key = os.getenv('BROKER_API_KEY')
    api_secret = os.getenv('BROKER_API_SECRET')
    
    if not api_key or not api_secret:
        pytest.skip("Live broker credentials not provided")
    
    broker = create_broker_api('binance', api_key, api_secret, sandbox=True)
    assert broker.connect() == True
```

## ⏱️ Rate Limiting

### Implementation

```python
# utils/rate_limiter.py
import time
from collections import defaultdict, deque

class RateLimiter:
    """Rate limiter for API calls."""
    
    def __init__(self):
        self.calls = defaultdict(deque)
        self.limits = {
            'binance': {'requests_per_minute': 1200, 'orders_per_second': 10},
            'alpaca': {'requests_per_minute': 200, 'orders_per_minute': 200},
            'ib': {'requests_per_second': 50}
        }
    
    def can_make_request(self, broker: str, request_type: str = 'general') -> bool:
        """Check if request can be made without hitting rate limit."""
        now = time.time()
        limit_key = f"{broker}_{request_type}"
        
        # Clean old requests
        while self.calls[limit_key] and self.calls[limit_key][0] < now - 60:
            self.calls[limit_key].popleft()
        
        # Check limit
        limit = self.limits.get(broker, {}).get(f"{request_type}_per_minute", 100)
        return len(self.calls[limit_key]) < limit
    
    def record_request(self, broker: str, request_type: str = 'general'):
        """Record a request."""
        limit_key = f"{broker}_{request_type}"
        self.calls[limit_key].append(time.time())

# Global rate limiter
rate_limiter = RateLimiter()
```

### Usage in Broker APIs

```python
def place_order(self, symbol: str, side: str, quantity: float, 
               order_type: str = "market", price: Optional[float] = None) -> OrderResult:
    """Place order with rate limiting."""
    
    # Check rate limit
    if not rate_limiter.can_make_request('binance', 'orders'):
        return OrderResult(
            success=False,
            error_message="Rate limit exceeded",
            timestamp=time.time()
        )
    
    try:
        # Place order
        result = self.client.create_order(...)
        
        # Record request
        rate_limiter.record_request('binance', 'orders')
        
        return OrderResult(success=True, ...)
        
    except Exception as e:
        return OrderResult(success=False, error_message=str(e))
```

## 🚨 Error Handling

### Common Error Types

```python
# broker/exceptions.py
class BrokerError(Exception):
    """Base broker error."""
    pass

class ConnectionError(BrokerError):
    """Connection-related errors."""
    pass

class AuthenticationError(BrokerError):
    """Authentication failures."""
    pass

class InsufficientFundsError(BrokerError):
    """Insufficient balance for trade."""
    pass

class RateLimitError(BrokerError):
    """Rate limit exceeded."""
    pass

class OrderError(BrokerError):
    """Order placement/management errors."""
    pass
```

### Error Handling Strategy

```python
def place_order_with_retry(self, symbol: str, side: str, quantity: float, 
                          order_type: str = "market", price: Optional[float] = None,
                          max_retries: int = 3) -> OrderResult:
    """Place order with retry logic."""
    
    for attempt in range(max_retries):
        try:
            result = self.place_order(symbol, side, quantity, order_type, price)
            
            if result.success:
                return result
            
            # Handle specific errors
            if "rate limit" in result.error_message.lower():
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"Rate limit hit, waiting {wait_time}s before retry")
                time.sleep(wait_time)
                continue
            
            if "insufficient" in result.error_message.lower():
                logger.error("Insufficient funds, not retrying")
                return result
            
            # Generic retry for other errors
            if attempt < max_retries - 1:
                logger.warning(f"Order failed (attempt {attempt + 1}), retrying: {result.error_message}")
                time.sleep(1)
            
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                return OrderResult(
                    success=False,
                    error_message=f"Failed after {max_retries} attempts: {str(e)}",
                    timestamp=time.time()
                )
    
    return result
```

## 🎯 Best Practices

### 1. Security

- **Never commit API keys** to version control
- **Use environment variables** or secure secret management
- **Enable IP whitelisting** when available
- **Use sandbox/testnet** for development and testing
- **Rotate API keys** regularly

### 2. Error Handling

- **Implement retry logic** with exponential backoff
- **Handle rate limits** gracefully
- **Log all API interactions** for debugging
- **Validate responses** before processing
- **Have fallback mechanisms** for critical operations

### 3. Performance

- **Implement connection pooling** for high-frequency trading
- **Cache account information** when appropriate
- **Use websockets** for real-time data when available
- **Batch operations** when possible
- **Monitor API quotas** and usage

### 4. Testing

- **Always test in sandbox** before live trading
- **Unit test all broker methods**
- **Integration test with real APIs**
- **Test error scenarios** and edge cases
- **Validate order execution** and fills

### 5. Monitoring

- **Log all trades** and API calls
- **Monitor API health** and response times
- **Set up alerts** for failures
- **Track API quota usage**
- **Monitor account balances** and positions

### Example Configuration

```env
# Complete broker configuration example
BROKER_NAME=binance
BROKER_API_KEY=your_api_key
BROKER_API_SECRET=your_api_secret
BROKER_SANDBOX=true

# Rate limiting
BROKER_MAX_REQUESTS_PER_MINUTE=1000
BROKER_MAX_ORDERS_PER_SECOND=5

# Error handling
BROKER_MAX_RETRIES=3
BROKER_RETRY_DELAY=1
BROKER_TIMEOUT=30

# Monitoring
BROKER_LOG_ALL_REQUESTS=true
BROKER_HEALTH_CHECK_INTERVAL=300
```

This guide provides a comprehensive framework for integrating AegisTrader with various broker APIs while maintaining security, reliability, and performance.
