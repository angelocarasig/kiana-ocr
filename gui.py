"""Main GUI module for OCR Translator application."""

import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import ImageGrab, Image
from typing import Optional, Tuple

from region_selector import RegionSelector
from ocr_processor import OCRProcessor
from monitor import ClipboardMonitor, RegionMonitor


class OCRTranslatorApp:
    """Main application window for OCR translation."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Kiana - Screen Region Monitor")
        self.root.geometry("900x700")
        
        self.monitor_mode = tk.StringVar(value="clipboard")
        self.region = None
        self.source_lang = tk.StringVar(value="auto")
        self.target_lang = tk.StringVar(value="en")
        self.scan_interval = tk.DoubleVar(value=1.0)
        
        self.clipboard_monitor = ClipboardMonitor(self.process_image)
        self.region_monitor = RegionMonitor(self.process_image)
        self.ocr_processor = OCRProcessor()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self._create_mode_frame(main_frame)
        self._create_control_frame(main_frame)
        self._create_status_label(main_frame)
        self._create_text_areas(main_frame)
        self._create_process_button(main_frame)
        
    def _create_mode_frame(self, parent):
        """Create monitor mode selection frame."""
        mode_frame = ttk.LabelFrame(parent, text="Monitor Mode", padding="10")
        mode_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="Clipboard", variable=self.monitor_mode, 
                       value="clipboard", command=self.on_mode_change).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Screen Region", variable=self.monitor_mode, 
                       value="region", command=self.on_mode_change).pack(side=tk.LEFT, padx=10)
        
        self.region_btn = ttk.Button(mode_frame, text="Select Region", 
                                    command=self.select_region, state='disabled')
        self.region_btn.pack(side=tk.LEFT, padx=20)
        
        self.region_label = ttk.Label(mode_frame, text="No region selected")
        self.region_label.pack(side=tk.LEFT, padx=10)
        
    def _create_control_frame(self, parent):
        """Create control panel with language selection and monitoring controls."""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.monitor_btn = ttk.Button(control_frame, text="Start Monitoring", 
                                     command=self.toggle_monitoring)
        self.monitor_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(control_frame, text="From:").pack(side=tk.LEFT, padx=(20, 5))
        source_combo = ttk.Combobox(control_frame, textvariable=self.source_lang, 
                                   width=15, state="readonly")
        source_combo['values'] = ['auto', 'en', 'es', 'fr', 'de', 'it', 'pt', 
                                 'ru', 'ja', 'ko', 'zh-cn', 'zh-tw', 'ar']
        source_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(control_frame, text="To:").pack(side=tk.LEFT, padx=(0, 5))
        target_combo = ttk.Combobox(control_frame, textvariable=self.target_lang, 
                                   width=15, state="readonly")
        target_combo['values'] = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 
                                 'ja', 'ko', 'zh-cn', 'zh-tw', 'ar']
        target_combo.pack(side=tk.LEFT)
        
        ttk.Label(control_frame, text="Scan interval:").pack(side=tk.LEFT, padx=(20, 5))
        interval_spin = ttk.Spinbox(control_frame, from_=0.5, to=10.0, increment=0.5,
                                   textvariable=self.scan_interval, width=8)
        interval_spin.pack(side=tk.LEFT)
        ttk.Label(control_frame, text="seconds").pack(side=tk.LEFT, padx=(5, 0))
        
    def _create_status_label(self, parent):
        """Create status display label."""
        self.status_label = ttk.Label(parent, text="Status: Not monitoring", 
                                     foreground="red")
        self.status_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
    def _create_text_areas(self, parent):
        """Create text areas for extracted and translated text."""
        ttk.Label(parent, text="Extracted Text:", font=('TkDefaultFont', 10, 'bold')).grid(
            row=3, column=0, sticky=tk.W)
        
        self.raw_text = scrolledtext.ScrolledText(parent, height=10, wrap=tk.WORD)
        self.raw_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 10))
        
        ttk.Label(parent, text="Translation:", font=('TkDefaultFont', 10, 'bold')).grid(
            row=5, column=0, sticky=tk.W)
        
        self.translated_text = scrolledtext.ScrolledText(parent, height=10, wrap=tk.WORD)
        self.translated_text.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        
    def _create_process_button(self, parent):
        """Create manual process button."""
        self.process_btn = ttk.Button(parent, text="Process Current Clipboard", 
                                     command=self.process_clipboard_once)
        self.process_btn.grid(row=7, column=0, pady=(10, 0))
        
    def on_mode_change(self):
        """Handle monitor mode change."""
        mode = self.monitor_mode.get()
        if mode == "region":
            self.region_btn.config(state='normal')
            self.process_btn.config(state='disabled')
        else:
            self.region_btn.config(state='disabled')
            self.process_btn.config(state='normal')
            self.region = None
            self.region_label.config(text="No region selected")
            
    def select_region(self):
        """Open region selector interface."""
        self.root.withdraw()
        
        def on_region_selected(region: Optional[Tuple[int, int, int, int]]):
            self.root.deiconify()
            if region:
                self.region = region
                x1, y1, x2, y2 = region
                self.region_label.config(
                    text=f"Region: {x2-x1}x{y2-y1} at ({x1},{y1})"
                )
            
        selector = RegionSelector(on_region_selected)
        selector.run()
        
    def toggle_monitoring(self):
        """Toggle monitoring on/off."""
        if self.monitor_btn['text'] == "Start Monitoring":
            if self.monitor_mode.get() == "region" and not self.region:
                self.status_label.config(text="Status: Please select a region first", 
                                       foreground="orange")
                return
                
            self.monitor_btn.config(text="Stop Monitoring")
            mode_text = "clipboard" if self.monitor_mode.get() == "clipboard" else "region"
            self.status_label.config(text=f"Status: Monitoring {mode_text}...", 
                                   foreground="green")
            
            if self.monitor_mode.get() == "clipboard":
                self.clipboard_monitor.start()
            else:
                self.region_monitor.set_region(self.region)
                self.region_monitor.set_interval(self.scan_interval.get())
                self.region_monitor.start()
        else:
            self.monitor_btn.config(text="Start Monitoring")
            self.status_label.config(text="Status: Not monitoring", foreground="red")
            self.clipboard_monitor.stop()
            self.region_monitor.stop()
    
    def process_clipboard_once(self):
        """Process current clipboard content once."""
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                self.process_image(img)
            else:
                self.status_label.config(text="Status: No image found in clipboard", 
                                       foreground="orange")
        except Exception as e:
            self.status_label.config(text=f"Status: Error - {str(e)}", 
                                   foreground="red")
    
    def process_image(self, img: Image.Image):
        """Process image for OCR and translation.
        
        Args:
            img: PIL Image to process
        """
        def update_ui():
            try:
                self.status_label.config(text="Status: Processing image...", 
                                       foreground="blue")
                
                text = self.ocr_processor.extract_text(img)
                
                self.raw_text.delete(1.0, tk.END)
                self.raw_text.insert(1.0, text)
                
                if text.strip():
                    try:
                        translation, detected_lang = self.ocr_processor.translate_text(
                            text, 
                            self.source_lang.get(), 
                            self.target_lang.get()
                        )
                        
                        self.translated_text.delete(1.0, tk.END)
                        self.translated_text.insert(1.0, translation)
                        
                        mode_text = "clipboard" if self.monitor_mode.get() == "clipboard" else "region"
                        self.status_label.config(
                            text=f"Status: Processed successfully from {mode_text}", 
                            foreground="green"
                        )
                    except Exception as e:
                        self.translated_text.delete(1.0, tk.END)
                        self.translated_text.insert(1.0, f"Translation error: {str(e)}")
                        self.status_label.config(text="Status: Translation failed", 
                                               foreground="orange")
                else:
                    self.translated_text.delete(1.0, tk.END)
                    self.translated_text.insert(1.0, "No text detected in image")
                    self.status_label.config(text="Status: No text found", 
                                           foreground="orange")
                    
            except Exception as e:
                self.status_label.config(text=f"Status: Error - {str(e)}", 
                                       foreground="red")
                self.translated_text.delete(1.0, tk.END)
                self.translated_text.insert(1.0, f"Error: {str(e)}")
        
        self.root.after(0, update_ui)