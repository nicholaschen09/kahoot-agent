"""
Main Kahoot Agent - Orchestrates screen capture, OCR, answer search, and clicking.
"""

import time
import cv2
import threading
from typing import Optional, Tuple, List
import argparse

from screen_capture import ScreenCapture
from ocr_extractor import OCRExtractor
from answer_searcher import AnswerSearcher
from auto_clicker import AutoClicker


class KahootAgent:
    def __init__(self, use_easyocr: bool = True, auto_click: bool = False):
        """
        Initialize the Kahoot Agent.
        
        Args:
            use_easyocr: Whether to use EasyOCR (more accurate) or Tesseract
            auto_click: Whether to automatically click answers (use with caution!)
        """
        self.screen_capture = ScreenCapture()
        self.ocr_extractor = OCRExtractor(use_easyocr=use_easyocr)
        self.answer_searcher = AnswerSearcher()
        self.auto_clicker = AutoClicker()
        
        self.auto_click = auto_click
        self.running = False
        
        # Configuration
        self.min_confidence = 0.3  # Minimum confidence to auto-click
        self.scan_interval = 2.0   # Seconds between scans
        
        # State tracking
        self.last_question = ""
        self.question_count = 0
        
    def capture_and_analyze(self) -> Tuple[Optional[str], List[str], List[Tuple[int, int]]]:
        """
        Capture screen and analyze for question and answers.
        
        Returns:
            Tuple of (question, answer_options, button_positions)
        """
        print("📸 Capturing screen...")
        
        # Capture question and answer areas
        question_img = self.screen_capture.capture_question_area()
        answers_img = self.screen_capture.capture_answers_area()
        
        if question_img is None or answers_img is None:
            print("❌ Failed to capture screen areas")
            return None, [], []
        
        # Save debug images
        cv2.imwrite("debug_question.png", question_img)
        cv2.imwrite("debug_answers.png", answers_img)
        
        print("🔤 Extracting text...")
        
        # Extract question text
        question = self.ocr_extractor.extract_question(question_img)
        if not question:
            print("❌ Failed to extract question text")
            return None, [], []
        
        # Extract answer options
        answer_options = self.ocr_extractor.extract_answers(answers_img)
        if not answer_options:
            print("❌ Failed to extract answer options")
            return question, [], []
        
        # Find button positions
        button_positions = self.auto_clicker.find_answer_buttons(answers_img, answer_options)
        
        # Try color-based detection as backup
        if not button_positions:
            button_positions = self.auto_clicker.find_color_coded_answers(answers_img)
        
        print(f"✅ Extracted question: {question}")
        print(f"✅ Found {len(answer_options)} answer options: {answer_options}")
        print(f"✅ Found {len(button_positions)} button positions")
        
        return question, answer_options, button_positions
    
    def search_for_answer(self, question: str, answer_options: List[str]) -> Tuple[str, float]:
        """
        Search for the best answer to the question.
        
        Args:
            question: The question text
            answer_options: List of possible answers
            
        Returns:
            Tuple of (best_answer, confidence)
        """
        print("🔍 Searching for answer...")
        
        best_answer, confidence = self.answer_searcher.find_best_answer(question, answer_options)
        
        print(f"✅ Best answer: '{best_answer}' (confidence: {confidence:.2f})")
        
        return best_answer, confidence
    
    def process_question(self) -> bool:
        """
        Process a single question - capture, analyze, search, and optionally click.
        
        Returns:
            True if processing was successful, False otherwise
        """
        try:
            # Capture and analyze
            question, answer_options, button_positions = self.capture_and_analyze()
            
            if not question or not answer_options:
                return False
            
            # Check if this is a new question (avoid processing the same question multiple times)
            if question == self.last_question:
                return True  # Not an error, just the same question
            
            self.last_question = question
            self.question_count += 1
            
            print(f"\n🎯 Question #{self.question_count}: {question}")
            print(f"📝 Options: {answer_options}")
            
            # Search for answer
            best_answer, confidence = self.search_for_answer(question, answer_options)
            
            if not best_answer:
                print("❌ No answer found")
                return False
            
            print(f"🎯 Recommended answer: {best_answer} (confidence: {confidence:.2f})")
            
            # Auto-click if enabled and confidence is high enough
            if self.auto_click and confidence >= self.min_confidence and button_positions:
                print("🖱️ Auto-clicking answer...")
                
                # Get answers area offset (you might need to adjust this based on your screen setup)
                answers_area_offset = (0, int(self.screen_capture.sct.monitors[1]["height"] * 0.4))
                
                success = self.auto_clicker.click_best_answer(
                    best_answer, answer_options, button_positions, answers_area_offset
                )
                
                if success:
                    print("✅ Answer clicked successfully!")
                else:
                    print("❌ Failed to click answer")
            
            elif self.auto_click:
                print(f"⚠️ Confidence too low ({confidence:.2f} < {self.min_confidence}) - not clicking")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing question: {e}")
            return False
    
    def run_continuous(self):
        """Run the agent continuously, monitoring for new questions."""
        print("🚀 Starting Kahoot Agent in continuous mode...")
        print(f"⚙️ Auto-click: {'Enabled' if self.auto_click else 'Disabled'}")
        print(f"⚙️ Min confidence for auto-click: {self.min_confidence}")
        print(f"⚙️ Scan interval: {self.scan_interval}s")
        print("⚠️ Emergency stop: Move mouse to top-left corner\n")
        
        self.running = True
        
        try:
            while self.running:
                self.process_question()
                time.sleep(self.scan_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            self.running = False
    
    def run_single(self):
        """Process a single question and exit."""
        print("🚀 Running Kahoot Agent in single-shot mode...")
        print("⚠️ Make sure Kahoot is visible on screen\n")
        
        # Give user time to position windows
        for i in range(3, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
        
        success = self.process_question()
        
        if success:
            print("\n✅ Question processed successfully!")
        else:
            print("\n❌ Failed to process question")
        
        return success
    
    def stop(self):
        """Stop the agent."""
        self.running = False
        print("🛑 Stopping agent...")


def main():
    """Main entry point with command line arguments."""
    parser = argparse.ArgumentParser(description="Kahoot Agent - Automated question answering")
    
    parser.add_argument("--mode", choices=["single", "continuous"], default="single",
                       help="Run mode: single question or continuous monitoring")
    
    parser.add_argument("--auto-click", action="store_true",
                       help="Enable automatic clicking (use with caution!)")
    
    parser.add_argument("--ocr", choices=["easyocr", "tesseract"], default="easyocr",
                       help="OCR engine to use")
    
    parser.add_argument("--confidence", type=float, default=0.3,
                       help="Minimum confidence for auto-clicking (0.0-1.0)")
    
    parser.add_argument("--interval", type=float, default=2.0,
                       help="Scan interval in seconds for continuous mode")
    
    args = parser.parse_args()
    
    # Create agent
    agent = KahootAgent(
        use_easyocr=(args.ocr == "easyocr"),
        auto_click=args.auto_click
    )
    
    # Configure agent
    agent.min_confidence = args.confidence
    agent.scan_interval = args.interval
    
    # Run agent
    if args.mode == "single":
        agent.run_single()
    else:
        agent.run_continuous()


if __name__ == "__main__":
    main()
