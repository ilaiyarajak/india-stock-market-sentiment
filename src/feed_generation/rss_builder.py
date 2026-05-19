import os
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
        fg.description('Automated sentiment analysis of Indian stock market news and Reddit discussions.')
        fg.language('en')
        fg.pubDate(datetime.now(timezone.utc))

        for article in articles:
            sentiment = sentiments.get(article.id)
            if not sentiment:
                continue

            fe = fg.add_entry()
            fe.id(article.url)
            fe.title(f"[{sentiment.category}] {article.title}")
            fe.link(href=article.url)
            fe.description(f"Source: {article.source} | Score: {sentiment.score:.2f}/100<br/><br/>{article.content[:500]}...")
            try:
                fe.pubDate(article.published_at.replace(tzinfo=timezone.utc))
            except Exception:
                fe.pubDate(datetime.now(timezone.utc))

        output_path = os.path.join(self.output_dir, filename)
        fg.rss_file(output_path)
        logger.info(f"Successfully generated RSS feed at {output_path} with {len(articles)} items.")
