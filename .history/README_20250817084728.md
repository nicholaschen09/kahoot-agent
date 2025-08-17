# Kahoot Agent 🤖

An automated Kahoot question-answering agent using OCR and web scraping. This tool captures your screen, extracts questions using OCR, searches for answers online, and can optionally click the correct answer automatically.

## ⚠️ Disclaimer

**This tool is for educational purposes only.** Using automated tools to answer Kahoot questions may:
- Violate Kahoot's terms of service
- Be considered cheating in educational settings
- Get you banned from Kahoot
- Be against the rules of your school/organization

Use responsibly and at your own risk!

## 🚀 Features

- **Screen Capture**: Automatically captures the Kahoot window
- **OCR Text Extraction**: Uses EasyOCR or Tesseract to extract questions and answers
- **Web Search**: Searches Google and educational sites for answers
- **Smart Answer Selection**: Analyzes search results to find the best answer
- **Automated Clicking**: Optionally clicks the correct answer (use with caution!)
- **Color Detection**: Detects Kahoot's colored answer buttons
- **Continuous Monitoring**: Can run continuously to handle multiple questions

## 📋 Prerequisites

### System Requirements
- Python 3.8 or higher
- macOS, Windows, or Linux
- Tesseract OCR (for Tesseract mode)

### Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tesseract-ocr
```

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

## 🛠️ Installation

1. **Clone or download the project:**
```bash
cd kahoot-agent
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
python kahoot_agent.py --help
```

## 🎯 Usage

### Basic Usage (Single Question)

1. Open Kahoot in your browser and navigate to a question
2. Run the agent:
```bash
python kahoot_agent.py --mode single
```
3. The agent will capture the screen, extract the question, search for answers, and display the result

### Continuous Mode

Monitor for multiple questions automatically:
```bash
python kahoot_agent.py --mode continuous
```

### Auto-Click Mode (Use with Caution!)

⚠️ **Warning**: This will automatically click answers. Make sure you understand the risks!

```bash
python kahoot_agent.py --mode continuous --auto-click
```

### Advanced Options

```bash
# Use Tesseract instead of EasyOCR
python kahoot_agent.py --ocr tesseract

# Set minimum confidence for auto-clicking (0.0-1.0)
python kahoot_agent.py --auto-click --confidence 0.5

# Change scan interval for continuous mode
python kahoot_agent.py --mode continuous --interval 3.0
```

## 🔧 Configuration

### Command Line Arguments

- `--mode`: Run mode (`single` or `continuous`)
- `--auto-click`: Enable automatic clicking
- `--ocr`: OCR engine (`easyocr` or `tesseract`)
- `--confidence`: Minimum confidence for auto-clicking (0.0-1.0)
- `--interval`: Scan interval in seconds for continuous mode

### Configuration Options in Code

Edit `kahoot_agent.py` to modify:
- `min_confidence`: Minimum confidence threshold
- `scan_interval`: Time between scans
- Answer search strategies
- Screen capture regions

## 🛡️ Safety Features

- **Fail-safe**: Move mouse to top-left corner to abort
- **Confidence Threshold**: Won't auto-click unless confidence is above threshold
- **Rate Limiting**: Prevents too many rapid web requests
- **Emergency Stop**: Built-in emergency stop functionality

## 📁 Project Structure

```
kahoot-agent/
├── kahoot_agent.py      # Main orchestration logic
├── screen_capture.py    # Screen capture functionality
├── ocr_extractor.py     # OCR text extraction
├── answer_searcher.py   # Web searching for answers
├── auto_clicker.py      # Automated clicking
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔍 How It Works

1. **Screen Capture**: Takes screenshots of the Kahoot window
2. **Image Processing**: Separates question and answer areas
3. **OCR Extraction**: Extracts text from images using OCR
4. **Answer Search**: Searches Google and educational sites for answers
5. **Answer Scoring**: Analyzes search results and scores possible answers
6. **Answer Selection**: Selects the highest-scoring answer
7. **Clicking** (optional): Automatically clicks the selected answer

## 🐛 Troubleshooting

### Common Issues

**OCR not working:**
- Make sure Tesseract is installed correctly
- Try switching between EasyOCR and Tesseract: `--ocr tesseract` or `--ocr easyocr`
- Check that the Kahoot window is clearly visible

**Screen capture issues:**
- Make sure Kahoot is in full screen or clearly visible
- Try adjusting screen resolution
- Check debug images (`debug_question.png`, `debug_answers.png`)

**Search not finding answers:**
- Check your internet connection
- Some questions may not have easily searchable answers
- Try with different types of questions

**Clicking not working:**
- Make sure auto-click is enabled: `--auto-click`
- Check confidence threshold: `--confidence 0.3`
- Verify button positions are detected correctly

### Debug Mode

The agent saves debug images:
- `debug_question.png`: Captured question area
- `debug_answers.png`: Captured answers area

Check these images to see what the agent is capturing.

## 🔬 Testing

Test individual components:

```bash
# Test screen capture
python screen_capture.py

# Test OCR extraction
python ocr_extractor.py

# Test answer searching
python answer_searcher.py
```

## ⚡ Performance Tips

- Use EasyOCR for better accuracy (default)
- Ensure good lighting and clear text on screen
- Close unnecessary applications to improve performance
- Use a stable internet connection for faster searches

## 🤝 Contributing

This is an educational project. Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Share your experience

## 📜 License

This project is for educational purposes only. Use responsibly and in accordance with your local laws and the terms of service of the platforms you're using.

## 🙏 Acknowledgments

- EasyOCR for excellent OCR capabilities
- Tesseract OCR for open-source OCR
- OpenCV for computer vision functionality
- BeautifulSoup for web scraping
- PyAutoGUI for automation capabilities
