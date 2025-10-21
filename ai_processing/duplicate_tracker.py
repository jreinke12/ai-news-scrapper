"""
Duplicate tracking system to avoid repetitive content
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Set
import hashlib

class DuplicateTracker:
    def __init__(self, storage_file: str = "content_history.json"):
        self.storage_file = storage_file
        self.content_history = self._load_history()
    
    def _load_history(self) -> Dict:
        """Load content history from file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_history(self):
        """Save content history to file"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.content_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving content history: {e}")
    
    def _generate_content_hash(self, content: Dict) -> str:
        """
        Generate a hash for content to detect duplicates
        
        Args:
            content: Content dictionary
            
        Returns:
            Hash string
        """
        # Create a string from key content fields
        content_string = f"{content.get('title', '')}{content.get('url', '')}{content.get('source', '')}"
        return hashlib.md5(content_string.encode()).hexdigest()
    
    def _is_recent_duplicate(self, content_hash: str, days_back: int = 3) -> bool:
        """
        Check if content is a recent duplicate
        
        Args:
            content_hash: Hash of the content
            days_back: How many days back to check
            
        Returns:
            True if duplicate found within time range
        """
        if content_hash not in self.content_history:
            return False
        
        last_seen = datetime.fromisoformat(self.content_history[content_hash]['last_seen'])
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        return last_seen > cutoff_date
    
    def _is_similar_title(self, new_title: str, days_back: int = 3) -> bool:
        """
        Check if there's a similar title in recent history
        
        Args:
            new_title: Title to check
            days_back: How many days back to check
            
        Returns:
            True if similar title found
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for content_hash, data in self.content_history.items():
            if datetime.fromisoformat(data['last_seen']) > cutoff_date:
                existing_title = data.get('title', '').lower()
                new_title_lower = new_title.lower()
                
                # Check for high similarity (simple word overlap)
                existing_words = set(existing_title.split())
                new_words = set(new_title_lower.split())
                
                # If more than 70% of words overlap, consider it similar
                if len(existing_words) > 0 and len(new_words) > 0:
                    overlap = len(existing_words.intersection(new_words))
                    similarity = overlap / min(len(existing_words), len(new_words))
                    
                    if similarity > 0.7:
                        return True
        
        return False
    
    def filter_duplicates(self, content_list: List[Dict], strict_mode: bool = False) -> List[Dict]:
        """
        Filter out duplicate content from a list
        
        Args:
            content_list: List of content dictionaries
            strict_mode: If True, use stricter duplicate detection
            
        Returns:
            Filtered list without duplicates
        """
        filtered_content = []
        
        for content in content_list:
            content_hash = self._generate_content_hash(content)
            title = content.get('title', '')
            
            # Check for exact duplicates
            if self._is_recent_duplicate(content_hash, days_back=3):
                print(f"Filtering exact duplicate: {title[:50]}...")
                continue
            
            # Check for similar titles (only in strict mode)
            if strict_mode and self._is_similar_title(title, days_back=3):
                print(f"Filtering similar title: {title[:50]}...")
                continue
            
            # Add to filtered list
            filtered_content.append(content)
            
            # Update history
            self.content_history[content_hash] = {
                'title': title,
                'url': content.get('url', ''),
                'source': content.get('source', ''),
                'last_seen': datetime.now().isoformat()
            }
        
        # Save updated history
        self._save_history()
        
        return filtered_content
    
    def get_recent_topics(self, days_back: int = 7) -> List[str]:
        """
        Get list of recent topics that have been covered
        
        Args:
            days_back: How many days back to look
            
        Returns:
            List of recent topic keywords
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_topics = []
        
        for content_hash, data in self.content_history.items():
            if datetime.fromisoformat(data['last_seen']) > cutoff_date:
                title = data.get('title', '').lower()
                
                # Extract key financial terms
                financial_terms = [
                    'student loan', 'pslf', 'forgiveness', 'inflation', 
                    'housing', 'credit', 'debt', 'investment', 'budget',
                    'retirement', 'tax', 'mortgage', 'refinance'
                ]
                
                for term in financial_terms:
                    if term in title and term not in recent_topics:
                        recent_topics.append(term)
        
        return recent_topics
    
    def cleanup_old_entries(self, days_back: int = 30):
        """
        Remove old entries from history to keep file size manageable
        
        Args:
            days_back: Remove entries older than this many days
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        # Create new history with only recent entries
        new_history = {}
        for content_hash, data in self.content_history.items():
            if datetime.fromisoformat(data['last_seen']) > cutoff_date:
                new_history[content_hash] = data
        
        self.content_history = new_history
        self._save_history()
        
        print(f"Cleaned up content history. Removed entries older than {days_back} days.")
