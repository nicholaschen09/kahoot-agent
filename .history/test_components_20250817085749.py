#!/usr/bin/env python3
"""
Test script to verify all components of the Kahoot Agent work correctly.
"""

import sys
import time
import traceback
from typing import Dict, Any


def test_imports() -> Dict[str, Any]:
    """Test if all required modules can be imported."""
    print("Testing imports...")
    results = {}
    
    # Core modules
    modules_to_test = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("requests", "Requests"),
        ("bs4", "BeautifulSoup4"),
        ("pyautogui", "PyAutoGUI"),
        ("mss", "MSS"),
        ("PIL", "Pillow")
    ]
    
    for module_name, display_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  [PASS] {display_name}")
            results[module_name] = True
        except ImportError as e:
            print(f"  [FAIL] {display_name}: {e}")
            results[module_name] = False
    
    # OCR modules
    ocr_modules = [
        ("easyocr", "EasyOCR"),
        ("pytesseract", "Tesseract")
    ]
    
    for module_name, display_name in ocr_modules:
        try:
            __import__(module_name)
            print(f"  [PASS] {display_name}")
            results[module_name] = True
        except ImportError as e:
            print(f"  [WARN] {display_name}: {e} (optional)")
            results[module_name] = False
    
    return results


def test_screen_capture():
    """Test screen capture functionality."""
    print("\n🖥️ Testing screen capture...")
    
    try:
        from screen_capture import ScreenCapture
        
        capture = ScreenCapture()
        print("  ✅ ScreenCapture initialized")
        
        # Test full screen capture
        img = capture.capture_full_screen()
        if img is not None:
            print(f"  ✅ Full screen captured: {img.shape}")
        else:
            print("  ❌ Failed to capture full screen")
            return False
        
        # Test Kahoot window detection
        window = capture.find_kahoot_window()
        if window:
            print(f"  ✅ Window detection works: {window}")
        else:
            print("  ⚠️ Window detection returned None (expected if no Kahoot open)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Screen capture error: {e}")
        traceback.print_exc()
        return False


def test_ocr_extraction():
    """Test OCR extraction functionality."""
    print("\n🔤 Testing OCR extraction...")
    
    try:
        from ocr_extractor import OCRExtractor
        import numpy as np
        
        # Test with EasyOCR if available
        try:
            ocr = OCRExtractor(use_easyocr=True)
            print("  ✅ EasyOCR extractor initialized")
        except:
            try:
                ocr = OCRExtractor(use_easyocr=False)
                print("  ✅ Tesseract extractor initialized")
            except Exception as e:
                print(f"  ❌ No OCR engine available: {e}")
                return False
        
        # Create a simple test image with text
        test_img = np.ones((100, 300, 3), dtype=np.uint8) * 255  # White image
        
        # Test text extraction (will likely return empty on blank image)
        text = ocr.extract_text(test_img)
        print(f"  ✅ Text extraction works (returned: '{text}')")
        
        return True
        
    except Exception as e:
        print(f"  ❌ OCR extraction error: {e}")
        traceback.print_exc()
        return False


def test_answer_searcher():
    """Test answer searching functionality."""
    print("\n🔍 Testing answer searcher...")
    
    try:
        from answer_searcher import AnswerSearcher
        
        searcher = AnswerSearcher()
        print("  ✅ AnswerSearcher initialized")
        
        # Test with a simple question
        test_question = "What is 2 + 2?"
        test_options = ["3", "4", "5", "6"]
        
        print(f"  🧪 Testing with: '{test_question}'")
        print("     This will make real web requests...")
        
        answer, confidence = searcher.find_best_answer(test_question, test_options)
        
        print(f"  ✅ Search completed: '{answer}' (confidence: {confidence:.2f})")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Answer searcher error: {e}")
        traceback.print_exc()
        return False


def test_auto_clicker():
    """Test auto clicker functionality (without actually clicking)."""
    print("\n🖱️ Testing auto clicker...")
    
    try:
        from auto_clicker import AutoClicker
        import numpy as np
        
        clicker = AutoClicker()
        print("  ✅ AutoClicker initialized")
        
        # Test button finding with fake image
        test_img = np.ones((400, 600, 3), dtype=np.uint8) * 128  # Gray image
        test_options = ["Option A", "Option B", "Option C", "Option D"]
        
        positions = clicker.find_answer_buttons(test_img, test_options)
        print(f"  ✅ Button detection works: found {len(positions)} positions")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Auto clicker error: {e}")
        traceback.print_exc()
        return False


def test_main_agent():
    """Test the main agent (without auto-clicking)."""
    print("\n🤖 Testing main agent...")
    
    try:
        from kahoot_agent import KahootAgent
        
        agent = KahootAgent(auto_click=False)  # Disable auto-click for safety
        print("  ✅ KahootAgent initialized")
        
        print("  ✅ All components integrated successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Main agent error: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🧪 Kahoot Agent Component Tests")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Screen Capture", test_screen_capture),
        ("OCR Extraction", test_ocr_extraction),
        ("Answer Searcher", test_answer_searcher),
        ("Auto Clicker", test_auto_clicker),
        ("Main Agent", test_main_agent)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! The agent should work correctly.")
        print("\nNext steps:")
        print("1. Open Kahoot in your browser")
        print("2. Run: python kahoot_agent.py --mode single")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("The agent may work partially or not at all.")
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
