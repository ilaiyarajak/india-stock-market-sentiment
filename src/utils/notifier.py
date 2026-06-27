import os
import logging
from src.config.settings import settings
from src.utils.telegram_notifier import TelegramNotifier

logger = logging.getLogger(__name__)

def send_telegram_notification(message: str, parse_mode: str = "Markdown"):
    # Ensure settings are loaded from environment variables for the workflow run
    settings.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", settings.TELEGRAM_BOT_TOKEN)
    settings.TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", settings.TELEGRAM_CHAT_ID)

    notifier = TelegramNotifier()
    if notifier.send_message(message, parse_mode):
        logger.info("Telegram notification sent successfully.")
    else:
        logger.error("Failed to send Telegram notification.")