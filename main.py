"""
AegisTrader - Vision-Based Trading Bot
Main application entry point with startup warnings and mode selection.
"""

import sys
import time
import signal
import logging
from typing import List
from pathlib import Path

# Import configuration and validation
from config import (
    validate_config, show_live_trading_warning, get_config_summary,
    LIVE_TRADING, DEFAULT_MARKETS, SCAN_INTERVAL
)

# Import core modules
from market_sessions import MarketSession, MarketType, get_active_markets
from assets import AssetManager, get_tradeable_assets
from scanner.market_scanner import MarketScanner, get_market_scanner
from strategy.strategy_engine import StrategyEngine, get_strategy_engine
from execution.execution import Execution, get_execution_engine
from risk.risk_manager import RiskManager, get_risk_manager
from utils.logger import get_logger
from utils.tts_feedback import get_tts_feedback

# Global instances
logger = None
scanner = None
strategy_engine = None
execution_engine = None
risk_manager = None
tts_feedback = None
running = False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global running
    print("\nShutdown signal received. Stopping AegisTrader...")
    running = False

def initialize_system():
    """Initialize all system components."""
    global logger, scanner, strategy_engine, execution_engine, risk_manager, tts_feedback
    
    print("Initializing AegisTrader components...")
    
    # Initialize logger first
    logger = get_logger()
    logger.info("Starting AegisTrader initialization")
    
    # Initialize TTS feedback
    tts_feedback = get_tts_feedback()
    tts_feedback.announce_system_status("Initializing AegisTrader")
    
    # Initialize market scanner
    scanner = get_market_scanner()
    logger.info("Market scanner initialized")
    
    # Initialize strategy engine
    strategy_engine = get_strategy_engine()
    logger.info("Strategy engine initialized")
    
    # Initialize execution engine
    execution_engine = get_execution_engine()
    logger.info("Execution engine initialized")
    
    # Initialize risk manager
    risk_manager = get_risk_manager()
    logger.info("Risk manager initialized")
    
    logger.info("All components initialized successfully")
    return True

def display_startup_info():
    """Display startup information and configuration."""
    print("\n" + "="*60)
    print("🛡️  AEGIS TRADER - Vision-Based Trading Bot")
    print("="*60)
    
    config = get_config_summary()
    print(f"Trading Mode: {config['trading_mode']}")
    print(f"Markets: {', '.join(config['markets'])}")
    print(f"Browser: {config['browser_type']} ({'headless' if config['headless_browser'] else 'visible'})")
    print(f"Max Position Size: {config['max_position_size']*100:.1f}%")
    print(f"Max Daily Loss: {config['max_daily_loss']*100:.1f}%")
    print(f"TTS Enabled: {config['tts_enabled']}")
    print(f"Scan Interval: {config['scan_interval']}s")
    print("="*60)

def display_market_status():
    """Display current market status."""
    market_session = MarketSession()
    session_info = market_session.get_trading_session_info()
    
    print(f"\n📊 Market Status ({session_info['current_time_uk']})")
    print("-" * 40)
    
    for market, details in session_info['markets'].items():
        status = "🟢 OPEN" if details['is_open'] else "🔴 CLOSED"
        print(f"{market.upper()}: {status}")
        
        if not details['is_open'] and details['next_open']:
            print(f"  Next open: {details['next_open']}")
    
    if session_info['is_uk_holiday']:
        print("⚠️  UK Holiday - Traditional markets may be affected")

