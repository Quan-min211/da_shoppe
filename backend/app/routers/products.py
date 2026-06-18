"""
Router cho Products API.
Endpoints: GET /api/products, GET /api/products/{product_id}
"""

import math
from fastapi import APIRouter, Query, HTTPException
from backend.app.services.data_service import data_service
from backend.app.models.schemas import PaginatedResponse
from backend.app.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=PaginatedResponse, summary="Danh sách sản phẩm")
async def list_products(
    page: int = Query(1, ge=1, description="Số trang"),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Số sản phẩm mỗi trang"),
    search: str = Query(None, description="Tìm kiếm theo tên sản phẩm"),
    sort_by: str = Query("avg_rating", description="Sắp xếp theo: avg_rating, price, total_reviews, sold_count"),
    sort_order: str = Query("desc", description="Thứ tự: asc hoặc desc"),
):
    """
    Lấy danh sách sản phẩm từ Gold Layer.
    
    Hỗ trợ:
    - **Phân trang** (page, page_size)
    - **Tìm kiếm** theo tên sản phẩm (search)
    - **Sắp xếp** theo nhiều tiêu chí (sort_by, sort_order)
    """
    records, total = data_service.get_products(
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return PaginatedResponse(
        data=records,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{product_id}", summary="Chi tiết sản phẩm")
async def get_product(product_id: str):
    """
    Lấy chi tiết 1 sản phẩm theo product_id.
    Bao gồm thông tin cơ bản + metrics đánh giá.
    """
    product = data_service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy sản phẩm: {product_id}")
    return product


@router.get("/{product_id}/reviews", summary="Reviews của sản phẩm")
async def get_product_reviews(product_id: str):
    """
    Lấy tất cả reviews/bình luận của 1 sản phẩm.
    """
    reviews = data_service.get_reviews_by_product(product_id)
    return {"product_id": product_id, "reviews": reviews, "total": len(reviews)}

