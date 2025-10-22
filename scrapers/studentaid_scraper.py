"""
Alternative StudentAid.gov data integration using official sources
Since StudentAid.gov uses JavaScript for dynamic content loading,
we'll use their official data sources and RSS feeds instead.
"""
import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import *

class StudentAidDataIntegration:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        # Official data sources
        self.data_sources = {
            'ed_gov_rss': 'https://www.ed.gov/news/rss',
            'ed_gov_news': 'https://www.ed.gov/news',
            'studentaid_data_center': 'https://studentaid.gov/data-center'
        }
    
    def fetch_ed_gov_rss(self) -> List[Dict]:
        """
        Fetch RSS feed from ed.gov for education-related news
        """
        articles = []
        
        try:
            feed = feedparser.parse(self.data_sources['ed_gov_rss'])
            
            for entry in feed.entries[:5]:  # Limit to 5 items
                if hasattr(entry, 'title') and hasattr(entry, 'summary'):
                    # Filter for student aid related content
                    title_lower = entry.title.lower()
                    summary_lower = entry.summary.lower()
                    
                    if any(keyword in title_lower or keyword in summary_lower 
                          for keyword in ['student', 'loan', 'aid', 'financial aid', 'pslf', 'forgiveness']):
                        articles.append({
                            'title': entry.title,
                            'description': entry.summary,
                            'url': entry.link,
                            'source': 'U.S. Department of Education',
                            'published_at': entry.get('published', ''),
                            'content_type': 'studentaid_official'
                        })
                        
        except Exception as e:
            print(f"Error fetching ed.gov RSS: {e}")
            
        return articles
    
    def fetch_studentaid_data_updates(self) -> List[Dict]:
        """
        Check for new datasets or updates in the StudentAid data center
        """
        articles = []
        
        try:
            response = requests.get(self.data_sources['studentaid_data_center'], 
                                 headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Since this page uses JavaScript, we'll look for any static content
            # that might indicate new data or updates
            if 'new' in response.text.lower() or 'updated' in response.text.lower():
                articles.append({
                    'title': 'StudentAid.gov Data Center Updates',
                    'description': 'New data or updates available in the StudentAid.gov Data Center. Check the official data center for the latest information.',
                    'url': self.data_sources['studentaid_data_center'],
                    'source': 'StudentAid.gov Data Center',
                    'published_at': datetime.now().strftime('%Y-%m-%d'),
                    'content_type': 'studentaid_data_update'
                })
                
        except Exception as e:
            print(f"Error checking StudentAid data center: {e}")
            
        return articles
    
    def get_studentaid_related_content(self) -> List[Dict]:
        """
        Get all StudentAid-related content from available sources
        
        Returns:
            List of StudentAid-related content
        """
        all_content = []
        
        print("Fetching U.S. Department of Education RSS feed...")
        ed_articles = self.fetch_ed_gov_rss()
        all_content.extend(ed_articles)
        print(f"  Found {len(ed_articles)} education-related articles")
        
        print("Checking StudentAid.gov data center...")
        data_updates = self.fetch_studentaid_data_updates()
        all_content.extend(data_updates)
        print(f"  Found {len(data_updates)} data updates")
        
        return all_content

# Update the original StudentAidScraper to use this new approach
class StudentAidScraper(StudentAidDataIntegration):
    """
    Updated StudentAid scraper that uses official data sources
    instead of trying to scrape JavaScript-heavy pages
    """
    
    def get_all_studentaid_content(self) -> List[Dict]:
        """
        Get all StudentAid-related content using official sources
        
        Returns:
            List of StudentAid-related content
        """
        return self.get_studentaid_related_content()