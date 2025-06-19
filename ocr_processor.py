"""OCR and translation processing module."""

import pytesseract
from deep_translator import GoogleTranslator
from PIL import Image


class OCRProcessor:
    """Handles OCR extraction and text translation."""
    
    @staticmethod
    def extract_text(image: Image.Image) -> str:
        """Extract text from image using Tesseract OCR.
        
        Args:
            image: PIL Image object to process
            
        Returns:
            Extracted text string
        """
        return pytesseract.image_to_string(image)
    
    @staticmethod
    def translate_text(text: str, source_lang: str, target_lang: str) -> tuple[str, str]:
        """Translate text from source to target language.
        
        Args:
            text: Text to translate
            source_lang: Source language code ('auto' for auto-detect)
            target_lang: Target language code
            
        Returns:
            Tuple of (translated_text, detected_language)
            
        Raises:
            Exception: If translation fails
        """
        if not text.strip():
            return "", ""
            
        if source_lang == 'auto':
            translator = GoogleTranslator(source='auto', target=target_lang)
            translation_text = translator.translate(text)
            detected_lang = 'auto'
        else:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translation_text = translator.translate(text)
            detected_lang = source_lang
            
        return translation_text, detected_lang