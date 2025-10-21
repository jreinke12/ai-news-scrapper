"""
Test the working components
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_news():
    """Test news scraping"""
    print("Testing news scraper...")
    try:
        from scrapers.news_scraper import NewsScraper
        scraper = NewsScraper()
        articles = scraper.get_all_news()
        print(f"SUCCESS: Found {len(articles)} news articles")
        if articles:
            print(f"Sample: {articles[0]['title'][:60]}...")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_reddit():
    """Test Reddit scraping"""
    print("\nTesting Reddit scraper...")
    try:
        from scrapers.reddit_scraper import RedditScraper
        scraper = RedditScraper()
        posts = scraper.get_all_reddit_content()
        print(f"SUCCESS: Found {len(posts)} Reddit posts")
        if posts:
            print(f"Sample: {posts[0]['title'][:60]}...")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing working components...")
    print("=" * 50)
    
    news_ok = test_news()
    reddit_ok = test_reddit()
    
    print(f"\nResults:")
    print(f"News Scraper: {'PASS' if news_ok else 'FAIL'}")
    print(f"Reddit Scraper: {'PASS' if reddit_ok else 'FAIL'}")
    
    if news_ok and reddit_ok:
        print("\nGreat! The core scraping is working!")
        print("You just need to add YouTube API key and email credentials.")
    else:
        print("\nSome issues to fix first.")
