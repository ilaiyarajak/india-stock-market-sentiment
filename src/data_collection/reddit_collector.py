import praw
from typing import List
from datetime import datetime
from src.models.article import Article
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class RedditCollector:
    def __init__(self):
        if not settings.REDDIT_CLIENT_ID or not settings.REDDIT_CLIENT_SECRET:
            logger.warning("Reddit credentials missing. Collector will return empty results.")
            self.reddit = None
        else:
            self.reddit = praw.Reddit(
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                user_agent=settings.REDDIT_USER_AGENT
            )
        self.subreddits = ["Indian_stock_market", "NSEIndia", "IndianStocks", "DalalStreetTalks"]

    def collect(self) -> List[Article]:
        if not self.reddit:
            return []
        
        articles = []
        for sub_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(sub_name)
                for post in subreddit.hot(limit=25):
                    articles.append(Article(
                        id=f"reddit_{post.id}",
                        title=post.title,
                        content=post.selftext,
                        url=f"https://reddit.com{post.permalink}",
                        source="Reddit",
                        author=post.author.name if post.author else "Unknown",
                        published_at=datetime.fromtimestamp(post.created_utc)
                    ))
            except Exception as e:
                logger.error(f"Error collecting from r/{sub_name}: {e}")
        return articles
