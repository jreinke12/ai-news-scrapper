"""
Configuration settings for the FitBUX Financial News Curator Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "FitBUX News Curator 1.0")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Email Configuration
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM", "FitBUX Agent <noreply@fitbux.com>")
EMAIL_TO = "jreinke@fitbux.com"

# News Sources
NEWS_SOURCES = [
    "bloomberg.com",
    "reuters.com", 
    "cnbc.com",
    "marketwatch.com",
    "finance.yahoo.com",
    "businessinsider.com",
    "forbes.com",
    "kiplinger.com",
    "investopedia.com",
    "nerdwallet.com"
]

# Reddit Subreddits to Monitor
REDDIT_SUBREDDITS = [
    "pslf",
    "personalfinance", 
    "studentloans"
]

# YouTube Channels to Monitor
YOUTUBE_CHANNELS = [
    "UCStudentLoanPlanner",  # Student Loan Planner
    "UCStanleyTate"  # Stanley Tate (you'll need to get the actual channel IDs)
]

# Search Queries for News
SEARCH_QUERIES = [
    "financial news for young professionals",
    "student loans 2025",
    "housing market trends",
    "credit card debt rising", 
    "inflation personal finance",
    "PSLF student loan forgiveness",
    "income driven repayment",
    "student loan consolidation"
]

# Scheduling Configuration
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

# Content Filtering
MAX_ARTICLES_PER_RUN = 10
MAX_REDDIT_POSTS = 5
MAX_YOUTUBE_VIDEOS = 3

# Duplicate Detection (in days)
DUPLICATE_CHECK_DAYS = 3
