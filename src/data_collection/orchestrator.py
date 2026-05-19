from typing import List
from src.models.article import Article
from src.data_collection.reddit_collector import RedditCollector
from src.data_collection.google_news_collector import GoogleNewsCollector
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CollectorOrchestrator:
    def __init__(self):
        self.collectors = [
            RedditCollector(),
            GoogleNewsCollector()
        ]

    def run_all(self) -> List[Article]:
        all_articles = []
        for collector in self.collectors:
            logger.info(f"Running collector: {collector.__class__.__name__}")
            articles = collector.collect()
            logger.info(f"Collected {len(articles)} articles from {collector.__class__.__name__}")
            all_articles.extend(articles)
        return all_articles
