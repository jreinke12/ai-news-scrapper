# 🧠 FitBUX Financial News Curator Agent – Specification

**Purpose:**  
Monitor financial news several times per day, summarize the most relevant updates for 20–40-year-olds, and email the daily digest to `jreinke@fitbux.com`.

---

## 🎯 Core Objectives
1. Search and summarize relevant financial news and YouTube videos.
2. Filter results for everyday financial relevance (student loans, inflation, housing, etc.).
3. Write summaries in FitBUX’s tone (educational, conversational, calm, empowering).
4. Email the curated digest automatically.

---

## 🌐 Data Sources

### News & Finance
- Bloomberg  
- Reuters  
- CNBC Personal Finance  
- MarketWatch  
- Yahoo! Finance  
- Business Insider  
- Forbes Money  
- Kiplinger  
- Investopedia  
- NerdWallet  

### Student Loans & Experts
- [Student Loan Planner](https://www.studentloanplanner.com/)
- Student Loan Planner YouTube Channel
- Stanley Tate YouTube Channel
- Adam Minsky articles (via Google search:
  `"Adam Minsky" + "student loan" site:forbes.com OR site:studentloanhero.com OR site:studentloanplanner.com"`)

### General Trending Sources
- Google News search queries:
  - “financial news for young professionals”
  - “student loans 2025”
  - “housing market trends”
  - “credit card debt rising”
  - “inflation personal finance”
- Reddit `r/personalfinance` (top daily threads)
- YouTube Trending (finance category)

---

## 🧭 Filtering Criteria

**Include if:**
- Affects young professionals (20–40).
- Involves student loans, budgeting, investing, credit, housing, taxes.
- Offers actionable or emotional insight.

**Exclude if:**
- Corporate-only M&A, hedge fund, or insider data.
- Crypto or speculative stocks (unless widely impactful).
- Redundant coverage.

---

## 🗞️ Output Format

**Email Subject:**  
`FitBUX Financial News Digest – [Month Day, Year]`

**Email Body Example (Markdown):**

```
🗓️ Date: [Month Day, Year]
🕒 Compiled automatically at [Time, Time Zone]

---

### 🔥 Top Financial Stories for Young Professionals

**1. [Title of Article or Video]**  
Source: [Source Name] – [Link]  
**Summary:** [2–3 sentence summary in FitBUX tone explaining what it means and why it matters.]

(repeat 5–10 stories)

---

### 🧭 FitBUX Perspective
[3–5 sentences summarizing overall financial theme of the day.]
```

---

## ✍️ Tone & Voice

- Conversational, trustworthy, empathetic.  
- Use short and medium-length sentences.  
- Integrate the five senses or emotion when possible.  
- Focus on calm understanding — not fear.  
- Always highlight “what this means for you.”

---

## ⚙️ Agent Pipeline

1. **Fetch Phase:**  
   - Use `NewsAPI`, `Google Custom Search`, or RSS scraping for the above sites.  
   - Use YouTube Data API v3 for channels (Student Loan Planner, Stanley Tate).  

2. **Filter Phase:**  
   - Discard duplicates and irrelevant or overly technical articles.  

3. **Summarization Phase:**  
   - Summarize each article via OpenAI or Bedrock LLM call using this system prompt:  

   ```
   You are FitBUX’s financial news summarizer. 
   Summarize the following article in 2–3 sentences that are 
   clear, conversational, and relevant to 20–40-year-olds. 
   Focus on how it affects day-to-day finances, stress, or opportunity.
   Use FitBUX’s voice: calm, educational, and empowering.
   ```

4. **Email Phase:**  
   - Compile all summaries into a single Markdown/HTML email.  
   - Send via SMTP or AWS SES to `jreinke@fitbux.com`.

---

## 🧩 Output JSON (optional structured export)
```json
{
  "date": "2025-10-20",
  "stories": [
    {
      "title": "Student Loan Forgiveness Delayed Again",
      "source": "CNBC",
      "url": "https://www.cnbc.com/article",
      "summary": "Borrowers expecting forgiveness this month will need to wait longer..."
    }
  ],
  "fitbux_perspective": "Rates and repayment uncertainty continue to shape financial stress..."
}
```

---

## 🧠 Example System Prompt (for Cursor or LangGraph)

```
SYSTEM PROMPT:

You are FitBUX’s Financial News Curator Agent.

Task: Search, summarize, and email the most relevant financial news for young professionals (20–40 years old). 
Use FitBUX’s brand voice (Innocent/Everyman archetype): trustworthy, simple, empowering. 
Always explain “why it matters” in plain language.

Output a digest email in the specified format.
```
---

## 🧰 `financial_news_curator.py` (core implementation outline)

```python
import os
import requests
import openai
import feedparser
from datetime import datetime
from email_client import send_email

openai.api_key = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(query="personal finance OR student loans", language="en"):
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={NEWS_API_KEY}"
    r = requests.get(url)
    data = r.json()
    return data.get("articles", [])[:10]

def summarize_article(title, description, url):
    content = f"Title: {title}\n\nDescription: {description}\n\nURL: {url}"
    prompt = f"""
    You are FitBUX’s financial news summarizer.
    Summarize the following in 2–3 sentences for young professionals (20–40).
    Use FitBUX’s tone: calm, educational, conversational.
    Focus on why it matters for personal finance or student loans.\n\n{content}
    """
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=250,
        temperature=0.6
    )
    return resp["choices"][0]["message"]["content"].strip()

def create_digest(articles):
    date_str = datetime.now().strftime("%B %d, %Y")
    body = f"🗓️ Date: {date_str}\n\n### 🔥 Top Financial Stories for Young Professionals\n\n"
    for i, art in enumerate(articles, 1):
        summary = summarize_article(art['title'], art['description'], art['url'])
        body += f"**{i}. {art['title']}**\nSource: {art['source']['name']} – {art['url']}\n**Summary:** {summary}\n\n"
    body += "---\n### 🧭 FitBUX Perspective\n"
    body += summarize_article("FitBUX Perspective", "Summarize the main financial theme of the day based on the stories above.", "")
    return body

def run_curator():
    topics = ["student loans", "housing market", "inflation", "investing basics"]
    all_articles = []
    for topic in topics:
        all_articles.extend(fetch_news(topic))
    digest = create_digest(all_articles[:10])
    send_email(
        to_email="jreinke@fitbux.com",
        subject=f"FitBUX Financial News Digest – {datetime.now().strftime('%B %d, %Y')}",
        body=digest
    )

if __name__ == "__main__":
    run_curator()
```

---

## 📧 `email_client.py` (SMTP example)

```python
import os
import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        server.send_message(msg)
```

---

## 🧩 `.env` (example)

```
OPENAI_API_KEY=your_openai_key
NEWS_API_KEY=your_newsapi_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password
EMAIL_FROM=FitBUX Agent <your_email@gmail.com>
```

---

## 💡 Setup Notes
- Add `feedparser`, `requests`, `openai`, and `python-dotenv` to `requirements.txt`.
- Schedule execution via CRON, AWS Lambda, or Cursor Tasks.
- Expand later with YouTube Data API and Reddit RSS ingestion.
