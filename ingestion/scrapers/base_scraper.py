"""
Abstract base class cho tất cả scrapers.

Định nghĩa interface chung để dễ mở rộng thêm platform khác
(Tiki, Lazada, ...) trong tương lai.
"""

from abc import ABC, abstractmethod
from typing import Any

from loguru import logger


class BaseScraper(ABC):
    """Abstract base scraper — interface chung cho mọi platform."""

    def __init__(self, platform: str):
        self.platform = platform
        self.logger = logger.bind(platform=platform)

    @abstractmethod
    def connect(self) -> None:
        """Kết nối tới browser / API source."""
        ...

    @abstractmethod
    def scrape_products(self, keyword: str, max_pages: int = 1) -> list[dict[str, Any]]:
        """Thu thập danh sách sản phẩm theo keyword.

        Args:
            keyword: Từ khóa tìm kiếm
            max_pages: Số trang tối đa

        Returns:
            List of raw product dicts
        """
        ...

    @abstractmethod
    def scrape_reviews(self, shop_id: int, item_id: int, max_reviews: int = 100) -> list[dict[str, Any]]:
        """Thu thập danh sách đánh giá của một sản phẩm.

        Args:
            shop_id: ID của shop
            item_id: ID của sản phẩm
            max_reviews: Số lượng đánh giá tối đa muốn thu thập

        Returns:
            List of raw review dicts
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """Đóng kết nối, giải phóng resources."""
        ...

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
