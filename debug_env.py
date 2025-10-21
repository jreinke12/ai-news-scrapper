"""
Debug environment variable loading
"""
import os
from dotenv import load_dotenv

print("Current directory:", os.getcwd())
print("Files in current directory:", os.listdir('.'))

# Try loading .env file
load_dotenv()

print("\nEnvironment variables:")
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("NEWS_API_KEY:", os.getenv("NEWS_API_KEY"))
print("REDDIT_CLIENT_ID:", os.getenv("REDDIT_CLIENT_ID"))
print("YOUTUBE_API_KEY:", os.getenv("YOUTUBE_API_KEY"))
print("EMAIL_USER:", os.getenv("EMAIL_USER"))
