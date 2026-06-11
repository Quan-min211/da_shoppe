"""
Pydantic schemas cho dữ liệu đánh giá (reviews) từ Shopee.

Chuẩn bị sẵn cho NLP Sentiment Analysis ở Phase 2.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ReviewSchema(BaseModel):
    """Schema cho 1 review từ Shopee.

    Fields mapping từ Shopee API `get_ratings`:
        - cmtid → review_id
        - itemid → product_id
        - shopid → shop_id
        - rating_star → rating
        - comment → review_text
        - author_username → author_username
        - ctime → created_at (unix timestamp)
    """

    # === IDs ===
    review_id: int = Field(..., description="Shopee comment ID")
    product_id: int = Field(..., description="Shopee item ID")
    shop_id: int = Field(..., description="Shopee shop ID")

    # === Review Content ===
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5 sao)")
    review_text: Optional[str] = Field(default=None, description="Nội dung đánh giá")

    # === Author ===
    author_username: Optional[str] = Field(default=None, description="Username người đánh giá")
    author_portrait: Optional[str] = Field(default=None, description="Avatar URL")

    # === Media ===
    images: list[str] = Field(default_factory=list, description="URLs hình ảnh đính kèm")
    videos: list[str] = Field(default_factory=list, description="URLs video đính kèm")

    # === Engagement ===
    like_count: int = Field(default=0, ge=0, description="Số lượt thích review")

    # === Timestamps ===
    created_at: Optional[datetime] = Field(default=None, description="Thời điểm tạo review")

    # === Metadata ===
    platform: str = Field(default="shopee", description="Nền tảng nguồn")
    scraped_at: datetime = Field(
        default_factory=datetime.now, description="Thời điểm thu thập"
    )

    # === NLP (sẽ fill ở Silver layer) ===
    sentiment_score: Optional[float] = Field(
        default=None, ge=-1, le=1, description="Sentiment score (-1 tới 1)"
    )
    sentiment_label: Optional[str] = Field(
        default=None, description="positive / negative / neutral"
    )

    @field_validator("created_at", mode="before")
    @classmethod
    def parse_unix_timestamp(cls, v):
        """Chuyển unix timestamp → datetime."""
        if isinstance(v, (int, float)) and v > 0:
            return datetime.fromtimestamp(v)
        return v

    @classmethod
    def from_shopee_rating(cls, rating: dict, product_id: int, shop_id: int) -> "ReviewSchema":
        """Factory method: parse từ Shopee ratings API response.

        Args:
            rating: dict từ Shopee API ratings response
            product_id: item ID
            shop_id: shop ID

        Returns:
            ReviewSchema instance đã validate
        """
        # Build image URLs
        images = []
        for img in rating.get("images", []):
            if isinstance(img, str):
                images.append(f"https://cf.shopee.vn/file/{img}")

        # Build video URLs
        videos = []
        for vid in rating.get("videos", []):
            if isinstance(vid, dict):
                url = vid.get("url", "")
                if url:
                    videos.append(url)

        return cls(
            review_id=rating.get("cmtid", 0),
            product_id=product_id,
            shop_id=shop_id,
            rating=rating.get("rating_star", 5),
            review_text=rating.get("comment", ""),
            author_username=rating.get("author_username", ""),
            author_portrait=rating.get("author_portrait", ""),
            images=images,
            videos=videos,
            like_count=rating.get("like_count", 0),
            created_at=rating.get("ctime"),
        )
