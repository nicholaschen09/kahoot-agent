// Background script for Kahoot Agent Chrome Extension
// Handles side panel opening and management

chrome.action.onClicked.addListener(async (tab) => {
    // Open the side panel when extension icon is clicked
    try {
        await chrome.sidePanel.open({ windowId: tab.windowId });
    } catch (error) {
        console.error('Failed to open side panel:', error);
        
        // Fallback: try to set the side panel for this tab
        try {
            await chrome.sidePanel.setOptions({
                tabId: tab.id,
                path: 'popup.html',
                enabled: true
            });
            await chrome.sidePanel.open({ windowId: tab.windowId });
        } catch (fallbackError) {
            console.error('Fallback also failed:', fallbackError);
        }
    }
});

// Enable side panel on Kahoot pages
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        const isKahootPage = tab.url.includes('kahoot.it') || tab.url.includes('play.kahoot.it');
        
        if (isKahootPage) {
            try {
                await chrome.sidePanel.setOptions({
                    tabId: tabId,
                    path: 'popup.html',
                    enabled: true
                });
            } catch (error) {
                console.error('Failed to enable side panel for Kahoot page:', error);
            }
        }
    }
});

// Handle extension installation
chrome.runtime.onInstalled.addListener(() => {
    console.log('Kahoot Agent extension installed');
});
