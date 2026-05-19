# 📈 Indian Stock Market Sentiment MVP

An automated system that collects market news, analyzes sentiment using VADER, and publishes an RSS feed.

## 🚀 Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Create `.env` based on `.env.example` to use Reddit collection:
   ```
   REDDIT_CLIENT_ID=your_id
   REDDIT_CLIENT_SECRET=your_secret
   ```

3. Run the pipeline:
   ```bash
   python src/main.py
   ```

4. Check `data/feeds/sentiment_rss.xml` for the output.

## 📡 RSS Feed
The output is a valid RSS 2.0 feed containing the latest stock market news categorized as **Bullish**, **Bearish**, or **Neutral**.
