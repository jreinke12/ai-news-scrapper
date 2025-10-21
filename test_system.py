"""
Test script for the FitBUX Financial News Curator Agent
"""
import os
import sys
from datetime import datetime

def test_environment():
    """Test if all required environment variables are set"""
    print("🔍 Testing environment variables...")
    
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
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    else:
        print("✅ All environment variables are set")
        return True

def test_news_scraper():
    """Test news scraping functionality"""
    print("\n📰 Testing news scraper...")
    
    try:
        from scrapers.news_scraper import NewsScraper
        scraper = NewsScraper()
        articles = scraper.get_all_news()
        
        print(f"✅ Found {len(articles)} news articles")
        if articles:
            print(f"  Sample: {articles[0]['title'][:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ News scraper error: {e}")
        return False

def test_reddit_scraper():
    """Test Reddit scraping functionality"""
    print("\n💬 Testing Reddit scraper...")
    
    try:
        from scrapers.reddit_scraper import RedditScraper
        scraper = RedditScraper()
        posts = scraper.get_all_reddit_content()
        
        print(f"✅ Found {len(posts)} Reddit posts")
        if posts:
            print(f"  Sample: {posts[0]['title'][:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Reddit scraper error: {e}")
        return False

def test_youtube_scraper():
    """Test YouTube scraping functionality"""
    print("\n📺 Testing YouTube scraper...")
    
    try:
        from scrapers.youtube_scraper import YouTubeScraper
        scraper = YouTubeScraper()
        videos = scraper.get_all_youtube_content()
        
        print(f"✅ Found {len(videos)} YouTube videos")
        if videos:
            print(f"  Sample: {videos[0]['title'][:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ YouTube scraper error: {e}")
        return False

def test_ai_summarizer():
    """Test AI summarization functionality"""
    print("\n🤖 Testing AI summarizer...")
    
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
        print(f"✅ AI summarizer working")
        print(f"  Sample summary: {summary[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ AI summarizer error: {e}")
        return False

def test_email_system():
    """Test email system (without actually sending)"""
    print("\n📧 Testing email system...")
    
    try:
        from email.email_system import EmailSystem
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
        print(f"✅ Email system working")
        print(f"  Digest length: {len(digest)} characters")
        return True
        
    except Exception as e:
        print(f"❌ Email system error: {e}")
        return False

def test_duplicate_tracker():
    """Test duplicate tracking functionality"""
    print("\n🔍 Testing duplicate tracker...")
    
    try:
        from ai_processing.duplicate_tracker import DuplicateTracker
        tracker = DuplicateTracker()
        
        # Test with dummy content
        test_content = [{
            'title': 'Test Article 1',
            'url': 'https://example.com/1',
            'source': 'Test Source'
        }, {
            'title': 'Test Article 2', 
            'url': 'https://example.com/2',
            'source': 'Test Source'
        }]
        
        filtered = tracker.filter_duplicates(test_content)
        print(f"✅ Duplicate tracker working")
        print(f"  Filtered {len(test_content)} items to {len(filtered)} unique items")
        return True
        
    except Exception as e:
        print(f"❌ Duplicate tracker error: {e}")
        return False

def run_full_test():
    """Run a full test of the system"""
    print("\n🧪 Running full system test...")
    
    try:
        from main_agent import run_news_curator
        success = run_news_curator()
        
        if success:
            print("✅ Full system test passed!")
            return True
        else:
            print("❌ Full system test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Full system test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 FitBUX Financial News Curator - System Test")
    print("=" * 60)
    
    # Test individual components
    tests = [
        ("Environment", test_environment),
        ("News Scraper", test_news_scraper),
        ("Reddit Scraper", test_reddit_scraper),
        ("YouTube Scraper", test_youtube_scraper),
        ("AI Summarizer", test_ai_summarizer),
        ("Email System", test_email_system),
        ("Duplicate Tracker", test_duplicate_tracker)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n📊 Test Results Summary:")
    print("-" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    # Ask if user wants to run full test
    if passed == len(results):
        print("\n🎉 All individual tests passed!")
        
        response = input("\nWould you like to run a full system test? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print("\n🚀 Running full system test...")
            full_test_result = run_full_test()
            
            if full_test_result:
                print("\n🎉 System is ready to use!")
                print("You can now run: python scheduler.py")
            else:
                print("\n💥 Full system test failed. Check the errors above.")
        else:
            print("\n✅ Individual tests passed. System should work correctly.")
    else:
        print("\n💥 Some tests failed. Please fix the issues before running the full system.")
        print("\nCommon fixes:")
        print("- Check your .env file has all required API keys")
        print("- Run: pip install -r requirements.txt")
        print("- Check your internet connection")

if __name__ == "__main__":
    main()
