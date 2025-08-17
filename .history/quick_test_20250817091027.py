#!/usr/bin/env python3
"""
Quick test script for the Kahoot Agent.
Makes it easy to test the agent step by step.
"""

import time
import sys
from kahoot_agent import KahootAgent


def main():
    print("Kahoot Agent Quick Test")
    print("=" * 30)
    
    print("\nInstructions:")
    print("1. Open Kahoot in your browser")
    print("2. Join a game or practice quiz")
    print("3. Wait for a question to appear")
    print("4. Make sure the question is clearly visible")
    
    input("\nPress Enter when ready...")
    
    # Create agent in safe mode (no auto-clicking)
    agent = KahootAgent(use_easyocr=True, auto_click=False)
    
    print("\nStarting test in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("\nCapturing and analyzing...")
    
    try:
        # Test the main functionality
        success = agent.process_question()
        
        if success:
            print("\n" + "=" * 50)
            print("Test completed successfully!")
            print("\nNext steps:")
            print("1. Check if the extracted question text is correct")
            print("2. Verify the answer options were detected properly") 
            print("3. Review the recommended answer")
            print("4. Check debug_question.png and debug_answers.png files")
            print("5. Manually click the recommended answer to test accuracy")
            
            print("\nFor continuous testing, run:")
            print("  python kahoot_agent.py --mode continuous")
            
        else:
            print("\nTest failed. Possible issues:")
            print("- Kahoot window not visible")
            print("- Question text not clear enough")
            print("- No internet connection")
            print("- OCR couldn't read the text")
            
            print("\nTroubleshooting:")
            print("1. Make sure Kahoot is maximized in your browser")
            print("2. Ensure the question is fully visible")
            print("3. Try again with a different question")
            print("4. Check debug images to see what was captured")
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nError during test: {e}")
        print("Make sure all dependencies are installed correctly")


if __name__ == "__main__":
    main()
