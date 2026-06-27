import requests
import logging
import os
from src.config.settings import settings

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        # Prioritize environment variables for GitHub Actions context
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", settings.TELEGRAM_BOT_TOKEN)
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", settings.TELEGRAM_CHAT_ID)
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, message: str, parse_mode: str = "Markdown") -> bool:
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram BOT_TOKEN or CHAT_ID not configured. Skipping notification.")
            return False

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode,
        }
        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False