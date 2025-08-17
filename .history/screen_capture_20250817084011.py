"""
Screen capture module for Kahoot window detection and screenshot functionality.
"""

import cv2
import numpy as np
import pyautogui
import mss
from typing import Tuple, Optional
import time


class ScreenCapture:
    def __init__(self):
        """Initialize screen capture with safety settings."""
        # Disable pyautogui fail-safe for automated clicking
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # Initialize screen capture
        self.sct = mss.mss()
        
    def find_kahoot_window(self) -> Optional[dict]:
        """
        Find Kahoot window on screen by looking for distinctive elements.
        Returns window coordinates if found.
        """
        # Take full screenshot first
        screenshot = self.capture_full_screen()
        
        # Convert to grayscale for template matching
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        # Look for Kahoot-specific elements (you may need to adjust these)
        # This is a basic implementation - you might need to create template images
        
        # For now, return full screen coordinates
        # In practice, you'd want to detect the actual Kahoot window
        monitor = self.sct.monitors[1]  # Primary monitor
        return {
            "top": monitor["top"],
            "left": monitor["left"], 
            "width": monitor["width"],
            "height": monitor["height"]
        }
    
    def capture_full_screen(self) -> np.ndarray:
        """Capture the full screen."""
        monitor = self.sct.monitors[1]  # Primary monitor
        screenshot = self.sct.grab(monitor)
        # Convert to OpenCV format (BGR)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    
    def capture_kahoot_window(self) -> Optional[np.ndarray]:
        """
        Capture just the Kahoot window area.
        Returns the captured image or None if window not found.
        """
        window_coords = self.find_kahoot_window()
        if not window_coords:
            return None
            
        # Capture the specific window area
        screenshot = self.sct.grab(window_coords)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    
    def capture_question_area(self) -> Optional[np.ndarray]:
        """
        Capture just the question area of Kahoot.
        This typically appears in the upper portion of the screen.
        """
        full_capture = self.capture_kahoot_window()
        if full_capture is None:
            return None
            
        # Extract question area (typically top 40% of screen)
        height, width = full_capture.shape[:2]
        question_area = full_capture[0:int(height * 0.4), 0:width]
        return question_area
    
    def capture_answers_area(self) -> Optional[np.ndarray]:
        """
        Capture the answers area of Kahoot.
        This typically appears in the lower portion of the screen.
        """
        full_capture = self.capture_kahoot_window()
        if full_capture is None:
            return None
            
        # Extract answers area (typically bottom 60% of screen)
        height, width = full_capture.shape[:2]
        answers_area = full_capture[int(height * 0.4):height, 0:width]
        return answers_area
    
    def save_screenshot(self, image: np.ndarray, filename: str) -> None:
        """Save screenshot to file for debugging."""
        cv2.imwrite(filename, image)
        print(f"Screenshot saved as {filename}")


# Test function
if __name__ == "__main__":
    capture = ScreenCapture()
    
    print("Taking screenshot in 3 seconds...")
    time.sleep(3)
    
    # Capture and save different areas
    full_img = capture.capture_full_screen()
    capture.save_screenshot(full_img, "full_screen.png")
    
    question_img = capture.capture_question_area()
    if question_img is not None:
        capture.save_screenshot(question_img, "question_area.png")
    
    answers_img = capture.capture_answers_area()
    if answers_img is not None:
        capture.save_screenshot(answers_img, "answers_area.png")
    
    print("Screenshots captured!")
