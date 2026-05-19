import requests
import time
from src.utils.logger import get_logger

logger = get_logger(__name__)

class HTTPClient:
    @staticmethod
    def get(url: str, retries=3, backoff_factor=1.0, **kwargs):
        for i in range(retries):
            try:
                response = requests.get(url, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if i == retries - 1:
                    logger.error(f"HTTP request failed after {retries} retries: {e}")
                    raise
                sleep_time = backoff_factor * (2 ** i)
                logger.warning(f"HTTP request failed: {e}. Retrying in {sleep_time}s...")
                time.sleep(sleep_time)
