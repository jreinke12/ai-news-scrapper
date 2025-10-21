# 🧠 FitBUX Financial News Curator Agent

An intelligent AI agent that automatically scrapes financial news, Reddit discussions, and YouTube videos to create daily digests for your YouTube channel and podcast content.

## 🎯 What It Does

- **Scrapes** financial news from major sources (Bloomberg, Reuters, CNBC, etc.)
- **Monitors** Reddit communities (r/pslf, r/personalfinance, r/studentloans)
- **Tracks** YouTube financial channels and trending videos
- **Summarizes** content using AI with your brand voice
- **Sends** daily email digests with markdown attachments
- **Runs** automatically on your schedule (3-4 times per day)

## 📁 Project Structure

```
ai-news-scrapper/
├── 📁 scrapers/              # Data collection modules
│   ├── news_scraper.py       # Financial news scraping
│   ├── reddit_scraper.py     # Reddit post monitoring
│   └── youtube_scraper.py    # YouTube video tracking
│
├── 📁 ai_processing/         # AI and content processing
│   ├── ai_summarizer.py      # AI content summarization
│   └── duplicate_tracker.py  # Duplicate content filtering
│
├── 📁 email/                 # Email system
│   └── email_system.py       # Email digest system
│
├── 📁 config/                # Configuration files
│   ├── config.py             # Main configuration
│   ├── brand_guidelines.md   # Your brand voice guidelines
│   └── env_example.txt       # Environment variables template
│
├── 📁 docs/                  # Documentation
│   └── DEPLOYMENT_GUIDE.md   # Cloud deployment instructions
│
├── 📁 data/                  # Data storage (created automatically)
│   └── content_history.json  # Duplicate tracking data
│
├── main_agent.py             # Main entry point
├── scheduler.py              # Scheduling system
├── test_system.py            # System testing script
├── lambda_handler.py         # AWS Lambda handler
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Get Your API Keys

You'll need these API keys (all have free tiers):

- **OpenAI API Key** - for AI summarization
- **NewsAPI Key** - for news articles
- **Reddit API Credentials** - for Reddit posts
- **YouTube Data API Key** - for YouTube videos
- **Gmail App Password** - for sending emails

### 2. Set Up Environment

```bash
# Install Python dependencies
pip install -r requirements.txt

# Copy the example environment file
copy config\env_example.txt .env

# Edit .env with your actual API keys
notepad .env
```

### 3. Test the System

```bash
# Test all components
python test_system.py

# Test once manually
python main_agent.py

# Test the scheduler
python scheduler.py --test
```

### 4. Run the Scheduler

```bash
# Run continuously (for local testing)
python scheduler.py
```

## ⚙️ Configuration

### Schedule (config/config.py)

- **Weekdays**: 6:00 AM, 9:00 AM, 12:00 PM, 3:00 PM, 5:00 PM CST
- **Weekends**: 6:00 PM CST

### Content Sources

- **News**: Bloomberg, Reuters, CNBC, MarketWatch, Yahoo Finance, etc.
- **Reddit**: r/pslf, r/personalfinance, r/studentloans
- **YouTube**: Student Loan Planner, Stanley Tate channels + trending searches

### Content Filtering

- Focuses on topics relevant to 20-40 year olds
- Student loans, PSLF, inflation, housing, credit, investing
- Filters out corporate M&A, crypto speculation, redundant content

## 📧 Email Digest Format

Each digest includes:

- **Top Financial Stories** (5-10 items with FitBUX summaries)
- **FitBUX Perspective** (overall financial theme analysis)
- **Markdown attachment** for easy content creation
- **Source links** for further research

## 🎨 Brand Voice Integration

The system uses your `config/brand_guidelines.md` file to ensure all content:

- Uses FitBUX's "Innocent Everyman" voice
- Is calm, trustworthy, and educational
- Focuses on "what this means for you"
- Ends with actionable insights or next steps

## ☁️ Cloud Deployment

For automatic running (even when your computer is off), see `docs/DEPLOYMENT_GUIDE.md` for:

- **AWS Lambda** (recommended)
- **Google Cloud Functions**
- **Windows Task Scheduler** (local)

## 🔧 Troubleshooting

### Common Issues

1. **Missing API Keys**

   - Check your `.env` file
   - Make sure all required keys are set

2. **Import Errors**

   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+)

3. **Email Not Sending**

   - Use Gmail App Password (not regular password)
   - Enable 2-factor authentication first

4. **No Content Found**
   - Check API rate limits
   - Verify API keys are working

### Testing Individual Components

```python
# Test news scraping
from scrapers.news_scraper import NewsScraper
scraper = NewsScraper()
articles = scraper.get_all_news()
print(f"Found {len(articles)} articles")

# Test Reddit scraping
from scrapers.reddit_scraper import RedditScraper
scraper = RedditScraper()
posts = scraper.get_all_reddit_content()
print(f"Found {len(posts)} Reddit posts")
```

## 📊 Expected Performance

- **Content per run**: 10-20 items
- **Processing time**: 2-5 minutes
- **Email delivery**: Immediate
- **Monthly cost**: $5-15 (mostly OpenAI API)

## 🎯 Customization

### Add More Sources

Edit `config/config.py` to add:

- More news sources
- Additional Reddit subreddits
- New YouTube channels

### Adjust Schedule

Modify `SCHEDULE_CONFIG` in `config/config.py`:

```python
SCHEDULE_CONFIG = {
    "weekdays": {
        "times": ["06:00", "09:00", "12:00", "15:00", "17:00"],
        "timezone": "US/Central"
    },
    "weekends": {
        "times": ["18:00"],
        "timezone": "US/Central"
    }
}
```

### Change Content Focus

Update `SEARCH_QUERIES` in `config/config.py`:

```python
SEARCH_QUERIES = [
    "your custom search terms here",
    "more specific topics",
    "additional keywords"
]
```

## 📞 Support

If you need help:

1. Check the troubleshooting section
2. Review the deployment guide in `docs/`
3. Test individual components
4. Check API dashboards for rate limits

---

**Ready to automate your financial content research?** Follow the quick start guide above and you'll have your first digest within minutes!
