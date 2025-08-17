# 🚀 Quick Start Guide

Get your Kahoot Agent up and running in 5 minutes!

## 📋 Prerequisites

- Python 3.8+ installed
- Internet connection for web searches
- Kahoot game open in a browser

## ⚡ Fast Setup

1. **Install dependencies:**
   ```bash
   python setup.py
   ```
   *OR manually:*
   ```bash
   pip install -r requirements.txt
   brew install tesseract  # macOS
   ```

2. **Test installation:**
   ```bash
   python test_components.py
   ```

3. **Run the agent:**
   ```bash
   python kahoot_agent.py --mode single
   ```

## 🎯 Basic Usage

### Safe Mode (Recommended for first time)
```bash
# Process one question and show answer (no clicking)
python kahoot_agent.py --mode single

# Monitor continuously and show answers
python kahoot_agent.py --mode continuous
```

### Auto-Click Mode (Use with caution!)
```bash
# Auto-click with high confidence threshold
python kahoot_agent.py --mode continuous --auto-click --confidence 0.7
```

## 🔧 Quick Configuration

| Option | Description | Example |
|--------|-------------|---------|
| `--mode single` | Process one question | Basic testing |
| `--mode continuous` | Monitor for multiple questions | During games |
| `--auto-click` | Automatically click answers | ⚠️ High risk |
| `--confidence 0.7` | Minimum confidence (0.0-1.0) | Higher = safer |
| `--ocr tesseract` | Use Tesseract instead of EasyOCR | Alternative OCR |
| `--interval 3.0` | Check every 3 seconds | Slower scanning |

## 🛡️ Safety Features

- **Emergency Stop**: Move mouse to top-left corner
- **Confidence Threshold**: Won't click unless confident
- **Fail-Safe**: PyAutoGUI fail-safe enabled
- **Rate Limiting**: Prevents excessive web requests

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "OCR not working" | Install tesseract: `brew install tesseract` |
| "No question found" | Make sure Kahoot is clearly visible |
| "Import errors" | Run `pip install -r requirements.txt` |
| "Can't find answers" | Check internet connection |
| "Clicking wrong spot" | Disable auto-click, use debug mode |

## 📱 Debug Mode

Check what the agent sees:
```bash
python example_usage.py
# Select option 4: Debug Mode
```

This saves debug images:
- `debug_question.png` - What it captured as the question
- `debug_answers.png` - What it captured as answer options

## ⚠️ Important Warnings

1. **Educational Use Only**: This tool is for learning purposes
2. **Check Terms of Service**: May violate Kahoot's ToS
3. **School Policies**: Could be considered cheating
4. **Use Responsibly**: Don't ruin the fun for others
5. **Test First**: Always test without auto-click first

## 🎮 Example Workflow

1. **Open Kahoot** in your browser
2. **Position the window** so questions are clearly visible
3. **Start the agent:**
   ```bash
   python kahoot_agent.py --mode single
   ```
4. **Wait for results** - it will show the recommended answer
5. **Manually click** the answer (safer than auto-click)

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed information
- Try [example_usage.py](example_usage.py) for interactive examples
- Customize settings in `kahoot_agent.py` for your needs
- Run tests with `test_components.py` to verify everything works

## 🆘 Need Help?

1. Run the test script: `python test_components.py`
2. Check debug images in debug mode
3. Review error messages for specific issues
4. Ensure all dependencies are installed correctly

---

**Remember: Use this tool ethically and responsibly! 🎓**
