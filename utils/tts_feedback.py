"""
Text-to-Speech feedback system for AegisTrader.
Audio notifications and trade confirmations.
"""

import logging
from typing import Optional
import threading
import queue
import time

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

from config import TTS_ENABLED, TTS_VOICE_RATE

logger = logging.getLogger(__name__)

class TTSFeedback:
    """Text-to-Speech feedback system."""
    
    def __init__(self):
        self.enabled = TTS_ENABLED and TTS_AVAILABLE
        self.engine = None
        self.voice_rate = TTS_VOICE_RATE
        self.message_queue = queue.Queue()
        self.worker_thread = None
        self.running = False
        
        if self.enabled:
            self.initialize_tts()
            self.start_worker()
        else:
            logger.warning("TTS not available or disabled")
    
    def initialize_tts(self) -> bool:
        """Initialize the TTS engine."""
        try:
            self.engine = pyttsx3.init()
            
            # Set voice properties
            self.engine.setProperty('rate', self.voice_rate)
            
            # Try to set a voice (optional)
            voices = self.engine.getProperty('voices')
            if voices:
                # Use first available voice
                self.engine.setProperty('voice', voices[0].id)
            
            logger.info("TTS engine initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
            self.enabled = False
            return False
    
    def start_worker(self):
        """Start the TTS worker thread."""
        if not self.enabled:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        logger.info("TTS worker thread started")
    
    def stop_worker(self):
        """Stop the TTS worker thread."""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
    
    def _worker_loop(self):
        """TTS worker thread loop."""
        while self.running:
            try:
                # Get message from queue with timeout
                message = self.message_queue.get(timeout=1)
                
                if message and self.engine:
                    self.engine.say(message)
                    self.engine.runAndWait()
                
                self.message_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"TTS worker error: {e}")
    
    def speak(self, message: str, priority: bool = False):
        """
        Add message to TTS queue.
        
        Args:
            message: Text to speak
            priority: If True, clear queue and speak immediately
        """
        if not self.enabled:
            return
        
        try:
            if priority:
                # Clear existing messages
                while not self.message_queue.empty():
                    try:
                        self.message_queue.get_nowait()
                    except queue.Empty:
                        break
            
            self.message_queue.put(message)
            logger.debug(f"TTS message queued: {message}")
            
        except Exception as e:
            logger.error(f"Error queuing TTS message: {e}")
    
    def announce_trade(self, symbol: str, action: str, quantity: float, price: float):
        """Announce a trade execution."""
        message = f"Trade executed: {action} {quantity:.4f} {symbol} at {price:.2f}"
        self.speak(message)
    
    def announce_signal(self, symbol: str, signal_type: str, confidence: float):
        """Announce a trading signal."""
        confidence_pct = int(confidence * 100)
        message = f"Signal: {signal_type} {symbol} with {confidence_pct} percent confidence"
        self.speak(message)
    
    def announce_profit(self, symbol: str, pnl: float):
        """Announce profit/loss."""
        if pnl > 0:
            message = f"Profit on {symbol}: {pnl:.2f} dollars"
        else:
            message = f"Loss on {symbol}: {abs(pnl):.2f} dollars"
        self.speak(message, priority=True)
    
    def announce_risk_event(self, event_type: str, description: str):
        """Announce risk management events."""
        message = f"Risk alert: {event_type}. {description}"
        self.speak(message, priority=True)
    
    def announce_market_status(self, status: str):
        """Announce market status changes."""
        message = f"Market status: {status}"
        self.speak(message)
    
    def announce_system_status(self, status: str):
        """Announce system status changes."""
        message = f"System status: {status}"
        self.speak(message, priority=True)
    
    def test_voice(self):
        """Test the TTS system."""
        self.speak("AegisTrader TTS system is working correctly", priority=True)

# Global TTS instance
tts_feedback = None

def get_tts_feedback() -> TTSFeedback:
    """Get the global TTS feedback instance."""
    global tts_feedback
    if tts_feedback is None:
        tts_feedback = TTSFeedback()
    return tts_feedback

if __name__ == "__main__":
    # Test TTS system
    print("Testing TTS Feedback System")
    print("=" * 30)
    
    tts = TTSFeedback()
    
    if tts.enabled:
        print("TTS is enabled")
        tts.test_voice()
        
        # Test various announcements
        time.sleep(2)
        tts.announce_signal("Bitcoin", "buy", 0.85)
        
        time.sleep(3)
        tts.announce_trade("BTCUSDT", "buy", 0.1, 50000)
        
        time.sleep(3)
        tts.announce_profit("BTCUSDT", 150.50)
        
        # Wait for messages to complete
        time.sleep(5)
        tts.stop_worker()
        
    else:
        print("TTS is not available")
    
    print("TTS test completed")
