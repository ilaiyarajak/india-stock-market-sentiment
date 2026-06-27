import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists.
# This is useful for local development, but GitHub Actions will provide secrets directly.
load_dotenv()

class AppSettings:
    """
    Application settings loaded from environment variables.
    Provides default values if environment variables are not set.
    """
    # Telegram settings
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # Reddit settings (example, based on previous context)
    REDDIT_CLIENT_ID: str = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CLIENT_SECRET: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT", "python:in.stock.sentiment.githubactions:v1.0")

    # Add other application-specific settings here

# Instantiate the settings object to make it importable as 'settings'
settings = AppSettings()