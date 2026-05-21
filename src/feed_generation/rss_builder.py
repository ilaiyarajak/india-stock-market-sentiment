import os
import json
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
from typing import List, Dict
from src.models.article import Article
from src.models.sentiment import Sentiment
from src.utils.logger import get_logger

from src.feed_generation.fetch_articles import fetch_articles_from_rss

logger = get_logger(__name__)

class RSSBuilder:
    def __init__(self, output_dir: str = "data/feeds"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def build_feed(self, articles: List[Article], sentiments: Dict[str, Sentiment], filename: str = "sentiment_rss.xml"):
        fg = FeedGenerator()
        fg.title('Indian Stock Market Sentiment')
        fg.link(href='https://github.com/ilaiya/india-stock-market-sentiment', rel='alternate')
        fg.link(href='https://ilaiya.github.io/india-stock-market-sentiment/data/feeds/sentiment_rss.xml', rel='self')
        fg.description('Automated sentiment analysis of Indian stock market news and Reddit discussions.')
        fg.language('en')
        now = datetime.now(timezone.utc)
        fg.pubDate(now)

        history_path = os.path.join(self.output_dir, "history.json")
        html_dir = os.path.abspath(os.path.join(self.output_dir, "entries"))
        try:
            os.makedirs(html_dir, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create entries directory at {html_dir}: {e}")

        history = []
        if os.path.exists(history_path):
            try:
                with open(history_path, 'r') as f:
                    history = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load history: {e}")
                history = []

        valid_sentiments = [sentiments[a.id] for a in articles if a.id in sentiments]
        # ... rest of the class ...

# Place the main block at the end so RSSBuilder is defined
if __name__ == "__main__":
    # Example feed URLs (add or modify as needed)
    feed_urls = [
        "https://news.google.com/rss/search?q=indian+stock+market",
        "https://www.oilprice.com/rss/main",
        "https://www.geopoliticalmonitor.com/feed/",
        # Add more feeds as needed
    ]

    # Fetch articles from all feeds
    articles = fetch_articles_from_rss(feed_urls)

    # Dummy sentiment analysis (replace with your real sentiment logic)
    from src.models.sentiment import Sentiment
    sentiments = {a.id: Sentiment(score=50) for a in articles}  # Replace with real scoring

    # Build the RSS feed
    builder = RSSBuilder(output_dir="data/feeds")
    builder.build_feed(articles, sentiments)
import os
import json
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
from typing import List, Dict
from src.models.article import Article
from src.models.sentiment import Sentiment
from src.utils.logger import get_logger

logger = get_logger(__name__)

class RSSBuilder:
    def __init__(self, output_dir: str = "data/feeds"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def build_feed(self, articles: List[Article], sentiments: Dict[str, Sentiment], filename: str = "sentiment_rss.xml"):
        fg = FeedGenerator()
        fg.title('Indian Stock Market Sentiment')
        fg.link(href='https://github.com/ilaiya/india-stock-market-sentiment', rel='alternate')
        fg.link(href='https://ilaiya.github.io/india-stock-market-sentiment/data/feeds/sentiment_rss.xml', rel='self')
        fg.description('Automated sentiment analysis of Indian stock market news and Reddit discussions.')
        fg.language('en')
        now = datetime.now(timezone.utc)
        fg.pubDate(now)

        history_path = os.path.join(self.output_dir, "history.json")
        html_dir = os.path.abspath(os.path.join(self.output_dir, "entries"))
        try:
            os.makedirs(html_dir, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create entries directory at {html_dir}: {e}")

        history = []
        if os.path.exists(history_path):
            try:
                with open(history_path, 'r') as f:
                    history = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load history: {e}")
                history = []

        valid_sentiments = [sentiments[a.id] for a in articles if a.id in sentiments]
        
        if valid_sentiments:
            avg_score = sum(s.score for s in valid_sentiments) / len(valid_sentiments)
            
            if avg_score >= 60:
                agg_category = "Bullish"
            elif avg_score <= 40:
                agg_category = "Bearish"
            else:
                agg_category = "Neutral"

            description_lines = [
                f"Overall Market Sentiment based on {len(valid_sentiments)} sources.<br/>",
                f"Aggregated Score: {avg_score:.2f}/100<br/>",
                f"Category: {agg_category}<br/>",
                "<br/><h3>Source Breakdown:</h3><ul>"
            ]
            
            source_counts = {}
            for article in articles:
                if article.id in sentiments:
                    source_counts[article.source] = source_counts.get(article.source, 0) + 1
            for src, count in source_counts.items():
                description_lines.append(f"<li>{src}: {count} articles</li>")
            description_lines.append("</ul>")
            
            pubdate_prefix = now.strftime('%Y-%m-%d %H:%M UTC')
            plain_desc = f"Overall Market Sentiment based on {len(valid_sentiments)} sources. Aggregated Score: {avg_score:.2f}/100. Category: {agg_category}. Source Breakdown: " + ", ".join([f"{src}: {count} articles" for src, count in source_counts.items()])
            
            entry_id = f"aggregate-{now.strftime('%Y%m%d%H%M%S')}"
            html_filename = f"{entry_id}.html"
            html_path = os.path.join(html_dir, html_filename)
            html_rel_link = f"entries/{html_filename}"

            # Write HTML file for this entry
            try:
                with open(html_path, "w") as html_file:
                    html_file.write(f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>Market Sentiment: {agg_category} ({avg_score:.2f}/100)</title>
</head>
<body>
    <h2>Market Sentiment: {agg_category} ({avg_score:.2f}/100)</h2>
    <div>
        {''.join(description_lines)}
    </div>
</body>
</html>
""")
                logger.info(f"Wrote HTML entry file: {html_path}")
            except Exception as e:
                logger.error(f"Failed to write HTML entry file at {html_path}: {e}")

            new_entry = {
                "id": entry_id,
                "title": f"Market Sentiment: {agg_category} ({avg_score:.2f}/100)",
                "link": html_rel_link,
                "description": plain_desc,
                "content": "".join(description_lines),
                "pubDate": now.isoformat()
            }
            history.append(new_entry)

        # Keep only the last 30 entries
        history = history[-30:]

        # Save history back to disk
        try:
            with open(history_path, 'w') as f:
                json.dump(history, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")

        # Add items to feed generator (newest first for standard RSS display, or oldest first if preferred;
        # feedgen typically adds them as they come, so let's reverse to put newest at the top)
        for item in reversed(history):
            fe = fg.add_entry()
            fe.id(item["id"])
            fe.title(item["title"])
            # Use the relative HTML link for each entry
            fe.link(href=item["link"])
            
            if "content" in item:
                fe.description(item["description"])
                fe.content(item["content"], type="CDATA")
            else:
                fe.description(item["description"])
                fe.content(item["description"], type="CDATA")
            
            try:
                item_date = datetime.fromisoformat(item["pubDate"])
                fe.pubDate(item_date)
            except ValueError:
                fe.pubDate(now)

        output_path = os.path.join(self.output_dir, filename)
        fg.rss_file(output_path)
        logger.info(f"Successfully generated aggregated RSS feed at {output_path} with {len(history)} items.")
