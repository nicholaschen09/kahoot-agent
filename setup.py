#!/usr/bin/env python3
"""
Setup script for Kahoot Agent
"""

import subprocess
import sys
import platform
import os


def run_command(command, shell=False):
    """Run a command and return success status."""
    try:
        result = subprocess.run(command, shell=shell, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def install_tesseract():
    """Install Tesseract OCR based on the operating system."""
    system = platform.system().lower()
    
    print(f"🔧 Installing Tesseract OCR for {system}...")
    
    if system == "darwin":  # macOS
        print("   Checking for Homebrew...")
        success, _ = run_command(["which", "brew"])
        if not success:
            print("❌ Homebrew not found. Please install Homebrew first:")
            print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            return False
        
        print("   Installing tesseract via Homebrew...")
        success, output = run_command(["brew", "install", "tesseract"])
        if success:
            print("✅ Tesseract installed successfully!")
            return True
        else:
            print(f"❌ Failed to install tesseract: {output}")
            return False
    
    elif system == "linux":
        print("   Installing tesseract via apt...")
        success, _ = run_command(["sudo", "apt", "update"])
        if success:
            success, output = run_command(["sudo", "apt", "install", "-y", "tesseract-ocr"])
            if success:
                print("✅ Tesseract installed successfully!")
                return True
            else:
                print(f"❌ Failed to install tesseract: {output}")
                return False
        else:
            print("❌ Failed to update package list")
            return False
    
    elif system == "windows":
        print("⚠️ Windows detected. Please install Tesseract manually:")
        print("   1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2. Install the executable")
        print("   3. Add Tesseract to your PATH")
        return True
    
    else:
        print(f"⚠️ Unsupported system: {system}")
        print("   Please install Tesseract OCR manually")
        return True


def check_tesseract():
    """Check if Tesseract is installed."""
    success, _ = run_command(["tesseract", "--version"])
    if success:
        print("✅ Tesseract OCR is installed")
        return True
    else:
        print("⚠️ Tesseract OCR not found")
        return False


def install_requirements():
    """Install Python requirements."""
    print("📦 Installing Python dependencies...")
    
    # Check if pip is available
    success, _ = run_command([sys.executable, "-m", "pip", "--version"])
    if not success:
        print("❌ pip not found!")
        return False
    
    # Install requirements
    success, output = run_command([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ])
    
    if success:
        print("✅ Python dependencies installed successfully!")
        return True
    else:
        print(f"❌ Failed to install dependencies: {output}")
        return False


def test_installation():
    """Test if the installation works."""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import cv2
        import numpy as np
        import requests
        import pyautogui
        
        print("✅ Core dependencies imported successfully")
        
        # Test OCR libraries
        try:
            import easyocr
            print("✅ EasyOCR available")
        except ImportError:
            print("⚠️ EasyOCR not available")
        
        try:
            import pytesseract
            print("✅ pytesseract available")
        except ImportError:
            print("⚠️ pytesseract not available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Kahoot Agent Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check current directory
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        print("   Make sure you're running this from the kahoot-agent directory")
        sys.exit(1)
    
    # Install Python requirements
    if not install_requirements():
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Check/install Tesseract
    if not check_tesseract():
        if platform.system().lower() != "windows":
            install_tesseract()
        else:
            print("⚠️ Please install Tesseract manually on Windows")
    
    # Test installation
    if test_installation():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Open Kahoot in your browser")
        print("2. Run: python kahoot_agent.py --mode single")
        print("3. Check the README.md for more usage instructions")
    else:
        print("\n❌ Setup completed with errors")
        print("   Some components may not work correctly")
        print("   Check the error messages above")


if __name__ == "__main__":
    main()
