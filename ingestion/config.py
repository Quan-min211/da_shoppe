"""
Configuration module — Quản lý settings cho ingestion layer.

Load settings từ:
1. .env file (nếu có)
2. Environment variables
3. Default values

Sử dụng pydantic-settings nếu có, fallback về os.environ nếu không.
"""

import os
from pathlib import Path
from functools import lru_cache

from loguru import logger

# Try to load .env file
try:
    from dotenv import load_dotenv

    # Tìm .env file từ project root
    _project_root = Path(__file__).parent.parent
    _env_file = _project_root / ".env"
    if _env_file.exists():
        load_dotenv(_env_file)
        logger.debug(f"Loaded .env from {_env_file}")
except ImportError:
    pass


class Settings:
    """Application settings.

    Load từ environment variables với fallback defaults.
    """

    def __init__(self):
        # === Chrome CDP ===
        self.CHROME_CDP_URL: str = os.getenv("CHROME_CDP_URL", "http://127.0.0.1:9222")

        # === Scraping ===
        self.REQUEST_DELAY_SECONDS: float = float(
            os.getenv("REQUEST_DELAY_SECONDS", "2")
        )
        self.MAX_PAGES_PER_KEYWORD: int = int(
            os.getenv("MAX_PAGES_PER_KEYWORD", "5")
        )
        self.MAX_REVIEWS_PER_PRODUCT: int = int(
            os.getenv("MAX_REVIEWS_PER_PRODUCT", "100")
        )
        self.PAGE_LOAD_TIMEOUT: int = int(
            os.getenv("PAGE_LOAD_TIMEOUT", "30000")
        )

        # === Data Storage ===
        self.DATA_DIR: str = os.getenv("DATA_DIR", "./data")
        self.RAW_DATA_DIR: str = os.getenv("RAW_DATA_DIR", "./data/raw")

        # === Logging ===
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_DIR: str = os.getenv("LOG_DIR", "./logs")

    def __repr__(self) -> str:
        return (
            f"Settings("
            f"CDP={self.CHROME_CDP_URL}, "
            f"delay={self.REQUEST_DELAY_SECONDS}s, "
            f"max_pages={self.MAX_PAGES_PER_KEYWORD}, "
            f"data_dir={self.DATA_DIR}"
            f")"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance (singleton pattern)."""
    settings = Settings()
    logger.debug(f"Settings loaded: {settings}")
    return settings
