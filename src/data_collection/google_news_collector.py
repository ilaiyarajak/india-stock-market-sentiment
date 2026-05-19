import feedparser
from typing import List
from datetime import datetime
import time
from src.models.article import Article
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GoogleNewsCollector:
    def __init__(self):
        self.feed_url = "https://news.google.com/rss/search?q=Indian+Stock+Market+OR+NSE+OR+BSE+OR+Nifty+OR+Sensex&hl=en-IN&gl=IN&ceid=IN:en"

    def collect(self) -> List[Article]:
        articles = []
        try:
            feed = feedparser.parse(self.feed_url)
            for entry in feed.entries[:50]:
                try:
                    pub_date = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                except:
                    pub_date = datetime.now()
                
                articles.append(Article(
                    id=f"gnews_{entry.id if hasattr(entry, 'id') else hash(entry.link)}",
                    title=entry.title,
                    content=entry.summary if hasattr(entry, 'summary') else "",
                    url=entry.link,
                    source="Google News",
                    author=entry.source.title if hasattr(entry, 'source') else "Unknown",
                    published_at=pub_date
                ))
        except Exception as e:
            logger.error(f"Error collecting from Google News: {e}")
        return articles
