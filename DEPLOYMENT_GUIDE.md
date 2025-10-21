# 🚀 FitBUX Financial News Curator - Deployment Guide

This guide will help you deploy your FitBUX Financial News Curator Agent to run automatically in the cloud.

## 📋 Prerequisites

Before deploying, you'll need:

1. **API Keys** (get these first):

   - OpenAI API key
   - NewsAPI key (free tier available)
   - Reddit API credentials
   - YouTube Data API key
   - Gmail App Password (for email)

2. **Cloud Account** (choose one):
   - AWS (recommended - free tier available)
   - Google Cloud Platform
   - Microsoft Azure

## 🔑 Getting Your API Keys

### 1. OpenAI API Key

- Go to https://platform.openai.com/api-keys
- Create a new secret key
- Copy and save it securely

### 2. NewsAPI Key

- Go to https://newsapi.org/register
- Sign up for free (1000 requests/day)
- Copy your API key

### 3. Reddit API Credentials

- Go to https://www.reddit.com/prefs/apps
- Click "Create App" or "Create Another App"
- Choose "script" as the app type
- Note down the client ID and secret

### 4. YouTube Data API Key

- Go to https://console.developers.google.com/
- Create a new project or select existing
- Enable YouTube Data API v3
- Create credentials (API key)
- Copy the API key

### 5. Gmail App Password

- Enable 2-factor authentication on your Gmail
- Go to Google Account settings > Security
- Generate an "App Password" for this application
- Use this password (not your regular Gmail password)

## ☁️ Option 1: AWS Lambda Deployment (Recommended)

### Step 1: Prepare Your Code

1. **Create a deployment package:**

```bash
# Install dependencies
pip install -r requirements.txt -t ./package

# Copy your Python files to the package
cp *.py ./package/
cp brand_guidelines.md ./package/

# Create a zip file
cd package
zip -r ../fitbux-news-curator.zip .
cd ..
```

### Step 2: Set Up AWS Lambda

1. **Create Lambda Function:**

   - Go to AWS Lambda console
   - Click "Create function"
   - Choose "Author from scratch"
   - Name: `fitbux-news-curator`
   - Runtime: Python 3.9
   - Click "Create function"

2. **Upload Code:**

   - Upload the `fitbux-news-curator.zip` file
   - Set handler to `main_agent.lambda_handler`

3. **Set Environment Variables:**

   - Go to Configuration > Environment variables
   - Add all your API keys and email settings

4. **Set Timeout:**
   - Go to Configuration > General configuration
   - Set timeout to 5 minutes

### Step 3: Set Up CloudWatch Events (Scheduler)

1. **Create EventBridge Rule:**
   - Go to Amazon EventBridge
   - Create rule
   - Schedule expression: `cron(0 6,9,12,15,17 * * ? *)` (weekdays)
   - Add another rule: `cron(0 18 * * ? *)` (weekends)
   - Target: Your Lambda function

## ☁️ Option 2: Google Cloud Functions

### Step 1: Set Up Google Cloud

1. **Install Google Cloud CLI:**

```bash
# Download and install from https://cloud.google.com/sdk/docs/install
```

2. **Authenticate:**

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Step 2: Deploy Function

1. **Create requirements.txt:**

```txt
requests==2.31.0
openai==1.3.0
feedparser==6.0.10
praw==7.7.1
google-api-python-client==2.108.0
python-dotenv==1.0.0
beautifulsoup4==4.12.2
lxml==4.9.3
pytz==2023.3
```

2. **Deploy:**

```bash
gcloud functions deploy fitbux-news-curator \
  --runtime python39 \
  --trigger-http \
  --entry-point main \
  --memory 512MB \
  --timeout 540s \
  --set-env-vars OPENAI_API_KEY=your_key,NEWS_API_KEY=your_key
```

### Step 3: Set Up Cloud Scheduler

1. **Create scheduled job:**

```bash
gcloud scheduler jobs create http fitbux-weekday-schedule \
  --schedule="0 6,9,12,15,17 * * 1-5" \
  --uri="https://YOUR_REGION-YOUR_PROJECT.cloudfunctions.net/fitbux-news-curator" \
  --http-method=POST
```

## 🖥️ Option 3: Local Computer (Windows Task Scheduler)

If you prefer to run locally on your computer:

### Step 1: Install Python and Dependencies

1. **Install Python 3.8+**
2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment

1. **Create .env file:**

```bash
# Copy env_example.txt to .env and fill in your keys
copy env_example.txt .env
```

2. **Edit .env file with your actual API keys**

### Step 3: Test the System

1. **Test once:**

```bash
python main_agent.py
```

2. **Test scheduler:**

```bash
python scheduler.py --test
```

### Step 4: Set Up Windows Task Scheduler

1. **Open Task Scheduler**
2. **Create Basic Task:**

   - Name: "FitBUX News Curator"
   - Trigger: Daily
   - Start: 6:00 AM
   - Action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\your\project\scheduler.py`
   - Start in: `C:\path\to\your\project`

3. **Create multiple tasks for different times**

## 🧪 Testing Your Deployment

### Test Individual Components

1. **Test news scraping:**

```python
from news_scraper import NewsScraper
scraper = NewsScraper()
articles = scraper.get_all_news()
print(f"Found {len(articles)} articles")
```

2. **Test Reddit scraping:**

```python
from reddit_scraper import RedditScraper
scraper = RedditScraper()
posts = scraper.get_all_reddit_content()
print(f"Found {len(posts)} Reddit posts")
```

3. **Test email system:**

```python
from email_system import EmailSystem
email = EmailSystem()
# Test with dummy content
```

### Test Full System

```bash
python main_agent.py
```

## 🔧 Troubleshooting

### Common Issues

1. **"No module named 'openai'"**

   - Make sure you installed all requirements
   - Check your Python path

2. **"Invalid API key"**

   - Double-check your API keys in .env file
   - Make sure there are no extra spaces

3. **"SMTP Authentication failed"**

   - Use App Password, not regular Gmail password
   - Enable 2-factor authentication first

4. **"Rate limit exceeded"**
   - You're hitting API limits
   - Check your API usage in respective dashboards

### Monitoring

1. **Check logs:**

   - AWS: CloudWatch Logs
   - Google Cloud: Cloud Functions logs
   - Local: Console output

2. **Monitor API usage:**
   - Check your API dashboards regularly
   - Set up billing alerts

## 📊 Expected Costs

### Free Tiers (per month):

- **OpenAI**: $5-10 (depending on usage)
- **NewsAPI**: Free (1000 requests/day)
- **Reddit API**: Free
- **YouTube API**: Free (10,000 units/day)
- **Gmail**: Free
- **AWS Lambda**: Free (1M requests/month)
- **Google Cloud Functions**: Free (2M invocations/month)

### Total estimated cost: $5-15/month

## 🎯 Next Steps

1. **Deploy using one of the options above**
2. **Test thoroughly**
3. **Monitor for a few days**
4. **Adjust schedule if needed**
5. **Add more sources or features**

## 📞 Support

If you run into issues:

1. Check the troubleshooting section
2. Review the logs
3. Test individual components
4. Contact support for specific APIs if needed

---

**Remember:** This system will run automatically and send you daily financial news digests. Make sure to check your email regularly to see the results!
