"""
Cloud-ready scheduler for the FitBUX Financial News Curator Agent
"""
import os
import sys
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from scrapers.news_scraper import NewsScraper
from scrapers.reddit_scraper import RedditScraper
from scrapers.youtube_scraper import YouTubeScraper
from ai_processing.ai_summarizer import AISummarizer
from ai_processing.duplicate_tracker import DuplicateTracker
from email_system.email_system import EmailSystem

def run_news_curator():
    """Main function to run the FitBUX Financial News Curator Agent"""
    try:
        print("Starting FitBUX Financial News Curator Agent...")
        
        # Initialize all components
        print("Initializing news scraper...")
        news_scraper = NewsScraper()
        
        print("Initializing Reddit scraper...")
        reddit_scraper = RedditScraper()
        
        print("Initializing YouTube scraper...")
        youtube_scraper = YouTubeScraper()
        
        print("Initializing AI summarizer...")
        ai_summarizer = AISummarizer()
        
        print("Initializing duplicate tracker...")
        duplicate_tracker = DuplicateTracker()
        
        print("Initializing email system...")
        email_system = EmailSystem()
        
        # Fetch content from all sources
        print("\nFetching content from all sources...")
        
        # Get news articles
        print("  Fetching financial news...")
        news_articles = news_scraper.get_all_news()
        print(f"    Found {len(news_articles)} news articles")
        
        # Get Reddit posts
        print("  Fetching Reddit discussions...")
        reddit_posts = reddit_scraper.get_all_reddit_content()
        print(f"    Found {len(reddit_posts)} Reddit posts")
        
        # Get YouTube videos
        print("  Fetching YouTube videos...")
        youtube_videos = youtube_scraper.get_all_youtube_content()
        print(f"    Found {len(youtube_videos)} YouTube videos")
        
        # Combine all content
        all_content = news_articles + reddit_posts + youtube_videos
        print(f"\nTotal content collected: {len(all_content)} items")
        
        if not all_content:
            print("No content found. Skipping digest creation.")
            return False
        
        # Filter duplicates
        print("\nFiltering duplicates...")
        filtered_content = duplicate_tracker.filter_duplicates(all_content, strict_mode=False)
        print(f"  After filtering: {len(filtered_content)} unique items")
        
        if not filtered_content:
            print("No unique content after filtering. Skipping digest creation.")
            return False
        
        # Process content with AI
        print("\nProcessing content with AI...")
        processed_content = ai_summarizer.process_all_content(
            news_articles=[item for item in filtered_content if item.get('content_type') == 'news'],
            reddit_posts=[item for item in filtered_content if 'reddit' in item.get('content_type', '')],
            youtube_videos=[item for item in filtered_content if 'youtube' in item.get('content_type', '')]
        )
        
        # Send email digest
        print("\nSending email digest...")
        email_success = email_system.send_digest(processed_content)
        
        if email_success:
            print("Email digest sent successfully!")
            
            # Print summary
            current_time = datetime.now(pytz.timezone('US/Central')).strftime("%Y-%m-%d %H:%M:%S %Z")
            print(f"\nDigest Summary:")
            print(f"  Time: {current_time}")
            print(f"  Content items: {processed_content['total_items']}")
            print(f"  Email sent to: jreinkefitbux@gmail.com")
            
            return True
        else:
            print("Failed to send email digest")
            return False
            
    except Exception as e:
        print(f"Error in news curator: {e}")
        import traceback
        traceback.print_exc()
        return False

def lambda_handler(event, context):
    """
    AWS Lambda handler function for cloud deployment
    
    Args:
        event: Lambda event data
        context: Lambda context
        
    Returns:
        Response dictionary
    """
    try:
        print("Cloud scheduler triggered")
        print(f"Event: {event}")
        
        # Run the news curator
        success = run_news_curator()
        
        if success:
            return {
                'statusCode': 200,
                'body': {
                    'message': 'FitBUX News Curator completed successfully',
                    'timestamp': datetime.now().isoformat()
                }
            }
        else:
            return {
                'statusCode': 500,
                'body': {
                    'message': 'FitBUX News Curator failed',
                    'timestamp': datetime.now().isoformat()
                }
            }
            
    except Exception as e:
        print(f"Cloud scheduler error: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'message': f'Cloud scheduler error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
        }

def main():
    """Main function for local testing"""
    print("FitBUX Financial News Curator - Cloud Scheduler")
    print("=" * 60)
    
    # Run the curator
    success = run_news_curator()
    
    if success:
        print("\nFitBUX News Curator completed successfully!")
        sys.exit(0)
    else:
        print("\nFitBUX News Curator failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
