import hashlib
from typing import List
from src.models.article import Article
from src.utils.logger import get_logger

logger = get_logger(__name__)

class Deduplicator:
    @staticmethod
    def deduplicate(articles: List[Article]) -> List[Article]:
        seen_hashes = set()
        unique_articles = []
        
        for article in articles:
            content_hash = hashlib.md5(f"{article.title.lower()}_{article.source}".encode('utf-8')).hexdigest()
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_articles.append(article)
                
        logger.info(f"Deduplicated {len(articles)} articles down to {len(unique_articles)}.")
        return unique_articles
