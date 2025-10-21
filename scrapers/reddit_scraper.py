"""
Reddit scraping module for financial subreddits
"""
import praw
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import *
from datetime import datetime, timedelta

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    
    def get_trending_posts(self, subreddit_name: str, limit: int = 10) -> List[Dict]:
        """
        Get trending posts from a specific subreddit
        
        Args:
            subreddit_name: Name of the subreddit (without r/)
            limit: Maximum number of posts to fetch
            
        Returns:
            List of post dictionaries
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            posts = []
            for submission in subreddit.hot(limit=limit):
                # Skip stickied posts and ads
                if submission.stickied or submission.is_self == False:
                    continue
                    
                posts.append({
                    'title': submission.title,
                    'content': submission.selftext[:500] if submission.selftext else '',  # First 500 chars
                    'url': f"https://reddit.com{submission.permalink}",
                    'source': f"r/{subreddit_name}",
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'created_utc': submission.created_utc,
                    'content_type': 'reddit_post'
                })
            
            return posts
            
        except Exception as e:
            print(f"Error fetching from r/{subreddit_name}: {e}")
            return []
    
    def get_all_reddit_content(self) -> List[Dict]:
        """
        Get trending posts from all configured subreddits
        """
        all_posts = []
        
        for subreddit in REDDIT_SUBREDDITS:
            posts = self.get_trending_posts(subreddit, limit=MAX_REDDIT_POSTS)
            all_posts.extend(posts)
        
        # Sort by score (most upvoted first)
        all_posts.sort(key=lambda x: x['score'], reverse=True)
        
        return all_posts[:MAX_REDDIT_POSTS * len(REDDIT_SUBREDDITS)]
    
    def get_recent_discussions(self, subreddit_name: str, hours_back: int = 24) -> List[Dict]:
        """
        Get recent discussion posts that might indicate trending topics
        
        Args:
            subreddit_name: Name of the subreddit
            hours_back: How many hours back to look
            
        Returns:
            List of discussion posts
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            cutoff_time = datetime.now().timestamp() - (hours_back * 3600)
            
            discussions = []
            for submission in subreddit.new(limit=50):
                # Skip if too old
                if submission.created_utc < cutoff_time:
                    continue
                    
                # Look for question posts or discussion posts
                title_lower = submission.title.lower()
                if any(keyword in title_lower for keyword in ['question', 'help', 'advice', 'what', 'how', 'why', 'should']):
                    discussions.append({
                        'title': submission.title,
                        'content': submission.selftext[:300] if submission.selftext else '',
                        'url': f"https://reddit.com{submission.permalink}",
                        'source': f"r/{subreddit_name}",
                        'score': submission.score,
                        'num_comments': submission.num_comments,
                        'created_utc': submission.created_utc,
                        'content_type': 'reddit_discussion'
                    })
            
            return discussions
            
        except Exception as e:
            print(f"Error fetching discussions from r/{subreddit_name}: {e}")
            return []
