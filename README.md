# Kahoot Agent Chrome Extension

A Chrome extension that automatically finds answers to Kahoot questions using web search and AI.

## Features

- **Direct DOM Access**: No screen capture needed - reads questions directly from the page
- **Smart Search**: Uses Wikipedia, DuckDuckGo, and built-in knowledge base
- **Auto-Click**: Optionally clicks answers automatically (use with caution!)
- **Continuous Mode**: Monitors for new questions automatically
- **Confidence Scoring**: Only acts when confident about the answer
- **Modern UI**: Clean, intuitive popup interface

## Installation

### Method 1: Load as Unpacked Extension (Recommended for Development)

1. **Open Chrome Extensions Page:**
   - Go to `chrome://extensions/`
   - Or click menu → More tools → Extensions

2. **Enable Developer Mode:**
   - Toggle "Developer mode" in the top right

3. **Load the Extension:**
   - Click "Load unpacked"
   - Select the `chrome-extension` folder

4. **Pin the Extension:**
   - Click the puzzle piece icon in Chrome toolbar
   - Pin "Kahoot Agent" for easy access

### Method 2: Install as .crx File (Coming Soon)

## Usage

### Quick Start

1. **Join a Kahoot Game:**
   - Go to https://kahoot.it/
   - Enter game PIN and join

2. **Open Extension:**
   - Click the Kahoot Agent icon in your toolbar
   - Or use the keyboard shortcut

3. **Find Answers:**
   - Click "Find Answer Now" for single questions
   - Or click "Start Agent" for continuous monitoring

### Settings

- **Auto-click answers**: Automatically clicks the best answer
- **Confidence threshold**: Minimum confidence required to auto-click (0-100%)
- **Continuous mode**: Monitors for new questions automatically

### Safety Features

- **Confidence Threshold**: Won't click unless highly confident
- **Manual Override**: Can always find answers without clicking
- **Educational Warning**: Reminds users of responsible usage

## How It Works

1. **Question Detection**: Monitors the Kahoot page for new questions
2. **DOM Extraction**: Reads question text and answer options directly from HTML
3. **Web Search**: Searches Wikipedia, DuckDuckGo, and knowledge bases
4. **Answer Scoring**: Analyzes search results to score each answer option
5. **Smart Selection**: Chooses the highest-scoring answer with confidence rating

## Technical Details

### Files Structure
```
chrome-extension/
├── manifest.json        # Extension configuration
├── popup.html          # Extension popup UI
├── popup.js            # Popup logic and controls
├── content.js          # Main agent logic (runs on Kahoot pages)
└── README.md           # This file
```

### Permissions Required
- `activeTab`: Access to current tab content
- `scripting`: Execute scripts on Kahoot pages
- `kahoot.it/*`: Access to Kahoot domains

### APIs Used
- Wikipedia REST API for general knowledge
- DuckDuckGo Instant Answer API for search results
- Chrome Extension APIs for DOM access

## Advantages Over Python Version

### ✅ Better
- **No OCR needed** - reads text directly from DOM
- **Faster and more accurate** - no image processing
- **Better integration** - runs inside the browser
- **Automatic updates** - detects new questions instantly
- **No installation hassles** - just load in Chrome

### ✅ More Reliable
- **No screen capture issues** - works regardless of window focus
- **Better element detection** - finds buttons precisely
- **Cross-platform** - works on any OS with Chrome
- **No Python dependencies** - pure JavaScript

## Responsible Usage

### ⚠️ Important Warnings

- **Educational Purpose Only**: This tool is for learning about web automation
- **Check Policies**: May violate your school's academic integrity policies
- **Respect Others**: Don't use to gain unfair advantages in competitive settings
- **Terms of Service**: May violate Kahoot's terms of use

### 🎓 Educational Value

This extension demonstrates:
- Chrome extension development
- DOM manipulation and monitoring
- Web APIs and CORS handling
- Search algorithms and scoring
- Modern JavaScript practices

## Troubleshooting

### Extension Not Working
- Make sure you're on a Kahoot page (kahoot.it)
- Check that Developer Mode is enabled
- Reload the extension if needed

### No Questions Detected
- Wait for a question to appear on screen
- Make sure the question is fully loaded
- Try refreshing the Kahoot page

### Search Not Finding Answers
- Check your internet connection
- Some questions may not have easily searchable answers
- Try with simpler, more common questions

### Auto-Click Not Working
- Ensure auto-click is enabled in settings
- Check that confidence threshold isn't too high
- Verify the extension has proper permissions

## Development

### Testing
1. Load extension in Chrome
2. Go to kahoot.it and join a game
3. Test with simple questions first
4. Check browser console for debug info

### Debugging
- Open Chrome DevTools on Kahoot page
- Check Console tab for error messages
- Use Network tab to monitor API calls

### Contributing
- Feel free to improve the search algorithms
- Add support for more question types
- Enhance the UI and user experience

## License

Educational use only. Use responsibly and ethically.
