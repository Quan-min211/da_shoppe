"""
Pydantic schemas cho dữ liệu sản phẩm Shopee.

Validate và chuẩn hóa data trước khi lưu vào pipeline.
Mapping trực tiếp từ Shopee API response → schema fields.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, computed_field


class ProductSchema(BaseModel):
    """Schema cho 1 sản phẩm từ Shopee.

    Fields mapping từ Shopee API `item_basic`:
        - itemid → product_id
        - shopid → shop_id
        - name → name
        - price / 100000 → price
        - price_before_discount / 100000 → original_price
        - catid → category_id
        - shop_location → shop_location
        - item_rating.rating_star → rating
        - cmt_count → review_count
        - historical_sold → sold_count
        - image → image_id (dùng để build URL)
    """

    # === IDs ===
    product_id: int = Field(..., description="Shopee item ID")
    shop_id: int = Field(..., description="Shopee shop ID")

    # === Product Info ===
    name: str = Field(..., min_length=1, max_length=1000, description="Tên sản phẩm")
    price: float = Field(..., gt=0, description="Giá hiện tại (VNĐ, đã chia 100000)")
    original_price: Optional[float] = Field(
        default=None, ge=0, description="Giá gốc trước giảm (VNĐ)"
    )
    currency: str = Field(default="VND", description="Đơn vị tiền tệ")

    # === Category ===
    category_id: Optional[int] = Field(default=None, description="Shopee category ID")
    category_name: Optional[str] = Field(default=None, description="Tên danh mục")

    # === Seller ===
    shop_location: Optional[str] = Field(default=None, description="Vị trí shop")

    # === Metrics ===
    rating: Optional[float] = Field(default=None, ge=0, le=5, description="Rating trung bình (0-5)")
    review_count: int = Field(default=0, ge=0, description="Số lượng đánh giá")
    sold_count: int = Field(default=0, ge=0, description="Tổng số đã bán (historical)")
    liked_count: int = Field(default=0, ge=0, description="Số lượt thích")
    stock: int = Field(default=0, ge=0, description="Số lượng tồn kho")

    # === Media ===
    image_url: Optional[str] = Field(default=None, description="URL hình ảnh chính")

    # === URLs ===
    url: Optional[str] = Field(default=None, description="URL sản phẩm trên Shopee")

    # === Metadata ===
    platform: str = Field(default="shopee", description="Nền tảng nguồn")
    scraped_at: datetime = Field(
        default_factory=datetime.now, description="Thời điểm thu thập"
    )
    keyword: Optional[str] = Field(default=None, description="Keyword tìm kiếm")

    @field_validator("price", "original_price", mode="before")
    @classmethod
    def convert_shopee_price(cls, v):
        """Shopee API trả giá nhân 100000, cần chia lại."""
        if v is not None and v > 1_000_000:
            return v / 100_000
        return v

    @computed_field
    @property
    def discount_pct(self) -> Optional[float]:
        """Tính phần trăm giảm giá."""
        if self.original_price and self.original_price > 0 and self.price < self.original_price:
            return round((1 - self.price / self.original_price) * 100, 1)
        return None

    @classmethod
    def from_shopee_item(cls, item: dict, keyword: str | None = None) -> "ProductSchema":
        """Factory method: parse từ Shopee API item_basic response.

        Args:
            item: dict từ Shopee API (trường `item_basic` hoặc trực tiếp item)
            keyword: keyword tìm kiếm (để tracking)

        Returns:
            ProductSchema instance đã validate
        """
        # Handle nested item_basic
        item_data = item.get("item_basic", item)

        # Build image URL từ image ID
        image_id = item_data.get("image", "")
        image_url = f"https://cf.shopee.vn/file/{image_id}" if image_id else None

        # Build product URL
        product_name_slug = item_data.get("name", "").replace(" ", "-")
        product_id = item_data.get("itemid", 0)
        shop_id = item_data.get("shopid", 0)
        product_url = f"https://shopee.vn/{product_name_slug}-i.{shop_id}.{product_id}"

        # Extract rating
        rating_info = item_data.get("item_rating", {})
        rating_star = rating_info.get("rating_star", None) if isinstance(rating_info, dict) else None

        return cls(
            product_id=item_data.get("itemid", 0),
            shop_id=item_data.get("shopid", 0),
            name=item_data.get("name", ""),
            price=item_data.get("price", 0),
            original_price=item_data.get("price_before_discount"),
            category_id=item_data.get("catid"),
            shop_location=item_data.get("shop_location"),
            rating=rating_star,
            review_count=item_data.get("cmt_count", 0),
            sold_count=item_data.get("historical_sold", 0),
            liked_count=item_data.get("liked_count", 0),
            stock=item_data.get("stock", 0),
            image_url=image_url,
            url=product_url,
            keyword=keyword,
        )


class ProductListResponse(BaseModel):
    """Response wrapper cho danh sách sản phẩm."""

    products: list[ProductSchema]
    total: int = Field(ge=0, description="Tổng số sản phẩm thu thập được")
    keyword: Optional[str] = None
    page: int = Field(default=1, ge=1)
    scraped_at: datetime = Field(default_factory=datetime.now)
