"""Monitoring modules for clipboard and screen regions."""

import io
import time
import threading
from PIL import ImageGrab, Image
from typing import Optional, Callable, Tuple


class ClipboardMonitor:
    """Monitor system clipboard for image changes."""
    
    def __init__(self, callback: Callable[[Image.Image], None]):
        """Initialize clipboard monitor.
        
        Args:
            callback: Function to call when new image is detected
        """
        self.callback = callback
        self.last_image = None
        self.monitoring = False
        self.thread = None
        
    def start(self):
        """Start monitoring clipboard in background thread."""
        self.monitoring = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop monitoring clipboard."""
        self.monitoring = False
        
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                img = ImageGrab.grabclipboard()
                
                if isinstance(img, Image.Image):
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    img_data = img_bytes.getvalue()
                    
                    if img_data != self.last_image:
                        self.last_image = img_data
                        self.callback(img)
                        
            except Exception as e:
                print(f"Error monitoring clipboard: {e}")
                
            time.sleep(0.5)


class RegionMonitor:
    """Monitor specific screen region for changes."""
    
    def __init__(self, callback: Callable[[Image.Image], None]):
        """Initialize region monitor.
        
        Args:
            callback: Function to call when region content changes
        """
        self.callback = callback
        self.region = None
        self.last_image = None
        self.monitoring = False
        self.thread = None
        self.scan_interval = 1.0
        
    def set_region(self, region: Tuple[int, int, int, int]):
        """Set the region to monitor.
        
        Args:
            region: Tuple of (x1, y1, x2, y2) coordinates
        """
        self.region = region
        
    def set_interval(self, interval: float):
        """Set scan interval in seconds.
        
        Args:
            interval: Time between scans in seconds
        """
        self.scan_interval = interval
        
    def start(self):
        """Start monitoring region in background thread."""
        if not self.region:
            raise ValueError("Region not set")
            
        self.monitoring = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop monitoring region."""
        self.monitoring = False
        
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                x1, y1, x2, y2 = self.region
                img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_data = img_bytes.getvalue()
                
                if img_data != self.last_image:
                    self.last_image = img_data
                    self.callback(img)
                    
            except Exception as e:
                print(f"Error monitoring region: {e}")
                
            time.sleep(self.scan_interval)