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
        now = datetime.now(timezone.utc)
        fg.pubDate(now)

        valid_sentiments = [sentiments[a.id] for a in articles if a.id in sentiments]
        
        if valid_sentiments:
            avg_score = sum(s.score for s in valid_sentiments) / len(valid_sentiments)
            
            if avg_score >= 60:
                agg_category = "Bullish"
            elif avg_score <= 40:
                agg_category = "Bearish"
            else:
                agg_category = "Neutral"

            fe = fg.add_entry()
            fe.id(f"aggregate-{now.strftime('%Y%m%d%H%M%S')}")
            fe.title(f"Market Sentiment: {agg_category} ({avg_score:.2f}/100)")
            fe.link(href='https://github.com/ilaiya/india-stock-market-sentiment')
            
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
            
            fe.description("".join(description_lines))
            fe.pubDate(now)

        output_path = os.path.join(self.output_dir, filename)
        fg.rss_file(output_path)
        logger.info(f"Successfully generated aggregated RSS feed at {output_path}.")
