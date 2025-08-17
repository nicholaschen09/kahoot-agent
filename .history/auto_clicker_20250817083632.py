"""
Automated clicking module for selecting answers in Kahoot.
"""

import pyautogui
import cv2
import numpy as np
from typing import List, Tuple, Optional
import time


class AutoClicker:
    def __init__(self):
        """Initialize the auto clicker with safety settings."""
        # Enable fail-safe (move mouse to top-left to abort)
        pyautogui.FAILSAFE = True
        
        # Set pause between actions
        pyautogui.PAUSE = 0.1
        
        # Confidence threshold for template matching
        self.confidence_threshold = 0.7
        
    def find_answer_buttons(self, answers_image: np.ndarray, 
                          answer_options: List[str]) -> List[Tuple[int, int]]:
        """
        Find the clickable positions for answer buttons.
        
        Args:
            answers_image: Screenshot of the answers area
            answer_options: List of answer text options
            
        Returns:
            List of (x, y) coordinates for each answer button
        """
        if answers_image is None or not answer_options:
            return []
        
        # For Kahoot, answers are typically arranged in a 2x2 grid
        # We'll divide the answers area into quadrants
        height, width = answers_image.shape[:2]
        
        # Define quadrant centers (typical Kahoot layout)
        quadrants = [
            (width // 4, height // 4),      # Top-left
            (3 * width // 4, height // 4),  # Top-right
            (width // 4, 3 * height // 4),  # Bottom-left
            (3 * width // 4, 3 * height // 4)  # Bottom-right
        ]
        
        # Return coordinates for up to 4 answers
        num_answers = min(len(answer_options), 4)
        return quadrants[:num_answers]
    
    def find_color_coded_answers(self, answers_image: np.ndarray) -> List[Tuple[int, int]]:
        """
        Find answer buttons based on Kahoot's color coding.
        Kahoot typically uses red, blue, yellow, and green for answers.
        
        Args:
            answers_image: Screenshot of the answers area
            
        Returns:
            List of (x, y) coordinates for detected color regions
        """
        if answers_image is None:
            return []
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(answers_image, cv2.COLOR_BGR2HSV)
        
        # Define color ranges for Kahoot answer buttons (HSV)
        color_ranges = {
            'red': ((0, 50, 50), (10, 255, 255)),
            'blue': ((100, 50, 50), (130, 255, 255)),
            'yellow': ((20, 50, 50), (30, 255, 255)),
            'green': ((40, 50, 50), (80, 255, 255))
        }
        
        button_positions = []
        
        for color_name, (lower, upper) in color_ranges.items():
            # Create mask for this color
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Find the largest contour (likely the answer button)
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get the center of the contour
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # Only add if the area is significant (likely a button)
                    area = cv2.contourArea(largest_contour)
                    if area > 1000:  # Minimum area threshold
                        button_positions.append((cx, cy))
        
        return button_positions
    
    def click_answer(self, answer_index: int, button_positions: List[Tuple[int, int]], 
                    answers_area_offset: Tuple[int, int] = (0, 0)) -> bool:
        """
        Click on the specified answer button.
        
        Args:
            answer_index: Index of the answer to click (0-based)
            button_positions: List of button positions relative to answers area
            answers_area_offset: Offset of answers area from screen origin
            
        Returns:
            True if click was successful, False otherwise
        """
        if not button_positions or answer_index >= len(button_positions):
            return False
        
        try:
            # Get the relative position
            rel_x, rel_y = button_positions[answer_index]
            
            # Convert to absolute screen coordinates
            abs_x = rel_x + answers_area_offset[0]
            abs_y = rel_y + answers_area_offset[1]
            
            # Perform the click
            pyautogui.click(abs_x, abs_y)
            
            print(f"Clicked answer {answer_index + 1} at position ({abs_x}, {abs_y})")
            return True
            
        except Exception as e:
            print(f"Error clicking: {e}")
            return False
    
    def click_best_answer(self, best_answer: str, answer_options: List[str], 
                         button_positions: List[Tuple[int, int]], 
                         answers_area_offset: Tuple[int, int] = (0, 0)) -> bool:
        """
        Click the button corresponding to the best answer.
        
        Args:
            best_answer: The text of the best answer
            answer_options: List of all answer options
            button_positions: List of button positions
            answers_area_offset: Offset of answers area from screen origin
            
        Returns:
            True if click was successful, False otherwise
        """
        if not best_answer or not answer_options:
            return False
        
        # Find the index of the best answer
        answer_index = -1
        for i, option in enumerate(answer_options):
            if option and best_answer.lower() in option.lower():
                answer_index = i
                break
        
        # If exact match not found, try fuzzy matching
        if answer_index == -1:
            best_words = set(best_answer.lower().split())
            best_match_score = 0
            
            for i, option in enumerate(answer_options):
                if option:
                    option_words = set(option.lower().split())
                    # Calculate word overlap
                    overlap = len(best_words.intersection(option_words))
                    if overlap > best_match_score:
                        best_match_score = overlap
                        answer_index = i
        
        if answer_index >= 0:
            return self.click_answer(answer_index, button_positions, answers_area_offset)
        
        print(f"Could not find answer '{best_answer}' in options: {answer_options}")
        return False
    
    def emergency_stop(self):
        """Emergency stop function - moves mouse to top-left corner."""
        pyautogui.moveTo(0, 0)
        print("Emergency stop activated!")


# Test function
if __name__ == "__main__":
    clicker = AutoClicker()
    
    print("Auto clicker initialized!")
    print("Emergency stop: Move mouse to top-left corner of screen")
    
    # Test clicking (replace with actual coordinates)
    test_positions = [(100, 100), (300, 100), (100, 300), (300, 300)]
    
    print("Test mode - would click at positions:", test_positions)
    
    # Uncomment below to test actual clicking (be careful!)
    # time.sleep(3)  # Give time to position windows
    # clicker.click_answer(0, test_positions)
