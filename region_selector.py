"""Region selector for screen capture.

Provides a fullscreen overlay interface for selecting screen regions.
"""

import tkinter as tk


class RegionSelector:
    """Fullscreen overlay for selecting a screen region.
    
    Args:
        callback: Function to call with selected region coordinates (x1, y1, x2, y2)
                 or None if cancelled.
    """
    
    def __init__(self, callback):
        self.callback = callback
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.configure(background='gray')
        
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.canvas.bind('<Escape>', lambda e: self.cancel())
        
        self.canvas.create_text(
            self.root.winfo_screenwidth() // 2,
            50,
            text="Drag to select region for OCR monitoring (ESC to cancel)",
            font=('Arial', 16, 'bold'),
            fill='white'
        )
        
    def on_click(self, event):
        """Handle mouse click to start selection."""
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        
    def on_drag(self, event):
        """Handle mouse drag to update selection rectangle."""
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='red', width=3
        )
        
    def on_release(self, event):
        """Handle mouse release to finalize selection."""
        if self.start_x and self.start_y:
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)
            
            if abs(x2 - x1) > 10 and abs(y2 - y1) > 10:
                self.callback((x1, y1, x2, y2))
                self.root.destroy()
            
    def cancel(self):
        """Cancel selection and close overlay."""
        self.callback(None)
        self.root.destroy()
        
    def run(self):
        """Start the region selector interface."""
        self.root.mainloop()