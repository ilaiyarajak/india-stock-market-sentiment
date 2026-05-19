from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Article:
    id: str
    title: str
    content: str
    url: str
    source: str
    published_at: datetime
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
