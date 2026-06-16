"""
FastAPI Backend — Vietnam E-Commerce Analytics Platform.

Entry point cho API server. Đọc dữ liệu từ Gold Layer (Parquet)
bằng pandas khi khởi động, phục vụ qua REST API.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend.app.services.data_service import data_service
from backend.app.routers import products, analytics
from backend.app.models.schemas import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load dữ liệu vào memory khi server khởi động."""
    logger.info("🚀 Đang khởi động Backend API...")
    data_service.load_data()
    logger.success("✅ Server sẵn sàng phục vụ!")
    yield
    logger.info("👋 Server đang tắt...")


app = FastAPI(
    title="🛒 Vietnam E-Commerce Analytics API",
    description=(
        "REST API phục vụ dữ liệu phân tích thương mại điện tử Việt Nam.\n\n"
        "Dữ liệu được thu thập từ Shopee, xử lý qua pipeline "
        "Bronze → Silver → Gold (Delta Lake), và phục vụ qua API này."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — cho phép frontend (Next.js) gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên giới hạn domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(products.router)
app.include_router(analytics.router)


@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Kiểm tra trạng thái server và dữ liệu."""
    return HealthResponse(
        status="healthy",
        total_products=len(data_service.df_product_metrics),
        total_reviews=len(data_service.df_reviews),
    )


@app.post("/api/reload", tags=["System"])
async def reload_data():
    """Reload dữ liệu từ Gold Layer (gọi sau khi ETL pipeline chạy xong)."""
    data_service.reload_data()
    return {"status": "reloaded", "total_products": len(data_service.df_product_metrics)}
