"""
OCR text extraction module for extracting questions and answers from Kahoot screenshots.
"""

import cv2
import numpy as np
import pytesseract
import easyocr
from typing import List, Optional, Dict
import re


class OCRExtractor:
    def __init__(self, use_easyocr: bool = True):
        """
        Initialize OCR extractor.
        
        Args:
            use_easyocr: If True, use EasyOCR (more accurate), else use Tesseract
        """
        self.use_easyocr = use_easyocr
        
        if use_easyocr:
            # Initialize EasyOCR reader for English
            self.reader = easyocr.Reader(['en'])
        
        # Tesseract configuration for better accuracy
        self.tesseract_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,?!:;-() '
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR accuracy.
        
        Args:
            image: Input image
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to clean up the image
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Resize image for better OCR (optimal height is around 200-300 pixels)
        height, width = cleaned.shape
        if height < 200:
            scale_factor = 250 / height
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            cleaned = cv2.resize(cleaned, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        return cleaned
    
    def extract_text_easyocr(self, image: np.ndarray) -> str:
        """
        Extract text using EasyOCR.
        
        Args:
            image: Input image
            
        Returns:
            Extracted text
        """
        # EasyOCR works better with color images
        results = self.reader.readtext(image)
        
        # Combine all detected text
        text_parts = []
        for (bbox, text, confidence) in results:
            # Only include text with reasonable confidence
            if confidence > 0.3:
                text_parts.append(text)
        
        return ' '.join(text_parts)
    
    def extract_text_tesseract(self, image: np.ndarray) -> str:
        """
        Extract text using Tesseract OCR.
        
        Args:
            image: Input image
            
        Returns:
            Extracted text
        """
        # Preprocess image for better accuracy
        processed_image = self.preprocess_image(image)
        
        # Extract text
        text = pytesseract.image_to_string(processed_image, config=self.tesseract_config)
        
        return text.strip()
    
    def extract_text(self, image: np.ndarray) -> str:
        """
        Extract text from image using the configured OCR method.
        
        Args:
            image: Input image
            
        Returns:
            Extracted text
        """
        if self.use_easyocr:
            return self.extract_text_easyocr(image)
        else:
            return self.extract_text_tesseract(image)
    
    def extract_question(self, question_image: np.ndarray) -> Optional[str]:
        """
        Extract question text from question area image.
        
        Args:
            question_image: Image containing the question
            
        Returns:
            Extracted question text or None if extraction fails
        """
        if question_image is None:
            return None
            
        text = self.extract_text(question_image)
        
        # Clean up the extracted text
        question = self.clean_question_text(text)
        
        return question if question else None
    
    def extract_answers(self, answers_image: np.ndarray) -> List[str]:
        """
        Extract answer options from answers area image.
        
        Args:
            answers_image: Image containing the answer options
            
        Returns:
            List of extracted answer texts
        """
        if answers_image is None:
            return []
            
        text = self.extract_text(answers_image)
        
        # Split and clean answer options
        answers = self.parse_answer_options(text)
        
        return answers
    
    def clean_question_text(self, raw_text: str) -> str:
        """
        Clean and format extracted question text.
        
        Args:
            raw_text: Raw OCR extracted text
            
        Returns:
            Cleaned question text
        """
        if not raw_text:
            return ""
        
        # Remove extra whitespace and newlines
        cleaned = re.sub(r'\s+', ' ', raw_text.strip())
        
        # Remove common OCR artifacts
        cleaned = re.sub(r'[|@#$%^&*]', '', cleaned)
        
        # Ensure question ends with proper punctuation
        if cleaned and not cleaned.endswith(('?', '.', '!')):
            cleaned += '?'
        
        return cleaned
    
    def parse_answer_options(self, raw_text: str) -> List[str]:
        """
        Parse answer options from extracted text.
        
        Args:
            raw_text: Raw OCR extracted text from answers area
            
        Returns:
            List of cleaned answer options
        """
        if not raw_text:
            return []
        
        # Split by common delimiters
        lines = raw_text.split('\n')
        
        answers = []
        for line in lines:
            cleaned = line.strip()
            # Skip empty lines and very short text (likely artifacts)
            if len(cleaned) > 2:
                # Remove common prefixes like "A)", "1.", etc.
                cleaned = re.sub(r'^[A-D]\)?\s*', '', cleaned)
                cleaned = re.sub(r'^[1-4]\.?\s*', '', cleaned)
                
                if cleaned:
                    answers.append(cleaned)
        
        # If we didn't get good results with line splitting, try other methods
        if len(answers) < 2:
            # Try splitting by common patterns
            # Kahoot typically has 2-4 answer options
            words = raw_text.split()
            if len(words) >= 4:
                # This is a fallback - you might need to adjust based on actual Kahoot layout
                answers = [' '.join(words[i:i+3]) for i in range(0, min(len(words), 12), 3)]
        
        return answers[:4]  # Kahoot typically has max 4 options


# Test function
if __name__ == "__main__":
    import cv2
    
    # Test with sample images (you would replace with actual screenshots)
    extractor = OCRExtractor(use_easyocr=True)
    
    # Test question extraction
    try:
        # You would load actual screenshot here
        # question_img = cv2.imread("question_area.png")
        # question = extractor.extract_question(question_img)
        # print(f"Extracted question: {question}")
        
        print("OCR extractor initialized successfully!")
        print("To test, run screen capture first, then use the generated images.")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to install tesseract-ocr on your system:")
        print("  macOS: brew install tesseract")
        print("  Ubuntu: sudo apt install tesseract-ocr")
        print("  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
