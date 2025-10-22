"""
News scraping module for financial news sources
"""
import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import *

class NewsScraper:
    def __init__(self):
        self.news_api_key = NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"
        
    def fetch_news_api_articles(self, query: str, days_back: int = 1) -> List[Dict]:
        """
        Fetch articles from NewsAPI
        
        Args:
            query: Search query for articles
            days_back: How many days back to search
            
        Returns:
            List of article dictionaries
        """
        if not self.news_api_key:
            print("Warning: NEWS_API_KEY not found. Skipping NewsAPI.")
            return []
            
        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)
        
        params = {
            'q': query,
            'from': from_date.strftime('%Y-%m-%d'),
            'to': to_date.strftime('%Y-%m-%d'),
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 20,
            'apiKey': self.news_api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                if article.get('title') and article.get('description'):
                    articles.append({
                        'title': article['title'],
                        'description': article['description'],
                        'url': article['url'],
                        'source': article['source']['name'],
                        'published_at': article['publishedAt'],
                        'content_type': 'news'
                    })
            
            return articles
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from NewsAPI: {e}")
            return []
    
    def fetch_rss_feeds(self) -> List[Dict]:
        """
        Fetch articles from RSS feeds of financial news sources
        """
        rss_feeds = [
            "https://feeds.bloomberg.com/markets/news.rss",
            "https://www.forbes.com/business/feed/",  # Forbes business news
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "https://feeds.marketwatch.com/marketwatch/topstories/",
            "https://feeds.finance.yahoo.com/rss/2.0/headline",  # Yahoo Finance (may be rate limited)
        ]
        
        articles = []
        
        for feed_url in rss_feeds:
            try:
                # Add delay to prevent rate limiting
                import time
                time.sleep(3)  # Increased to 3 seconds for better rate limiting
                
                feed = feedparser.parse(feed_url)
                
                # Check if feed was successfully parsed
                if hasattr(feed, 'status') and feed.status >= 400:
                    print(f"RSS feed {feed_url} returned error status: {feed.status}")
                    continue
                
                if not feed.entries:
                    print(f"No entries found in RSS feed: {feed_url}")
                    continue
                
                for entry in feed.entries[:5]:  # Limit to 5 per feed
                    if hasattr(entry, 'title') and hasattr(entry, 'summary'):
                        articles.append({
                            'title': entry.title,
                            'description': entry.summary,
                            'url': entry.link,
                            'source': feed.feed.get('title', 'RSS Feed'),
                            'published_at': entry.get('published', ''),
                            'content_type': 'rss'
                        })
                        
            except Exception as e:
                print(f"Error parsing RSS feed {feed_url}: {e}")
                continue
                
        return articles
    
    def search_adam_minsky_articles(self) -> List[Dict]:
        """
        Search for Adam Minsky articles using multiple approaches
        """
        articles = []
        
        # Approach 1: NewsAPI search
        search_queries = [
            '"Adam Minsky" + "student loan"',
            '"Adam Minsky" + "PSLF"',
            '"Adam Minsky" + "loan forgiveness"',
            '"Adam Minsky" + "student debt"'
        ]
        
        for query in search_queries:
            try:
                # Use NewsAPI to search for these specific queries
                query_articles = self.fetch_news_api_articles(query, days_back=7)
                for article in query_articles:
                    article['content_type'] = 'expert_article'
                    article['source'] = 'Adam Minsky via ' + article.get('source', 'Unknown')
                articles.extend(query_articles)
            except Exception as e:
                print(f"Error searching for Adam Minsky articles: {e}")
                continue
        
        # Approach 2: Direct site searches (if NewsAPI doesn't work)
        if not articles:
            print("No Adam Minsky articles found via NewsAPI, trying direct searches...")
            # This would require additional implementation for direct site scraping
            # For now, we'll rely on NewsAPI and RSS feeds
        
        return articles

    def get_all_news(self) -> List[Dict]:
        """
        Fetch news from all sources and combine them
        """
        all_articles = []
        
        # Fetch from NewsAPI for each search query
        for query in SEARCH_QUERIES:
            articles = self.fetch_news_api_articles(query)
            all_articles.extend(articles)
        
        # Fetch from RSS feeds
        rss_articles = self.fetch_rss_feeds()
        all_articles.extend(rss_articles)
        
        # Search for Adam Minsky articles
        adam_articles = self.search_adam_minsky_articles()
        all_articles.extend(adam_articles)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_articles = []
        
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        # Sort by published date (newest first)
        unique_articles.sort(
            key=lambda x: x.get('published_at', ''), 
            reverse=True
        )
        
        return unique_articles[:MAX_ARTICLES_PER_RUN]
