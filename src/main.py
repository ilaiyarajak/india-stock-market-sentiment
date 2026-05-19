import sys
import os

# Add project root to python path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collection.orchestrator import CollectorOrchestrator
from src.sentiment.vader_scorer import VaderScorer
from src.feed_generation.deduplicator import Deduplicator
from src.feed_generation.rss_builder import RSSBuilder
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Starting Indian Stock Market Sentiment Pipeline")
    
    # 1. Data Collection
    logger.info("Phase 1: Collecting articles...")
    orchestrator = CollectorOrchestrator()
    articles = orchestrator.run_all()
    
    if not articles:
        logger.error("No articles collected. Exiting.")
        sys.exit(1)
        
    # 2. Deduplication
    logger.info("Phase 2: Deduplicating articles...")
    unique_articles = Deduplicator.deduplicate(articles)
    
    # 3. Sentiment Analysis
    logger.info("Phase 3: Analyzing sentiment...")
    scorer = VaderScorer()
    sentiments = scorer.analyze_batch(unique_articles)
    
    # 4. Feed Generation
    logger.info("Phase 4: Generating feeds...")
    builder = RSSBuilder()
    builder.build_feed(unique_articles, sentiments)
    
    logger.info("Pipeline completed successfully.")

if __name__ == "__main__":
    main()
