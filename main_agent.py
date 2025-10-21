"""
Main FitBUX Financial News Curator Agent
"""
import os
import sys
from datetime import datetime
import pytz

# Import our modules
from scrapers.news_scraper import NewsScraper
from scrapers.reddit_scraper import RedditScraper
from scrapers.youtube_scraper import YouTubeScraper
from ai_processing.ai_summarizer import AISummarizer
from ai_processing.duplicate_tracker import DuplicateTracker
from email_system.email_system import EmailSystem
from config.config import *

def run_news_curator() -> bool:
    """
    Main function to run the FitBUX Financial News Curator Agent
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print("🧠 Starting FitBUX Financial News Curator Agent...")
        
        # Initialize all components
        print("📰 Initializing news scraper...")
        news_scraper = NewsScraper()
        
        print("💬 Initializing Reddit scraper...")
        reddit_scraper = RedditScraper()
        
        print("📺 Initializing YouTube scraper...")
        youtube_scraper = YouTubeScraper()
        
        print("🤖 Initializing AI summarizer...")
        ai_summarizer = AISummarizer()
        
        print("🔍 Initializing duplicate tracker...")
        duplicate_tracker = DuplicateTracker()
        
        print("📧 Initializing email system...")
        email_system = EmailSystem()
        
        # Fetch content from all sources
        print("\n📊 Fetching content from all sources...")
        
        # Get news articles
        print("  📰 Fetching financial news...")
        news_articles = news_scraper.get_all_news()
        print(f"    Found {len(news_articles)} news articles")
        
        # Get Reddit posts
        print("  💬 Fetching Reddit discussions...")
        reddit_posts = reddit_scraper.get_all_reddit_content()
        print(f"    Found {len(reddit_posts)} Reddit posts")
        
        # Get YouTube videos
        print("  📺 Fetching YouTube videos...")
        youtube_videos = youtube_scraper.get_all_youtube_content()
        print(f"    Found {len(youtube_videos)} YouTube videos")
        
        # Combine all content
        all_content = news_articles + reddit_posts + youtube_videos
        print(f"\n📈 Total content collected: {len(all_content)} items")
        
        if not all_content:
            print("⚠️ No content found. Skipping digest creation.")
            return False
        
        # Filter duplicates
        print("\n🔍 Filtering duplicates...")
        filtered_content = duplicate_tracker.filter_duplicates(all_content, strict_mode=False)
        print(f"  After filtering: {len(filtered_content)} unique items")
        
        if not filtered_content:
            print("⚠️ No unique content after filtering. Skipping digest creation.")
            return False
        
        # Process content with AI
        print("\n🤖 Processing content with AI...")
        processed_content = ai_summarizer.process_all_content(
            news_articles=[item for item in filtered_content if item.get('content_type') == 'news'],
            reddit_posts=[item for item in filtered_content if 'reddit' in item.get('content_type', '')],
            youtube_videos=[item for item in filtered_content if 'youtube' in item.get('content_type', '')]
        )
        
        # Send email digest
        print("\n📧 Sending email digest...")
        email_success = email_system.send_digest(processed_content)
        
        if email_success:
            print("✅ Email digest sent successfully!")
            
            # Print summary
            current_time = datetime.now(pytz.timezone('US/Central')).strftime("%Y-%m-%d %H:%M:%S %Z")
            print(f"\n📊 Digest Summary:")
            print(f"  Time: {current_time}")
            print(f"  Content items: {processed_content['total_items']}")
            print(f"  Email sent to: {config.EMAIL_TO}")
            
            return True
        else:
            print("❌ Failed to send email digest")
            return False
            
    except Exception as e:
        print(f"❌ Error in news curator: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_environment():
    """Check if all required environment variables are set"""
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
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these in your .env file or environment")
        return False
    
    return True

def main():
    """Main entry point"""
    print("🎯 FitBUX Financial News Curator Agent")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run the curator
    success = run_news_curator()
    
    if success:
        print("\n🎉 FitBUX News Curator completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 FitBUX News Curator failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
