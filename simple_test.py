"""
Simple test script for the FitBUX Financial News Curator Agent
"""
import os
import sys
from datetime import datetime

def test_environment():
    """Test if all required environment variables are set"""
    print("Testing environment variables...")
    
    required_vars = [
        'OPENAI_API_KEY',
        'NEWS_API_KEY', 
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET',
        'YOUTUBE_API_KEY',
        'EMAIL_USER',
        'EMAIL_PASS'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("ERROR: Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    else:
        print("SUCCESS: All environment variables are set")
        return True

def test_news_scraper():
    """Test news scraping functionality"""
    print("\nTesting news scraper...")
    
    try:
        from scrapers.news_scraper import NewsScraper
        scraper = NewsScraper()
        articles = scraper.get_all_news()
        
        print(f"SUCCESS: Found {len(articles)} news articles")
        if articles:
            print(f"  Sample: {articles[0]['title'][:50]}...")
        return True
        
    except Exception as e:
        print(f"ERROR: News scraper error: {e}")
        return False

def test_reddit_scraper():
    """Test Reddit scraping functionality"""
    print("\nTesting Reddit scraper...")
    
    try:
        from scrapers.reddit_scraper import RedditScraper
        scraper = RedditScraper()
        posts = scraper.get_all_reddit_content()
        
        print(f"SUCCESS: Found {len(posts)} Reddit posts")
        if posts:
            print(f"  Sample: {posts[0]['title'][:50]}...")
        return True
        
    except Exception as e:
        print(f"ERROR: Reddit scraper error: {e}")
        return False

def test_youtube_scraper():
    """Test YouTube scraping functionality"""
    print("\nTesting YouTube scraper...")
    
    try:
        from scrapers.youtube_scraper import YouTubeScraper
        scraper = YouTubeScraper()
        videos = scraper.get_all_youtube_content()
        
        print(f"SUCCESS: Found {len(videos)} YouTube videos")
        if videos:
            print(f"  Sample: {videos[0]['title'][:50]}...")
        return True
        
    except Exception as e:
        print(f"ERROR: YouTube scraper error: {e}")
        return False

def test_ai_summarizer():
    """Test AI summarization functionality"""
    print("\nTesting AI summarizer...")
    
    try:
        from ai_processing.ai_summarizer import AISummarizer
        summarizer = AISummarizer()
        
        # Test with dummy content
        test_content = {
            'title': 'Test Financial News Article',
            'description': 'This is a test article about student loans and financial planning.',
            'url': 'https://example.com',
            'source': 'Test Source'
        }
        
        summary = summarizer.summarize_content(test_content)
        print(f"SUCCESS: AI summarizer working")
        print(f"  Sample summary: {summary[:100]}...")
        return True
        
    except Exception as e:
        print(f"ERROR: AI summarizer error: {e}")
        return False

def test_email_system():
    """Test email system (without actually sending)"""
    print("\nTesting email system...")
    
    try:
        from email_system.email_system import EmailSystem
        email_system = EmailSystem()
        
        # Test creating digest content
        test_content = {
            'content': [{
                'title': 'Test Article',
                'source': 'Test Source',
                'url': 'https://example.com',
                'fitbux_summary': 'This is a test summary.'
            }],
            'fitbux_perspective': 'This is a test perspective.'
        }
        
        digest = email_system.create_digest_content(test_content)
        print(f"SUCCESS: Email system working")
        print(f"  Digest length: {len(digest)} characters")
        return True
        
    except Exception as e:
        print(f"ERROR: Email system error: {e}")
        return False

def main():
    """Main test function"""
    print("FitBUX Financial News Curator - System Test")
    print("=" * 60)
    
    # Test individual components
    tests = [
        ("Environment", test_environment),
        ("News Scraper", test_news_scraper),
        ("Reddit Scraper", test_reddit_scraper),
        ("YouTube Scraper", test_youtube_scraper),
        ("AI Summarizer", test_ai_summarizer),
        ("Email System", test_email_system)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"ERROR: {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\nTest Results Summary:")
    print("-" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\nAll tests passed! System is ready to use.")
        print("You can now run: python main_agent.py")
    else:
        print("\nSome tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
