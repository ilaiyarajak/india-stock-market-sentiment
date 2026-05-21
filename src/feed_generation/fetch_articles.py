import feedparser
from src.models.article import Article

def fetch_articles_from_rss(feed_urls):
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            articles.append(
                Article(
                    id=entry.get('id', entry.link),
                    title=entry.title,
                    link=entry.link,
                    published=entry.get('published', ''),
                    source=url,  # Or extract a better source name
                    # ...other fields as needed...
                )
            )
    return articles
