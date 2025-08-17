// Popup script for Kahoot Agent Chrome Extension

class KahootAgentPopup {
    constructor() {
        this.isActive = false;
        this.autoClick = false;
        this.continuousMode = false;
        this.confidence = 70;

        this.initializeElements();
        this.bindEvents();
        this.loadSettings();
        this.checkKahootPage();
    }

    initializeElements() {
        this.startBtn = document.getElementById('startAgent');
        this.stopBtn = document.getElementById('stopAgent');
        this.findBtn = document.getElementById('findAnswer');
        this.status = document.getElementById('status');
        this.autoClickToggle = document.getElementById('autoClickToggle');
        this.continuousToggle = document.getElementById('continuousToggle');
        this.confidenceSlider = document.getElementById('confidenceSlider');
        this.confidenceValue = document.getElementById('confidenceValue');
    }

    bindEvents() {
        this.startBtn.addEventListener('click', () => this.startAgent());
        this.stopBtn.addEventListener('click', () => this.stopAgent());
        this.findBtn.addEventListener('click', () => this.findAnswerNow());

        this.autoClickToggle.addEventListener('click', () => this.toggleAutoClick());
        this.continuousToggle.addEventListener('click', () => this.toggleContinuous());

        this.confidenceSlider.addEventListener('input', (e) => {
            this.confidence = e.target.value;
            this.confidenceValue.textContent = e.target.value + '%';
            this.saveSettings();
        });
    }

    async checkKahootPage() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            const isKahoot = tab.url && (
                tab.url.includes('kahoot.it') ||
                tab.url.includes('play.kahoot.it')
            );

            if (!isKahoot) {
                this.status.textContent = 'Not on Kahoot page';
                this.status.className = 'status status-inactive';
                this.startBtn.disabled = true;
                this.findBtn.disabled = true;
            } else {
                this.status.textContent = 'Ready to assist';
                this.status.className = 'status status-inactive';
                this.startBtn.disabled = false;
                this.findBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error checking page:', error);
        }
    }

    async startAgent() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

            await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                func: this.injectAgent,
                args: [{
                    autoClick: this.autoClick,
                    continuous: this.continuousMode,
                    confidence: this.confidence / 100
                }]
            });

            this.isActive = true;
            this.updateUI();

        } catch (error) {
            console.error('Error starting agent:', error);
            this.status.textContent = 'Error starting agent';
        }
    }

    async stopAgent() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

            await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                func: () => {
                    if (window.kahootAgent) {
                        window.kahootAgent.stop();
                        delete window.kahootAgent;
                    }
                }
            });

            this.isActive = false;
            this.updateUI();

        } catch (error) {
            console.error('Error stopping agent:', error);
        }
    }

    async findAnswerNow() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

            await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                func: this.findSingleAnswer,
                args: [{
                    autoClick: this.autoClick,
                    confidence: this.confidence / 100
                }]
            });

        } catch (error) {
            console.error('Error finding answer:', error);
        }
    }

    toggleAutoClick() {
        this.autoClick = !this.autoClick;
        this.autoClickToggle.classList.toggle('active', this.autoClick);
        this.saveSettings();
    }

    toggleContinuous() {
        this.continuousMode = !this.continuousMode;
        this.continuousToggle.classList.toggle('active', this.continuousMode);
        this.saveSettings();
    }

    updateUI() {
        if (this.isActive) {
            this.startBtn.style.display = 'none';
            this.stopBtn.style.display = 'block';
            this.status.textContent = this.continuousMode ? 'Monitoring questions...' : 'Agent active';
            this.status.className = 'status status-active';
        } else {
            this.startBtn.style.display = 'block';
            this.stopBtn.style.display = 'none';
            this.status.textContent = 'Agent inactive';
            this.status.className = 'status status-inactive';
        }
    }

    saveSettings() {
        chrome.storage.local.set({
            autoClick: this.autoClick,
            continuous: this.continuousMode,
            confidence: this.confidence
        });
    }

    loadSettings() {
        chrome.storage.local.get(['autoClick', 'continuous', 'confidence'], (result) => {
            this.autoClick = result.autoClick || false;
            this.continuousMode = result.continuous || false;
            this.confidence = result.confidence || 70;

            this.autoClickToggle.classList.toggle('active', this.autoClick);
            this.continuousToggle.classList.toggle('active', this.continuousMode);
            this.confidenceSlider.value = this.confidence;
            this.confidenceValue.textContent = this.confidence + '%';
        });
    }

    // Function to inject into the page
    injectAgent(config) {
        // Import the main agent code
        if (!window.kahootAgent) {
            const script = document.createElement('script');
            script.src = chrome.runtime.getURL('content.js');
            document.head.appendChild(script);

            // Wait for script to load then start
            setTimeout(() => {
                if (window.KahootAgent) {
                    window.kahootAgent = new window.KahootAgent(config);
                    window.kahootAgent.start();
                }
            }, 1000);
        } else {
            window.kahootAgent.updateConfig(config);
            window.kahootAgent.start();
        }
    }

    // Function to find a single answer
    findSingleAnswer(config) {
        if (window.KahootAgent) {
            const agent = new window.KahootAgent(config);
            agent.findAnswer();
        } else {
            console.log('Kahoot Agent not loaded');
        }
    }
}

// Initialize popup when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new KahootAgentPopup();
});
