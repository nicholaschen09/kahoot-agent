"""
Answer searching module for finding correct answers to Kahoot questions.
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from typing import List, Dict, Optional, Tuple
import urllib.parse
from googlesearch import search as google_search


class AnswerSearcher:
    def __init__(self):
        """Initialize the answer searcher with default settings."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum seconds between requests
        
    def rate_limit(self):
        """Implement rate limiting to avoid being blocked."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def clean_query(self, question: str) -> str:
        """
        Clean and optimize question for search.
        
        Args:
            question: Raw question text
            
        Returns:
            Cleaned search query
        """
        if not question:
            return ""
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', question.strip())
        
        # Remove question marks and other punctuation that might interfere
        cleaned = re.sub(r'[?!.]+$', '', cleaned)
        
        # Remove common filler words that don't help with search
        filler_words = ['which', 'what', 'who', 'where', 'when', 'how', 'the following']
        words = cleaned.lower().split()
        words = [word for word in words if word not in filler_words]
        
        return ' '.join(words)
    
    def search_google(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Search Google for the query and return results.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with 'title', 'url', and 'snippet'
        """
        try:
            self.rate_limit()
            
            results = []
            search_results = google_search(query, num_results=num_results)
            
            for url in search_results:
                try:
                    # Get page content
                    response = self.session.get(url, timeout=5)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract title
                    title = soup.find('title')
                    title_text = title.text if title else "No title"
                    
                    # Extract relevant text content
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Get text content
                    text = soup.get_text()
                    
                    # Clean and limit snippet
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    # Limit snippet length
                    snippet = text[:500] + "..." if len(text) > 500 else text
                    
                    results.append({
                        'title': title_text,
                        'url': url,
                        'snippet': snippet
                    })
                    
                    self.rate_limit()
                    
                except Exception as e:
                    print(f"Error processing {url}: {e}")
                    continue
            
            return results
            
        except Exception as e:
            print(f"Google search error: {e}")
            return []
    
    def search_educational_sites(self, query: str) -> List[Dict[str, str]]:
        """
        Search specific educational sites for answers.
        
        Args:
            query: Search query
            
        Returns:
            List of search results
        """
        educational_sites = [
            "site:quizlet.com",
            "site:khanacademy.org", 
            "site:coursehero.com",
            "site:chegg.com",
            "site:wikipedia.org"
        ]
        
        all_results = []
        
        for site in educational_sites:
            site_query = f"{query} {site}"
            try:
                results = self.search_google(site_query, num_results=2)
                all_results.extend(results)
            except Exception as e:
                print(f"Error searching {site}: {e}")
                continue
        
        return all_results
    
    def extract_potential_answers(self, search_results: List[Dict[str, str]], 
                                answer_options: List[str]) -> Dict[str, float]:
        """
        Extract potential answers from search results and score them.
        
        Args:
            search_results: List of search results
            answer_options: List of possible answer options from Kahoot
            
        Returns:
            Dictionary mapping answer options to confidence scores
        """
        answer_scores = {option: 0.0 for option in answer_options}
        
        if not search_results or not answer_options:
            return answer_scores
        
        # Combine all search result text
        all_text = ""
        for result in search_results:
            all_text += f" {result.get('title', '')} {result.get('snippet', '')}"
        
        all_text = all_text.lower()
        
        # Score each answer option based on frequency and context
        for option in answer_options:
            if not option:
                continue
                
            option_lower = option.lower()
            
            # Direct mentions
            direct_mentions = all_text.count(option_lower)
            answer_scores[option] += direct_mentions * 2
            
            # Word-level matching
            option_words = option_lower.split()
            for word in option_words:
                if len(word) > 2:  # Skip very short words
                    word_count = all_text.count(word)
                    answer_scores[option] += word_count * 0.5
            
            # Context-based scoring (look for patterns like "answer is X")
            patterns = [
                rf"answer is {re.escape(option_lower)}",
                rf"correct answer.*{re.escape(option_lower)}",
                rf"{re.escape(option_lower)}.*is correct",
                rf"solution.*{re.escape(option_lower)}"
            ]
            
            for pattern in patterns:
                matches = len(re.findall(pattern, all_text))
                answer_scores[option] += matches * 5  # High score for direct answer indicators
        
        # Normalize scores
        max_score = max(answer_scores.values()) if answer_scores.values() else 1
        if max_score > 0:
            answer_scores = {k: v / max_score for k, v in answer_scores.items()}
        
        return answer_scores
    
    def find_best_answer(self, question: str, answer_options: List[str]) -> Tuple[str, float]:
        """
        Find the best answer for a given question and options.
        
        Args:
            question: The question text
            answer_options: List of possible answer options
            
        Returns:
            Tuple of (best_answer, confidence_score)
        """
        if not question or not answer_options:
            return "", 0.0
        
        # Clean the query
        search_query = self.clean_query(question)
        
        # Add answer options to the query for better context
        if answer_options:
            options_text = " ".join(answer_options)
            search_query = f"{search_query} {options_text}"
        
        print(f"Searching for: {search_query}")
        
        # Search for answers
        try:
            # First try general search
            general_results = self.search_google(search_query, num_results=3)
            
            # Then try educational sites
            educational_results = self.search_educational_sites(search_query)
            
            # Combine results
            all_results = general_results + educational_results
            
            # Score the answers
            scores = self.extract_potential_answers(all_results, answer_options)
            
            # Find the best answer
            if scores:
                best_answer = max(scores.items(), key=lambda x: x[1])
                return best_answer[0], best_answer[1]
            
        except Exception as e:
            print(f"Search error: {e}")
        
        # Fallback: return first option with low confidence
        return answer_options[0] if answer_options else "", 0.1


# Test function
if __name__ == "__main__":
    searcher = AnswerSearcher()
    
    # Test with sample question
    test_question = "What is the capital of France?"
    test_options = ["London", "Berlin", "Paris", "Madrid"]
    
    print(f"Question: {test_question}")
    print(f"Options: {test_options}")
    
    answer, confidence = searcher.find_best_answer(test_question, test_options)
    
    print(f"Best answer: {answer}")
    print(f"Confidence: {confidence:.2f}")
