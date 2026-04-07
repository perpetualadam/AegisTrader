"""
Asset management system for AegisTrader.
Handles crypto, UK stocks, and commodities with TradingView ticker support.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from enum import Enum
import json
import logging
from pathlib import Path

from market_sessions import MarketType

logger = logging.getLogger(__name__)

@dataclass
class Asset:
    """Represents a tradeable asset."""
    symbol: str
    name: str
    market_type: MarketType
    tradingview_ticker: str
    exchange: str
    sector: Optional[str] = None
    min_price_increment: float = 0.01
    min_quantity: float = 0.001
    is_active: bool = True

class AssetManager:
    """Manages all tradeable assets and their configurations."""
    
    def __init__(self, assets_file: Optional[str] = None):
        self.assets: Dict[str, Asset] = {}
        self.assets_by_market: Dict[MarketType, List[Asset]] = {
            market_type: [] for market_type in MarketType
        }
        
        # Load default assets
        self._load_default_assets()
        
        # Load custom assets if file provided
        if assets_file:
            self._load_assets_from_file(assets_file)
    
    def _load_default_assets(self):
        """Load default asset configurations."""
        
        # Cryptocurrency assets
        crypto_assets = [
            Asset("BTC", "Bitcoin", MarketType.CRYPTO, "BINANCE:BTCUSDT", "Binance"),
            Asset("ETH", "Ethereum", MarketType.CRYPTO, "BINANCE:ETHUSDT", "Binance"),
            Asset("ADA", "Cardano", MarketType.CRYPTO, "BINANCE:ADAUSDT", "Binance"),
            Asset("SOL", "Solana", MarketType.CRYPTO, "BINANCE:SOLUSDT", "Binance"),
            Asset("MATIC", "Polygon", MarketType.CRYPTO, "BINANCE:MATICUSDT", "Binance"),
            Asset("DOT", "Polkadot", MarketType.CRYPTO, "BINANCE:DOTUSDT", "Binance"),
            Asset("AVAX", "Avalanche", MarketType.CRYPTO, "BINANCE:AVAXUSDT", "Binance"),
            Asset("LINK", "Chainlink", MarketType.CRYPTO, "BINANCE:LINKUSDT", "Binance"),
            Asset("UNI", "Uniswap", MarketType.CRYPTO, "BINANCE:UNIUSDT", "Binance"),
            Asset("LTC", "Litecoin", MarketType.CRYPTO, "BINANCE:LTCUSDT", "Binance"),
        ]
        
        # UK Stock assets (FTSE 100 major components)
        uk_stock_assets = [
            Asset("LLOY", "Lloyds Banking Group", MarketType.STOCKS, "LSE:LLOY", "LSE", "Banking"),
            Asset("BARC", "Barclays", MarketType.STOCKS, "LSE:BARC", "LSE", "Banking"),
            Asset("VOD", "Vodafone Group", MarketType.STOCKS, "LSE:VOD", "LSE", "Telecommunications"),
            Asset("BP", "BP", MarketType.STOCKS, "LSE:BP", "LSE", "Energy"),
            Asset("SHEL", "Shell", MarketType.STOCKS, "LSE:SHEL", "LSE", "Energy"),
            Asset("AZN", "AstraZeneca", MarketType.STOCKS, "LSE:AZN", "LSE", "Healthcare"),
            Asset("ULVR", "Unilever", MarketType.STOCKS, "LSE:ULVR", "LSE", "Consumer Goods"),
            Asset("TSCO", "Tesco", MarketType.STOCKS, "LSE:TSCO", "LSE", "Retail"),
            Asset("RIO", "Rio Tinto", MarketType.STOCKS, "LSE:RIO", "LSE", "Mining"),
            Asset("BT.A", "BT Group", MarketType.STOCKS, "LSE:BT.A", "LSE", "Telecommunications"),
        ]
        
        # Commodities assets
        commodity_assets = [
            Asset("GOLD", "Gold", MarketType.COMMODITIES, "TVC:GOLD", "COMEX", "Precious Metals"),
            Asset("SILVER", "Silver", MarketType.COMMODITIES, "TVC:SILVER", "COMEX", "Precious Metals"),
            Asset("OIL", "Crude Oil WTI", MarketType.COMMODITIES, "NYMEX:CL1!", "NYMEX", "Energy"),
            Asset("BRENT", "Brent Oil", MarketType.COMMODITIES, "ICE:BRN1!", "ICE", "Energy"),
            Asset("NATGAS", "Natural Gas", MarketType.COMMODITIES, "NYMEX:NG1!", "NYMEX", "Energy"),
            Asset("COPPER", "Copper", MarketType.COMMODITIES, "COMEX:HG1!", "COMEX", "Industrial Metals"),
            Asset("WHEAT", "Wheat", MarketType.COMMODITIES, "CBOT:ZW1!", "CBOT", "Agriculture"),
            Asset("CORN", "Corn", MarketType.COMMODITIES, "CBOT:ZC1!", "CBOT", "Agriculture"),
            Asset("COFFEE", "Coffee", MarketType.COMMODITIES, "ICE:KC1!", "ICE", "Agriculture"),
            Asset("SUGAR", "Sugar", MarketType.COMMODITIES, "ICE:SB1!", "ICE", "Agriculture"),
        ]
        
        # Add all assets
        all_assets = crypto_assets + uk_stock_assets + commodity_assets
        
        for asset in all_assets:
            self.add_asset(asset)
    
    def add_asset(self, asset: Asset):
        """Add an asset to the manager."""
        self.assets[asset.symbol] = asset
        self.assets_by_market[asset.market_type].append(asset)
        logger.info(f"Added asset: {asset.symbol} ({asset.name})")
    
    def remove_asset(self, symbol: str):
        """Remove an asset from the manager."""
        if symbol in self.assets:
            asset = self.assets[symbol]
            del self.assets[symbol]
            self.assets_by_market[asset.market_type].remove(asset)
            logger.info(f"Removed asset: {symbol}")
    
    def get_asset(self, symbol: str) -> Optional[Asset]:
        """Get an asset by symbol."""
        return self.assets.get(symbol)
    
    def get_assets_by_market(self, market_type: MarketType) -> List[Asset]:
        """Get all assets for a specific market type."""
        return [asset for asset in self.assets_by_market[market_type] if asset.is_active]
    
    def get_active_assets(self) -> List[Asset]:
        """Get all active assets."""
        return [asset for asset in self.assets.values() if asset.is_active]
    
    def get_assets_by_sector(self, sector: str) -> List[Asset]:
        """Get all assets in a specific sector."""
        return [asset for asset in self.assets.values() 
                if asset.sector == sector and asset.is_active]
    
    def get_tradingview_tickers(self, market_types: Optional[List[MarketType]] = None) -> List[str]:
        """Get TradingView tickers for specified market types."""
        if market_types is None:
            market_types = list(MarketType)
        
        tickers = []
        for market_type in market_types:
            for asset in self.get_assets_by_market(market_type):
                tickers.append(asset.tradingview_ticker)
        
        return tickers
    
    def search_assets(self, query: str) -> List[Asset]:
        """Search assets by symbol or name."""
        query = query.lower()
        results = []
        
        for asset in self.assets.values():
            if (query in asset.symbol.lower() or 
                query in asset.name.lower() or
                (asset.sector and query in asset.sector.lower())):
                results.append(asset)
        
        return results
    
    def get_market_summary(self) -> Dict:
        """Get summary of assets by market type."""
        summary = {}
        
        for market_type in MarketType:
            assets = self.get_assets_by_market(market_type)
            summary[market_type.value] = {
                'count': len(assets),
                'symbols': [asset.symbol for asset in assets[:10]],  # First 10
                'sectors': list(set(asset.sector for asset in assets if asset.sector))
            }
        
        return summary
    
    def _load_assets_from_file(self, file_path: str):
        """Load assets from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            for asset_data in data.get('assets', []):
                asset = Asset(
                    symbol=asset_data['symbol'],
                    name=asset_data['name'],
                    market_type=MarketType(asset_data['market_type']),
                    tradingview_ticker=asset_data['tradingview_ticker'],
                    exchange=asset_data['exchange'],
                    sector=asset_data.get('sector'),
                    min_price_increment=asset_data.get('min_price_increment', 0.01),
                    min_quantity=asset_data.get('min_quantity', 0.001),
                    is_active=asset_data.get('is_active', True)
                )
                self.add_asset(asset)
            
            logger.info(f"Loaded {len(data.get('assets', []))} assets from {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to load assets from {file_path}: {e}")
    
    def save_assets_to_file(self, file_path: str):
        """Save current assets to a JSON file."""
        try:
            data = {
                'assets': [
                    {
                        'symbol': asset.symbol,
                        'name': asset.name,
                        'market_type': asset.market_type.value,
                        'tradingview_ticker': asset.tradingview_ticker,
                        'exchange': asset.exchange,
                        'sector': asset.sector,
                        'min_price_increment': asset.min_price_increment,
                        'min_quantity': asset.min_quantity,
                        'is_active': asset.is_active
                    }
                    for asset in self.assets.values()
                ]
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {len(self.assets)} assets to {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to save assets to {file_path}: {e}")

# Global asset manager instance
asset_manager = AssetManager()

def get_tradeable_assets(market_types: Optional[List[MarketType]] = None) -> List[Asset]:
    """Get all tradeable assets for specified market types."""
    if market_types is None:
        return asset_manager.get_active_assets()
    
    assets = []
    for market_type in market_types:
        assets.extend(asset_manager.get_assets_by_market(market_type))
    
    return assets

def get_asset_by_symbol(symbol: str) -> Optional[Asset]:
    """Get an asset by its symbol."""
    return asset_manager.get_asset(symbol)

if __name__ == "__main__":
    # Test the asset management functionality
    print("Asset Management System")
    print("=" * 40)
    
    summary = asset_manager.get_market_summary()
    
    for market, info in summary.items():
        print(f"\n{market.upper()}:")
        print(f"  Count: {info['count']}")
        print(f"  Sample symbols: {', '.join(info['symbols'])}")
        if info['sectors']:
            print(f"  Sectors: {', '.join(info['sectors'])}")
    
    print(f"\nTotal active assets: {len(asset_manager.get_active_assets())}")
    
    # Test search
    search_results = asset_manager.search_assets("gold")
    print(f"\nSearch results for 'gold': {[asset.symbol for asset in search_results]}")
