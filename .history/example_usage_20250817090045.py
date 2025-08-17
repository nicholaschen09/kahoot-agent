#!/usr/bin/env python3
"""
Example usage scenarios for the Kahoot Agent.
"""

import time
from kahoot_agent import KahootAgent


def example_single_question():
    """Example: Process a single question manually."""
    print(" Example: Single Question Mode")
    print("-" * 40)
    
    # Create agent (no auto-clicking for safety)
    agent = KahootAgent(use_easyocr=True, auto_click=False)
    
    print("1. Open Kahoot in your browser")
    print("2. Navigate to a question")
    print("3. Make sure the question is clearly visible")
    print("\nStarting in 5 seconds...")
    
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n Processing question...")
    success = agent.process_question()
    
    if success:
        print("✅ Question processed successfully!")
    else:
        print("❌ Failed to process question")


def example_continuous_monitoring():
    """Example: Continuous monitoring mode."""
    print(" Example: Continuous Monitoring")
    print("-" * 40)
    
    # Create agent with custom settings
    agent = KahootAgent(use_easyocr=True, auto_click=False)
    agent.min_confidence = 0.4  # Lower confidence threshold
    agent.scan_interval = 3.0   # Check every 3 seconds
    
    print("🤖 Starting continuous monitoring...")
    print("   - Auto-click: Disabled (for safety)")
    print("   - Confidence threshold: 0.4")
    print("   - Scan interval: 3 seconds")
    print("   - Emergency stop: Move mouse to top-left corner")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        agent.run_continuous()
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")


def example_high_confidence_auto_click():
    """Example: Auto-click mode with high confidence requirement."""
    print(" Example: Auto-Click Mode (High Confidence)")
    print("-" * 40)
    
    print("⚠️ WARNING: This will automatically click answers!")
    print("⚠️ Make sure you understand the risks and have permission!")
    
    confirm = input("Type 'YES' to continue: ")
    if confirm != "YES":
        print("Cancelled.")
        return
    
    # Create agent with auto-clicking enabled
    agent = KahootAgent(use_easyocr=True, auto_click=True)
    agent.min_confidence = 0.7  # High confidence requirement
    agent.scan_interval = 2.0
    
    print("🤖 Starting auto-click mode...")
    print("   - Auto-click: Enabled")
    print("   - Confidence threshold: 0.7 (high)")
    print("   - Will only click if very confident")
    print("   - Emergency stop: Move mouse to top-left corner")
    print("\nStarting in 5 seconds...")
    
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    try:
        agent.run_continuous()
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")


def example_debug_mode():
    """Example: Debug mode to see what the agent captures."""
    print(" Example: Debug Mode")
    print("-" * 40)
    
    agent = KahootAgent(use_easyocr=True, auto_click=False)
    
    print(" Taking debug screenshots...")
    print("Make sure Kahoot is visible on screen")
    
    # Give time to position windows
    for i in range(3, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)
    
    # Capture and analyze (this saves debug images)
    question, answers, positions = agent.capture_and_analyze()
    
    print(f"\n📊 Debug Results:")
    print(f"   Question: {question}")
    print(f"   Answers: {answers}")
    print(f"   Button positions: {len(positions)} found")
    
    print(f"\n📁 Debug files saved:")
    print(f"   - debug_question.png (question area)")
    print(f"   - debug_answers.png (answers area)")
    
    if question and answers:
        print(f"\n Searching for answer...")
        best_answer, confidence = agent.search_for_answer(question, answers)
        print(f"   Best answer: {best_answer}")
        print(f"   Confidence: {confidence:.2f}")


def example_custom_configuration():
    """Example: Custom configuration for specific needs."""
    print(" Example: Custom Configuration")
    print("-" * 40)
    
    # Create agent with custom settings
    agent = KahootAgent(use_easyocr=False, auto_click=False)  # Use Tesseract
    
    # Customize search behavior
    agent.answer_searcher.min_request_interval = 0.5  # Faster searches
    
    # Customize OCR settings
    agent.ocr_extractor.tesseract_config = '--oem 3 --psm 7'  # Single text line
    
    # Customize confidence threshold
    agent.min_confidence = 0.3  # Lower threshold
    
    print("⚙️ Custom configuration:")
    print("   - OCR: Tesseract (instead of EasyOCR)")
    print("   - Search interval: 0.5s (faster)")
    print("   - OCR mode: Single text line")
    print("   - Confidence threshold: 0.3 (lower)")
    
    print("\nProcessing question with custom settings...")
    success = agent.process_question()
    
    if success:
        print("✅ Custom configuration works!")
    else:
        print("❌ Custom configuration failed")


def main():
    """Main menu for examples."""
    print("🤖 Kahoot Agent - Example Usage")
    print("=" * 50)
    
    examples = [
        ("Single Question Mode", example_single_question),
        ("Continuous Monitoring", example_continuous_monitoring),
        ("Auto-Click Mode (HIGH RISK)", example_high_confidence_auto_click),
        ("Debug Mode", example_debug_mode),
        ("Custom Configuration", example_custom_configuration)
    ]
    
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("  0. Exit")
    
    try:
        choice = int(input("\nSelect an example (0-5): "))
        
        if choice == 0:
            print("Goodbye!")
            return
        
        if 1 <= choice <= len(examples):
            name, func = examples[choice - 1]
            print(f"\n{'='*50}")
            func()
        else:
            print("Invalid choice!")
    
    except ValueError:
        print("Please enter a number!")
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
