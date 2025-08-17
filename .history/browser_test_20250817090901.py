#!/usr/bin/env python3
"""
Simple test script that helps focus on browser window for Kahoot testing.
"""

import time
from kahoot_agent import KahootAgent

def main():
    print("Browser Window Test for Kahoot")
    print("=" * 35)
    print()
    print("IMPORTANT SETUP:")
    print("1. Switch to your BROWSER TAB with Kahoot")
    print("2. Make the browser window LARGE/FULLSCREEN")
    print("3. Make sure you can see:")
    print("   - The question text clearly")
    print("   - All 4 answer options")
    print("4. Hide this terminal or code editor")
    print()
    print("Current Kahoot Question: 'Switzerland' with flag options")
    print("Expected Answer: Red flag with white cross (Swiss flag)")
    print()
    
    input("Press Enter when your BROWSER with Kahoot is the active window...")
    
    print("Testing in 5 seconds...")
    for i in range(5, 0, -1):
        print(f"  {i}... (make sure browser is active)")
        time.sleep(1)
    
    print("\nCapturing browser window...")
    
    # Test with agent
    agent = KahootAgent(use_easyocr=True, auto_click=False)
    
    try:
        success = agent.process_question()
        
        print("\n" + "="*50)
        print("ANALYSIS:")
        
        if success:
            print("✓ Screen capture worked")
            print("✓ Check if it found 'Switzerland' in the question")
            print("✓ Check if it found flag-related answer options")
            print("\nFor the current question:")
            print("- Correct answer should be: Swiss flag (red with white cross)")
            print("- This is typically the TOP-LEFT option in Kahoot")
        else:
            print("✗ Screen capture failed")
            print("→ Try making browser window larger")
            print("→ Ensure Kahoot game is clearly visible")
            
        print("\nDebug files saved:")
        print("- debug_question.png (should show 'Switzerland')")
        print("- debug_answers.png (should show 4 flag options)")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure virtual environment is active and all dependencies installed")

if __name__ == "__main__":
    main()
