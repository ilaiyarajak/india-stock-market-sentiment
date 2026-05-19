from dataclasses import dataclass
from typing import List
from .article import Article

@dataclass
class Feed:
    title: str
    description: str
    link: str
    items: List[Article]