def run_trading_loop():
    """Main trading loop."""
    global running
    
    logger.info("Starting main trading loop")
    tts_feedback.announce_system_status("Trading loop started")
    
    # Get tradeable assets for active markets
    active_market_types = [MarketType(market) for market in DEFAULT_MARKETS]
    assets = get_tradeable_assets(active_market_types)
    
    if not assets:
        logger.error("No tradeable assets found")
        return
    
    logger.info(f"Monitoring {len(assets)} assets across {len(active_market_types)} markets")
    
    # Start continuous scanning
    scanner.start_continuous_scanning(assets, SCAN_INTERVAL)
    
    try:
        while running:
            # Get latest opportunities
            opportunities = scanner.find_best_opportunities()
            
            if opportunities:
                logger.info(f"Found {len(opportunities)} trading opportunities")
                
                # Process each opportunity
                for opportunity in opportunities:
                    if not running:
                        break
                    
                    # Get scan result for detailed analysis
                    scan_result = scanner.scan_results.get(opportunity.asset.symbol)
                    if not scan_result:
                        continue
                    
                    # Generate trading signal
                    signal = strategy_engine.analyze_opportunity(opportunity, scan_result)
                    
                    if signal:
                        # Validate with risk manager
                        portfolio_summary = execution_engine.get_portfolio_summary()
                        positions = execution_engine.get_positions()
                        
                        validation = risk_manager.validate_signal(
                            signal, 
                            portfolio_summary['current_balance'],
                            {pos['symbol']: pos for pos in positions}
                        )
                        
                        if validation['approved']:
                            # Execute trade
                            order_id = execution_engine.place_order(signal, validation['position_size'])
                            
                            if order_id:
                                logger.info(f"Trade executed: {signal.signal_type.value} {signal.asset.symbol}")
                                tts_feedback.announce_trade(
                                    signal.asset.symbol,
                                    signal.signal_type.value,
                                    validation['position_size'],
                                    signal.entry_price
                                )
                            else:
                                logger.warning(f"Failed to execute trade for {signal.asset.symbol}")
                        else:
                            logger.info(f"Signal rejected by risk manager: {validation['warnings']}")
            
            # Update risk metrics
            portfolio_summary = execution_engine.get_portfolio_summary()
            risk_manager.update_daily_pnl(portfolio_summary['current_balance'])
            
            # Sleep before next iteration
            time.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Error in trading loop: {e}")
    finally:
        # Stop continuous scanning
        scanner.stop_continuous_scanning()
        logger.info("Trading loop stopped")

def display_final_summary():
    """Display final trading summary."""
    if execution_engine:
        summary = execution_engine.get_portfolio_summary()
        
        print("\n" + "="*50)
        print("📈 FINAL TRADING SUMMARY")
        print("="*50)
        print(f"Initial Balance: ${summary['initial_balance']:,.2f}")
        print(f"Final Balance: ${summary['current_balance']:,.2f}")
        print(f"Total Return: {summary['total_return']*100:+.2f}%")
        print(f"Total Trades: {summary['total_trades']}")
        print(f"Win Rate: {summary['win_rate']*100:.1f}%")
        print(f"Max Drawdown: {summary['max_drawdown']*100:.1f}%")
        print(f"Total Fees: ${summary['total_fees']:,.2f}")
        print("="*50)
        
        # Save final state
        timestamp = int(time.time())
        execution_engine.save_state(f"data/final_state_{timestamp}.json")

def main():
    """Main application entry point."""
    global running
    
    print("Starting AegisTrader...")
    
    # Validate configuration
    if not validate_config():
        print("❌ Configuration validation failed. Please check your settings.")
        sys.exit(1)
    
    # Show live trading warning if applicable
    if not show_live_trading_warning():
        print("Exiting AegisTrader.")
        sys.exit(0)
    
    # Display startup information
    display_startup_info()
    
    # Display market status
    display_market_status()
    
    # Initialize system components
    if not initialize_system():
        print("❌ System initialization failed.")
        sys.exit(1)
    
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start trading
    running = True
    
    try:
        print("\n🚀 Starting trading operations...")
        run_trading_loop()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
    
    finally:
        # Cleanup and final summary
        print("\n🛑 Shutting down AegisTrader...")
        
        if tts_feedback:
            tts_feedback.announce_system_status("AegisTrader shutting down")
            tts_feedback.stop_worker()
        
        display_final_summary()
        
        if logger:
            logger.info("AegisTrader shutdown complete")
        
        print("✅ AegisTrader shutdown complete.")

if __name__ == "__main__":
    main()
