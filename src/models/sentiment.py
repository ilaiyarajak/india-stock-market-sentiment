from dataclasses import dataclass

@dataclass
class Sentiment:
    article_id: str
    score: float
    category: str
