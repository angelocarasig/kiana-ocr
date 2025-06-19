"""OCR Translator Application

A desktop application that performs OCR on screenshots or screen regions
and translates the extracted text in real-time.
"""

import pytesseract
import os
import tkinter as tk
from gui import OCRTranslatorApp

if os.path.exists(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def main():
    """Entry point for the OCR Translator application."""
    try:
        pytesseract.get_tesseract_version()
    except:
        print("Error: Tesseract is not installed or not in PATH")
        print("Please install Tesseract OCR:")
        print("- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("- Mac: brew install tesseract")
        print("- Linux: sudo apt-get install tesseract-ocr")
        return
    
    root = tk.Tk()
    app = OCRTranslatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()