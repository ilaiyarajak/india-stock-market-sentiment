from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.models.article import Article
from src.models.sentiment import Sentiment
from typing import Dict, List

class VaderScorer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        market_lexicon = {
            "bullish": 2.0, "bearish": -2.0, "rally": 1.5, "crash": -2.5,
            "surge": 1.5, "dive": -1.5, "correction": -1.0, "breakout": 1.5,
            "nifty": 0.0, "sensex": 0.0, "nse": 0.0, "bse": 0.0
        }
        self.analyzer.lexicon.update(market_lexicon)

    def analyze(self, article: Article) -> Sentiment:
        text = f"{article.title} {article.content}"
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        
        scaled_score = (compound + 1) * 50
        
        if scaled_score >= 60:
            category = "Bullish"
        elif scaled_score <= 40:
            category = "Bearish"
        else:
            category = "Neutral"
            
        return Sentiment(
            article_id=article.id,
            score=scaled_score,
            category=category
        )
        
    def analyze_batch(self, articles: List[Article]) -> Dict[str, Sentiment]:
        return {article.id: self.analyze(article) for article in articles}
