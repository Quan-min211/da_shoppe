"""
Pydantic schemas cho API responses.
"""

from pydantic import BaseModel
from typing import Optional


class ProductResponse(BaseModel):
    """Schema cho 1 sản phẩm trong danh sách."""
    product_id: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    discount: Optional[str] = None
    sold_count: Optional[str] = None
    rating_star: Optional[float] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    shop_name: Optional[str] = None
    location: Optional[str] = None
    
    # Metrics từ Gold Layer
    total_reviews: Optional[int] = 0
    avg_rating: Optional[float] = 0.0
    star_5_count: Optional[int] = 0
    star_4_count: Optional[int] = 0
    star_3_count: Optional[int] = 0
    star_2_count: Optional[int] = 0
    star_1_count: Optional[int] = 0
    star_5_percentage: Optional[float] = 0.0

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    """Schema cho response có phân trang."""
    data: list[dict]
    total: int
    page: int
    page_size: int
    total_pages: int


class AnalyticsOverview(BaseModel):
    """Schema cho tổng quan analytics."""
    total_products: int
    avg_price: float
    avg_rating: float
    total_reviews: int


class RatingDistribution(BaseModel):
    """Schema cho phân bố đánh giá."""
    star_1: int
    star_2: int
    star_3: int
    star_4: int
    star_5: int
    total: int


class HealthResponse(BaseModel):
    """Schema cho health check."""
    status: str
    total_products: int
    total_reviews: int
