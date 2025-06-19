# Kiana

A real-time OCR translation tool that can monitor your clipboard or a specific screen region for text extraction and translation.

## Features

- **Dual Monitoring Modes**
  - Clipboard mode: Automatically processes screenshots copied to clipboard
  - Screen Region mode: Continuously monitors a selected area of your screen
  
- **Real-time Translation**
  - Supports multiple languages (English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic)
  - Auto-detect source language option
  
- **User-friendly Interface**
  - Visual region selection with drag-and-drop
  - Adjustable scan intervals for region monitoring
  - Clear status indicators

# Preview

![image](./assets/Screenshot%202025-06-19%20231250.png)
![image](./assets/Screenshot%202025-06-19%20231407.png)

## Prerequisites

### Python
- Python 3.8 or higher

### Tesseract OCR
You must install Tesseract OCR separately:

**Windows:**
1. Download the installer from [UB Mannheim's Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer (default installation path: `C:\Program Files\Tesseract-OCR`)
3. The application will automatically detect Tesseract if installed in the default location

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

## Installation

1. Clone or download this repository:
```bash
git clone https://github.com/yourusername/ocr-translator.git
cd ocr-translator
```

2. Create a virtual environment (not required but generally recommended):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python main.py
```

2. **For Clipboard Mode:**
   - Select "Clipboard" radio button
   - Click "Start Monitoring"
   - Take a screenshot (Win+Shift+S on Windows, Cmd+Shift+4 on Mac)
   - The text will be automatically extracted and translated

3. **For Screen Region Mode:**
   - Select "Screen Region" radio button
   - Click "Select Region"
   - Click and drag to draw a rectangle around the area you want to monitor
   - Click "Start Monitoring"
   - The selected region will be continuously scanned for text

## File Structure

```
ocr-translator/
├── main.py              # Application entry point
├── gui.py               # Main GUI window
├── region_selector.py   # Screen region selection overlay
├── ocr_processor.py     # OCR and translation logic
├── monitor.py           # Clipboard and region monitoring
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Troubleshooting

### "Tesseract is not installed or not in PATH"
- Ensure Tesseract is installed (see Prerequisites section)
- On Windows, verify it's installed in `C:\Program Files\Tesseract-OCR`
- Alternatively, add Tesseract to your system PATH

### Translation errors
- Check your internet connection (translation requires online access)
- Try selecting a different source/target language combination

### No text detected
- Ensure the image has clear, readable text
- Try adjusting the monitor region to capture text more precisely
- Make sure the text has sufficient contrast with the background

## Dependencies

- **Pillow**: Image processing and screenshot capture
- **pytesseract**: Python wrapper for Tesseract OCR
- **deep-translator**: Reliable translation service wrapper
- **tkinter**: GUI framework (included with Python)

## License

This project is provided as-is for educational and personal