// Content script for Kahoot Agent Chrome Extension
// This runs directly on the Kahoot page and can access the DOM

class KahootAgent {
    constructor(config = {}) {
        this.config = {
            autoClick: config.autoClick || false,
            continuous: config.continuous || false,
            confidence: config.confidence || 0.7,
            searchDelay: 2000,
            ...config
        };
        
        this.isRunning = false;
        this.observer = null;
        this.lastQuestion = '';
        this.questionCount = 0;
        
        console.log('Kahoot Agent initialized', this.config);
    }
    
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        console.log('Kahoot Agent started');
        
        if (this.config.continuous) {
            this.startContinuousMonitoring();
        } else {
            this.findAnswer();
        }
        
        this.showNotification('Kahoot Agent started', 'success');
    }
    
    stop() {
        this.isRunning = false;
        
        if (this.observer) {
            this.observer.disconnect();
            this.observer = null;
        }
        
        console.log('Kahoot Agent stopped');
        this.showNotification('Kahoot Agent stopped', 'info');
    }
    
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
    }
    
    startContinuousMonitoring() {
        // Monitor for question changes using MutationObserver
        this.observer = new MutationObserver((mutations) => {
            for (let mutation of mutations) {
                if (mutation.type === 'childList' || mutation.type === 'attributes') {
                    this.checkForNewQuestion();
                }
            }
        });
        
        this.observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['class']
        });
        
        // Also check immediately
        this.checkForNewQuestion();
    }
    
    checkForNewQuestion() {
        if (!this.isRunning) return;
        
        const question = this.extractQuestion();
        if (question && question !== this.lastQuestion) {
            this.lastQuestion = question;
            this.questionCount++;
            
            console.log(`New question detected (#${this.questionCount}):`, question);
            
            // Small delay to ensure all elements are loaded
            setTimeout(() => {
                this.findAnswer();
            }, 1000);
        }
    }
    
    extractQuestion() {
        // Try multiple selectors for different Kahoot layouts
        const questionSelectors = [
            '[data-functional-selector="block-title"]',
            '.question-title',
            '.question-text',
            '[class*="question"]',
            '[class*="title"]',
            'h1', 'h2'
        ];
        
        for (let selector of questionSelectors) {
            const element = document.querySelector(selector);
            if (element && element.textContent.trim()) {
                const text = element.textContent.trim();
                // Filter out non-question text
                if (text.length > 3 && !text.includes('Kahoot') && !text.includes('players')) {
                    return text;
                }
            }
        }
        
        return null;
    }
    
    extractAnswerOptions() {
        // Try multiple selectors for answer options
        const answerSelectors = [
            '[data-functional-selector="answer-option"]',
            '.answer-option',
            '.option-text',
            '[class*="answer"]',
            '[class*="option"]',
            'button[class*="answer"]'
        ];
        
        const answers = [];
        const answerElements = [];
        
        for (let selector of answerSelectors) {
            const elements = document.querySelectorAll(selector);
            if (elements.length >= 2) {
                elements.forEach(element => {
                    const text = element.textContent.trim();
                    if (text && text.length > 0) {
                        answers.push(text);
                        answerElements.push(element);
                    }
                });
                break;
            }
        }
        
        return { answers, elements: answerElements };
    }
    
    async findAnswer() {
        if (!this.isRunning) return;
        
        const question = this.extractQuestion();
        if (!question) {
            console.log('No question found on page');
            this.showNotification('No question found', 'warning');
            return;
        }
        
        const { answers, elements } = this.extractAnswerOptions();
        if (answers.length === 0) {
            console.log('No answer options found');
            this.showNotification('No answers found', 'warning');
            return;
        }
        
        console.log('Question:', question);
        console.log('Answer options:', answers);
        
        this.showNotification(`Searching for: "${question}"`, 'info');
        
        try {
            const result = await this.searchForAnswer(question, answers);
            
            console.log('Search result:', result);
            
            if (result.answer) {
                const confidence = Math.round(result.confidence * 100);
                this.showNotification(
                    `Best answer: "${result.answer}" (${confidence}% confidence)`,
                    'success'
                );
                
                if (this.config.autoClick && result.confidence >= this.config.confidence) {
                    this.clickAnswer(result.answer, elements, answers);
                } else if (this.config.autoClick) {
                    this.showNotification(
                        `Confidence too low (${confidence}% < ${Math.round(this.config.confidence * 100)}%)`,
                        'warning'
                    );
                }
            } else {
                this.showNotification('No answer found', 'error');
            }
            
        } catch (error) {
            console.error('Error searching for answer:', error);
            this.showNotification('Search error occurred', 'error');
        }
    }
    
    async searchForAnswer(question, answers) {
        // Create search query
        const query = this.cleanQuery(question) + ' ' + answers.join(' ');
        
        try {
            // Use Google search via CORS proxy or direct search
            const searchResults = await this.performWebSearch(query);
            
            // Score the answers based on search results
            const scores = this.scoreAnswers(searchResults, answers);
            
            // Find best answer
            const bestAnswer = this.findBestAnswer(scores);
            
            return bestAnswer;
            
        } catch (error) {
            console.error('Search error:', error);
            return { answer: null, confidence: 0 };
        }
    }
    
    cleanQuery(question) {
        // Clean the question for better search results
        return question
            .replace(/[?!.]+$/, '')
            .replace(/^(what|which|who|where|when|how|why)\s+/i, '')
            .trim();
    }
    
    async performWebSearch(query) {
        // Try multiple search approaches
        try {
            // Method 1: Wikipedia search
            const wikiResults = await this.searchWikipedia(query);
            if (wikiResults) return wikiResults;
            
            // Method 2: Duck Duck Go search
            const ddgResults = await this.searchDuckDuckGo(query);
            if (ddgResults) return ddgResults;
            
            // Method 3: Fallback to built-in knowledge
            return this.useBuiltInKnowledge(query);
            
        } catch (error) {
            console.error('All search methods failed:', error);
            return '';
        }
    }
    
    async searchWikipedia(query) {
        try {
            const url = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(query)}`;
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.extract) {
                return data.extract;
            }
        } catch (error) {
            console.log('Wikipedia search failed:', error);
        }
        return null;
    }
    
    async searchDuckDuckGo(query) {
        try {
            // DuckDuckGo instant answer API
            const url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1&skip_disambig=1`;
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.Abstract) {
                return data.Abstract;
            } else if (data.Definition) {
                return data.Definition;
            }
        } catch (error) {
            console.log('DuckDuckGo search failed:', error);
        }
        return null;
    }
    
    useBuiltInKnowledge(query) {
        // Basic knowledge base for common questions
        const knowledge = {
            'switzerland': 'Switzerland flag is red with white cross',
            'france': 'France capital is Paris',
            'germany': 'Germany capital is Berlin',
            'italy': 'Italy capital is Rome',
            'spain': 'Spain capital is Madrid',
            'england': 'England capital is London',
            'usa': 'USA capital is Washington DC',
            '2+2': 'four',
            '3+3': 'six',
            '4+4': 'eight'
        };
        
        const lowerQuery = query.toLowerCase();
        for (let [key, value] of Object.entries(knowledge)) {
            if (lowerQuery.includes(key)) {
                return value;
            }
        }
        
        return '';
    }
    
    scoreAnswers(searchResults, answers) {
        const scores = {};
        const text = searchResults.toLowerCase();
        
        answers.forEach(answer => {
            const answerLower = answer.toLowerCase();
            let score = 0;
            
            // Direct mention
            if (text.includes(answerLower)) {
                score += 10;
            }
            
            // Word-level matching
            const words = answerLower.split(' ');
            words.forEach(word => {
                if (word.length > 2 && text.includes(word)) {
                    score += 2;
                }
            });
            
            scores[answer] = score;
        });
        
        return scores;
    }
    
    findBestAnswer(scores) {
        let bestAnswer = null;
        let maxScore = 0;
        
        for (let [answer, score] of Object.entries(scores)) {
            if (score > maxScore) {
                maxScore = score;
                bestAnswer = answer;
            }
        }
        
        // Normalize confidence (rough calculation)
        const confidence = Math.min(maxScore / 10, 1.0);
        
        return { answer: bestAnswer, confidence };
    }
    
    clickAnswer(targetAnswer, elements, answers) {
        const index = answers.findIndex(answer => 
            answer.toLowerCase().includes(targetAnswer.toLowerCase()) ||
            targetAnswer.toLowerCase().includes(answer.toLowerCase())
        );
        
        if (index >= 0 && elements[index]) {
            setTimeout(() => {
                elements[index].click();
                this.showNotification(`Clicked: "${targetAnswer}"`, 'success');
                console.log('Answer clicked:', targetAnswer);
            }, 500);
        } else {
            console.log('Could not find element to click for:', targetAnswer);
        }
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            z-index: 10000;
            font-family: Arial, sans-serif;
            font-size: 14px;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        `;
        
        const colors = {
            success: '#4CAF50',
            error: '#f44336',
            warning: '#ff9800',
            info: '#2196F3'
        };
        
        notification.style.backgroundColor = colors[type] || colors.info;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    notification.remove();
                }, 300);
            }
        }, 5000);
    }
}

// Make the class globally available
window.KahootAgent = KahootAgent;

// Auto-start in basic mode if agent is not already running
if (!window.kahootAgent && window.location.href.includes('kahoot.it')) {
    console.log('Kahoot Agent content script loaded');
}
