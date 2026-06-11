# 📋 Plan Đồ Án Mới — Data Lakehouse + Full-Stack Analytics Platform

> Tài liệu này là bản kế hoạch chi tiết cho đồ án tiếp theo, xây dựng dựa trên kinh nghiệm từ dự án Crypto Data Lakehouse, bổ sung thêm các kỹ năng thiếu cho vị trí **Data Engineer / Data Analyst**.

---

## Mục lục

- [1. Tổng quan đồ án](#1-tổng-quan-đồ-án)
- [2. Gợi ý Data Source](#2-gợi-ý-data-source)
- [3. Kiến trúc hệ thống](#3-kiến-trúc-hệ-thống)
- [4. Tổ chức thư mục](#4-tổ-chức-thư-mục)
- [5. Chi tiết từng module](#5-chi-tiết-từng-module)
- [6. Web Dashboard (Full-Stack)](#6-web-dashboard-full-stack)
- [7. Kỹ năng cải thiện cho DE/DA](#7-kỹ-năng-cải-thiện-cho-deda)
- [8. Timeline thực hiện](#8-timeline-thực-hiện)
- [9. So sánh với đồ án Crypto](#9-so-sánh-với-đồ-án-crypto)

---

## 1. Tổng quan đồ án

### Ý tưởng: **Vietnam E-Commerce Analytics Platform**

Xây dựng nền tảng phân tích dữ liệu thương mại điện tử Việt Nam, thu thập và xử lý dữ liệu sản phẩm, giá cả, đánh giá từ sàn TMĐT Shopee để phân tích thị trường.

### Tại sao chọn đề tài này?

| Tiêu chí | Crypto Lakehouse (đã làm) | E-Commerce Analytics (mới) |
|-----------|--------------------------|---------------------------|
| **Domain** | Tài chính / Crypto | Thương mại điện tử |
| **Tính ứng dụng** | Niche market | Phổ biến, dễ hiểu với nhà tuyển dụng |
| **Data variety** | Chỉ có số (OHLCV) | Số + Text + Category + Image URL |
| **NLP skills** | Không có | Sentiment Analysis trên reviews |
| **BI/Dashboard** | Chỉ có Flask basic | Full-stack web dashboard |
| **Data volume** | ~10-45 MB/ngày | ~100-500 MB/ngày (nhiều hơn) |
| **Portfolio impact** | Tốt | Rất tốt (recruiter dễ hiểu) |

### Mục tiêu kỹ năng

```
✅ Giữ nguyên từ Crypto project:
   - Medallion Architecture (Bronze → Silver → Gold)
   - Apache Kafka + Spark Streaming
   - Delta Lake + ACID transactions
   - Apache Airflow orchestration
   - Docker Compose deployment
   - Data Quality & Validation

🆕 Kỹ năng MỚI bổ sung:
   - Full-stack web dashboard (React/Next.js + API)
   - NLP / Text Analytics (Sentiment Analysis)
   - Data Visualization nâng cao (Chart.js / D3.js / Recharts)
   - REST API design (FastAPI)
   - Database design (PostgreSQL cho OLTP)
   - Monitoring & Observability (Prometheus + Grafana)
   - CI/CD pipeline (GitHub Actions)
   - Data Catalog & Lineage
   - Unit Testing & Integration Testing
```

---

## 2. Gợi ý Data Source

### Phương án A: E-Commerce Vietnam (⭐ Đề xuất chính)

| Nguồn | Loại | Phương thức | Dữ liệu |
|--------|------|-------------|----------|
| **Shopee** | Web Scraping / API | Scrapy/Shopee Open API | Sản phẩm, giá, rating, reviews, seller info |
| **Vietnam CPI** | Open Data | GSO Vietnam | Chỉ số giá tiêu dùng (tham chiếu) |

**Ưu điểm:**
- Dữ liệu đa dạng (structured + unstructured)
- Có thể so sánh giá cross-platform
- Text reviews → NLP sentiment analysis
- Dễ giải thích cho nhà tuyển dụng

**Endpoints mẫu (Shopee):**
```
GET https://shopee.vn/api/v4/item/get?itemid=...&shopid=...
GET https://shopee.vn/api/v2/item/get_ratings?itemid=...&shopid=...
```

### Phương án B: Vietnam Stock Market

| Nguồn | Loại | Phương thức | Dữ liệu |
|--------|------|-------------|----------|
| **VNDirect** | REST API | `vnstock` library | OHLCV, order book, financial reports |
| **SSI** | WebSocket | SSI Fast Connect | Real-time quotes, market depth |
| **CafeF** | Scraping | BeautifulSoup | News, phân tích kỹ thuật |
| **TCBS** | API | `tcbs-stock-api` | Financials, insider trading |

**Ưu điểm:**
- Tương tự Crypto nhưng regulated market
- Có financial reports → EDA nâng cao
- Vietnam-focused → có giá trị local

### Phương án C: IoT / Smart City

| Nguồn | Loại | Phương thức | Dữ liệu |
|--------|------|-------------|----------|
| **OpenWeatherMap** | REST API | Free tier | Thời tiết real-time, forecast |
| **AQI (Air Quality)** | API | `aqicn.org` | Chất lượng không khí |
| **Traffic Data** | API | Google Maps / HERE | Tình trạng giao thông |
| **IoT Simulator** | Generated | Python faker | Sensor data (nhiệt độ, độ ẩm) |

**Ưu điểm:**
- IoT rất hot trong Data Engineering
- Dễ tạo data volume lớn (simulator)
- Time-series analysis

### 🏆 Đề xuất: **Phương án A (E-Commerce)** vì:
1. Recruiter dễ hiểu → portfolio impact cao
2. Data đa dạng nhất (số + text + category)
3. Bổ sung NLP skill mà CV đang thiếu
4. Có thể build dashboard đẹp với product cards, charts

---

## 3. Kiến trúc hệ thống

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                                     │
│  ┌──────────────────────────────────────────────────────────────┐        │
│  │                          Shopee                              │        │
│  │                 (Scraping & Internal API)                    │        │
│  └──────────────────────────────┬───────────────────────────────┘        │
└─────────────────────────────────┼────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      INGESTION LAYER                                      │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │                     Scrapy Spiders                           │       │
│  │                   (Scheduled crawls)                         │       │
│  └──────────────────────────────┬───────────────────────────────┘       │
│                                 │                                       │
│                                 ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │              Apache Kafka Topics                              │       │
│  │  • raw_products    • raw_reviews                              │       │
│  └────────────┬─────────────────────────────────────────────────┘       │
└───────────────┼────────────────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   PROCESSING LAYER (Apache Spark)                         │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│  │   BRONZE          │  │   SILVER          │  │   GOLD            │       │
│  │   Raw append-only │  │   Clean + Dedup   │  │   Analytics-ready │       │
│  │                   │  │   + NLP Sentiment  │  │   + Aggregations  │       │
│  │   • products_raw  │  │   • products      │  │   • price_trends  │       │
│  │   • reviews_raw   │  │   • reviews       │  │   • category_stats│       │
│  │                   │  │   • sentiment     │  │   • seller_ranking│       │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘       │
│                                                                          │
│                        Delta Lake (GCS / MinIO)                           │
└──────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      SERVING LAYER                                        │
│                                                                          │
│  ┌────────────────────┐  ┌────────────────────┐  ┌──────────────────┐   │
│  │ FastAPI Backend     │  │ Trino SQL Engine   │  │ PostgreSQL       │   │
│  │ (REST API cho web)  │  │ (Ad-hoc queries)   │  │ (App database)   │   │
│  └─────────┬──────────┘  └────────────────────┘  └──────────────────┘   │
│            │                                                              │
│            ▼                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │                    Next.js Web Dashboard                          │    │
│  │  • Product price tracker    • Category analytics                  │    │
│  │  • Sentiment dashboard      • Seller ranking                      │    │
│  │  • Price alerts             • Alerts management                   │    │
│  └──────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION & MONITORING                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ Airflow DAGs │  │ Prometheus   │  │ Grafana      │  │ GitHub      │ │
│  │ (Scheduling) │  │ (Metrics)    │  │ (Dashboards) │  │ Actions CI  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └─────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Tổ chức thư mục

```
ECommerce-Analytics-Platform/
│
├── 📄 README.md                        # Giới thiệu project
├── 📄 docker-compose.yml               # Orchestration toàn bộ services
├── 📄 docker-compose.dev.yml           # Override cho local dev
├── 📄 Makefile                         # Shortcuts: make up, make test, make lint
├── 📄 .env.example                     # Template biến môi trường
├── 📄 .gitignore
├── 📄 pyproject.toml                   # Python project config (thay requirements.txt)
│
├── 📁 ingestion/                       # === DATA INGESTION ===
│   ├── scrapers/
│   │   └── shopee_spider.py            # Scrapy spider cho Shopee
│   ├── producers/
│   │   ├── kafka_producer.py           # Base Kafka producer (shared)
│   │   ├── product_producer.py         # Products → Kafka
│   │   └── review_producer.py          # Reviews → Kafka
│   ├── schemas/
│   │   ├── product_schema.py           # Pydantic models cho validation
│   │   └── review_schema.py
│   ├── tests/
│   │   ├── test_scrapers.py
│   │   └── test_producers.py
│   └── requirements.txt
│
├── 📁 processing/                      # === SPARK ETL PIPELINE ===
│   ├── bronze/
│   │   └── kafka_to_bronze.py          # Kafka → Bronze (Structured Streaming)
│   ├── silver/
│   │   ├── products_cleansing.py       # Bronze → Silver (Products)
│   │   ├── reviews_cleansing.py        # Bronze → Silver (Reviews)
│   │   └── sentiment_analysis.py       # NLP: Review text → sentiment score
│   ├── gold/
│   │   ├── price_trends.py            # Silver → Gold: Price analytics
│   │   ├── category_stats.py          # Silver → Gold: Category aggregation
│   │   └── seller_ranking.py          # Silver → Gold: Seller performance
│   ├── utils/
│   │   ├── spark_session.py           # Shared SparkSession factory
│   │   ├── gcs_auth.py               # GCS authentication helper
│   │   └── data_quality.py           # Shared DQ rules engine
│   └── tests/
│       ├── test_bronze.py
│       ├── test_silver.py
│       └── test_gold.py
│
├── 📁 backend/                         # === FASTAPI REST API ===
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI entry point
│   │   ├── config.py                  # Settings (pydantic-settings)
│   │   ├── models/                    # SQLAlchemy / Pydantic models
│   │   │   ├── product.py
│   │   │   ├── review.py
│   │   │   └── alert.py
│   │   ├── routers/                   # API endpoints
│   │   │   ├── products.py           # /api/products
│   │   │   ├── analytics.py          # /api/analytics
│   │   │   ├── trends.py             # /api/trends
│   │   │   └── alerts.py             # /api/alerts
│   │   ├── services/                  # Business logic
│   │   │   ├── trino_service.py      # Query Trino Gold tables
│   │   │   └── alert_service.py      # Price alert logic
│   │   └── middleware/
│   │       ├── auth.py               # JWT authentication
│   │       └── rate_limit.py         # API rate limiting
│   ├── tests/
│   │   ├── test_products.py
│   │   └── test_analytics.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── 📁 frontend/                        # === NEXT.JS WEB DASHBOARD ===
│   ├── src/
│   │   ├── app/                       # Next.js App Router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx               # Home / Overview dashboard
│   │   │   ├── products/
│   │   │   │   └── page.tsx           # Product search & comparison
│   │   │   ├── analytics/
│   │   │   │   └── page.tsx           # Charts & analytics
│   │   │   ├── trends/
│   │   │   │   └── page.tsx           # Market trends
│   │   │   └── alerts/
│   │   │       └── page.tsx           # Price alerts management
│   │   ├── components/
│   │   │   ├── ui/                    # Reusable UI (shadcn/ui)
│   │   │   ├── charts/               # Chart components (Recharts)
│   │   │   ├── ProductCard.tsx
│   │   │   ├── PriceHistory.tsx
│   │   │   ├── SentimentGauge.tsx
│   │   │   └── TrendChart.tsx
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── useProducts.ts
│   │   │   └── useAnalytics.ts
│   │   └── lib/
│   │       ├── api.ts                 # API client (axios/fetch)
│   │       └── utils.ts
│   ├── Dockerfile
│   ├── package.json
│   └── tailwind.config.ts
│
├── 📁 dags/                            # === AIRFLOW ORCHESTRATION ===
│   ├── 01_ingestion_dag.py            # Scraping + API collection
│   ├── 02_bronze_streaming_dag.py     # Kafka → Bronze
│   ├── 03_silver_dag.py               # Bronze → Silver + NLP
│   ├── 04_gold_dag.py                 # Silver → Gold aggregations
│   ├── 05_sync_to_postgres_dag.py     # Gold → PostgreSQL (cho API)
│   └── 06_maintenance_dag.py          # Delta VACUUM, cleanup
│
├── 📁 dbt/                             # === DATA QUALITY & MODELING ===
│   ├── models/
│   │   ├── staging/                   # 1:1 mapping từ source
│   │   ├── intermediate/             # Business logic transforms
│   │   └── marts/                    # Final analytics tables
│   ├── tests/                        # Data quality tests
│   ├── seeds/                        # Reference data (categories)
│   └── dbt_project.yml
│
├── 📁 ml/                              # === MACHINE LEARNING ===
│   ├── notebooks/
│   │   ├── 01_EDA.ipynb              # Exploratory Data Analysis
│   │   ├── 02_sentiment_model.ipynb  # NLP model development
│   │   └── 03_price_prediction.ipynb # Price forecasting
│   ├── models/
│   │   ├── sentiment/                # PhoBERT / ViSoBERT fine-tuned
│   │   └── forecasting/             # Prophet / LSTM
│   ├── training/
│   │   ├── train_sentiment.py
│   │   └── train_forecaster.py
│   └── serving/
│       └── model_api.py              # MLflow / BentoML serving
│
├── 📁 monitoring/                      # === OBSERVABILITY ===
│   ├── prometheus/
│   │   └── prometheus.yml            # Scrape config
│   ├── grafana/
│   │   ├── provisioning/
│   │   │   └── dashboards/
│   │   │       ├── pipeline_health.json
│   │   │       └── data_quality.json
│   │   └── Dockerfile
│   └── alertmanager/
│       └── config.yml                # Alert rules
│
├── 📁 infra/                           # === INFRASTRUCTURE ===
│   ├── spark/
│   │   ├── Dockerfile
│   │   └── start-spark.sh
│   ├── kafka/
│   │   └── Dockerfile
│   ├── airflow/
│   │   └── Dockerfile
│   ├── trino/
│   │   └── catalog/
│   │       └── delta.properties
│   ├── hive/
│   │   └── hive-site.xml
│   └── scripts/
│       └── init_postgres.sql
│
├── 📁 tests/                           # === INTEGRATION TESTS ===
│   ├── e2e/
│   │   ├── test_full_pipeline.py     # End-to-end pipeline test
│   │   └── test_api_integration.py   # API integration test
│   ├── conftest.py                   # Shared fixtures
│   └── docker-compose.test.yml       # Test environment
│
├── 📁 docs/                            # === DOCUMENTATION ===
│   ├── ARCHITECTURE.md
│   ├── QUICK_START.md
│   ├── DATA_DICTIONARY.md            # 🆕 Schema documentation
│   ├── API_REFERENCE.md              # 🆕 API endpoints docs
│   ├── RUNBOOK.md                    # 🆕 Operations runbook
│   └── diagrams/
│       ├── system_architecture.png
│       └── data_flow.png
│
├── 📁 .github/                         # === CI/CD ===
│   └── workflows/
│       ├── ci.yml                    # Lint + Test on PR
│       ├── cd.yml                    # Deploy on merge to main
│       └── data_quality.yml          # Scheduled DQ checks
│
└── 📁 scripts/                         # === UTILITY SCRIPTS ===
    ├── setup_dev.sh                  # One-click dev setup
    ├── seed_data.py                  # Load sample data
    └── health_check.py              # Check all services
```

### So sánh tổ chức thư mục

| Aspect | Crypto Project (cũ) | E-Commerce Project (mới) |
|--------|---------------------|--------------------------|
| **Structure** | Flat (mọi thứ ở root) | Modular (mỗi layer 1 folder) |
| **Testing** | Minimal (`tests/`) | Per-module + E2E + CI |
| **Backend** | Flask basic trong ML/ | FastAPI riêng biệt |
| **Frontend** | Template HTML | Next.js full SPA |
| **Config** | `.env` only | `pyproject.toml` + `.env` |
| **CI/CD** | Không có | GitHub Actions |
| **Monitoring** | Không có | Prometheus + Grafana |
| **Docs** | Markdown files | Structured + API docs |

---

## 5. Chi tiết từng module

### 5.1. Ingestion Layer

```python
# ingestion/schemas/product_schema.py — Pydantic validation (MỚI)
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class ProductSchema(BaseModel):
    """Schema validation trước khi đẩy vào Kafka"""
    product_id: str
    platform: str  # "shopee"
    name: str = Field(min_length=1, max_length=500)
    price: float = Field(gt=0)
    original_price: Optional[float] = None
    discount_pct: Optional[float] = Field(ge=0, le=100, default=None)
    category: str
    seller_name: str
    rating: Optional[float] = Field(ge=0, le=5, default=None)
    review_count: int = Field(ge=0)
    sold_count: int = Field(ge=0)
    url: str
    image_url: Optional[str] = None
    scraped_at: datetime

    @validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be positive")
        return v
```

**Kỹ năng mới học được:**
- Pydantic validation (thay vì DQ rules trong Spark)
- Scrapy framework (web scraping có cấu trúc)
- Rate limiting & politeness (robots.txt compliance)

### 5.2. Processing Layer (Spark ETL)

```python
# processing/silver/sentiment_analysis.py — NLP Pipeline (MỚI)
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import FloatType, StringType
from underthesea import sentiment  # Vietnamese NLP

@F.udf(returnType=FloatType())
def analyze_sentiment(text: str) -> float:
    """Phân tích sentiment review tiếng Việt"""
    if not text:
        return 0.0
    result = sentiment(text)
    # Map: positive → 1.0, negative → -1.0, neutral → 0.0
    mapping = {"positive": 1.0, "negative": -1.0, "neutral": 0.0}
    return mapping.get(result, 0.0)

def transform_reviews(df: DataFrame) -> DataFrame:
    """Bronze Reviews → Silver Reviews + Sentiment Score"""
    return (
        df
        .withColumn("sentiment_score", analyze_sentiment(F.col("review_text")))
        .withColumn("sentiment_label",
            F.when(F.col("sentiment_score") > 0, "positive")
             .when(F.col("sentiment_score") < 0, "negative")
             .otherwise("neutral")
        )
        .withColumn("review_length", F.length("review_text"))
        .withColumn("processed_at", F.current_timestamp())
    )
```

**Kỹ năng mới học được:**
- NLP / Text Analytics (Sentiment Analysis)
- UDF trong PySpark
- Vietnamese NLP (`underthesea` / `PhoBERT`)

### 5.3. Backend API (FastAPI)

```python
# backend/app/routers/analytics.py — RESTful API (MỚI)
from fastapi import APIRouter, Query, Depends
from typing import Optional
from datetime import date

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/price-trends")
async def get_price_trends(
    category: str = Query(..., description="Product category"),
    platform: Optional[str] = Query(None, description="shopee|tiki|lazada"),
    start_date: date = Query(...),
    end_date: date = Query(...),
    interval: str = Query("daily", regex="^(hourly|daily|weekly)$"),
):
    """
    Trả về xu hướng giá theo category và platform.
    Query trực tiếp từ Gold layer qua Trino.
    """
    query = """
        SELECT
            platform, category, price_date,
            AVG(avg_price) as avg_price,
            MIN(min_price) as min_price,
            MAX(max_price) as max_price,
            SUM(product_count) as total_products
        FROM delta_gcs.gold.price_trends
        WHERE category = :category
          AND price_date BETWEEN :start_date AND :end_date
        GROUP BY platform, category, price_date
        ORDER BY price_date
    """
    results = await trino_service.execute(query, params={...})
    return {"data": results, "meta": {"category": category, "interval": interval}}
```

**Kỹ năng mới học được:**
- FastAPI (modern Python web framework)
- REST API design (CRUD, pagination, filtering)
- Async/await patterns
- API documentation (OpenAPI / Swagger)
- Authentication (JWT)

### 5.4. Frontend Dashboard (Next.js)

```
Dashboard Pages:
├── / (Overview)
│   ├── KPI Cards: Total products, Avg price, Top categories
│   ├── Price Trend Chart (line chart, multi-platform)
│   └── Recent Alerts
│
├── /products (Product Explorer)
│   ├── Search & Filter (by category, platform, price range)
│   ├── Product Cards (image, name, price, rating, platform badge)
│   ├── Price Comparison Table (cross-platform)
│   └── Pagination
│
├── /analytics (Deep Analytics)
│   ├── Category Distribution (pie/donut chart)
│   ├── Price Distribution (histogram)
│   ├── Sentiment Analysis (bar chart by category)
│   ├── Seller Ranking (table with sparklines)
│   └── Google Trends Overlay
│
├── /trends (Market Trends)
│   ├── Trending Products (by sold_count growth)
│   ├── Price Drop Alerts
│   ├── Seasonal Patterns (heatmap)
│   └── Cross-Platform Price Gap
│
└── /alerts (Alert Management)
    ├── Create Price Alert (product + threshold)
    ├── Active Alerts List
    └── Alert History
```

**Kỹ năng mới học được:**
- React / Next.js (modern frontend)
- Data Visualization (Recharts / Chart.js)
- Responsive design (Tailwind CSS)
- State management (React Query / SWR)
- Server-Side Rendering (SSR)

---

## 6. Web Dashboard (Full-Stack)

### Tech Stack cho Web

| Layer | Technology | Lý do chọn |
|-------|-----------|------------|
| **Frontend** | Next.js 14 (App Router) | SSR + SEO + React ecosystem |
| **Styling** | Tailwind CSS + shadcn/ui | Rapid development, beautiful UI |
| **Charts** | Recharts hoặc Chart.js | React-native, interactive |
| **Backend** | FastAPI (Python) | Async, type-safe, auto-docs |
| **ORM** | SQLAlchemy + Alembic | Migration management |
| **App DB** | PostgreSQL | OLTP cho user data, alerts |
| **Analytics DB** | Trino → Delta Lake | OLAP cho Gold layer queries |
| **Auth** | NextAuth.js + JWT | Social login (Google/GitHub) |
| **Cache** | Redis | API response caching |
| **Real-time** | WebSocket / SSE | Live price updates |

### Dashboard wireframe concept

```
┌──────────────────────────────────────────────────────────────────────┐
│  🛒 E-Commerce Analytics          [Search...]    👤 Login   🔔 3    │
├──────────┬───────────────────────────────────────────────────────────┤
│          │                                                           │
│ 📊 Home  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│          │  │ 125,432  │ │ ₫245K   │ │  4.2★   │ │  +12%   │       │
│ 🏷️ Prods │  │ Products │ │ Avg Prc │ │ Avg Rat │ │ Growth  │       │
│          │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │
│ 📈 Stats │                                                           │
│          │  ┌─────────────────────────────────────────────────┐     │
│ 📉 Trend │  │                                                 │     │
│          │  │         Price Trend Chart (30 days)              │     │
│ 🔔 Alert │  │         ──── Shopee  ──── Tiki  ──── Lazada    │     │
│          │  │                                                 │     │
│ ⚙️ Sett  │  └─────────────────────────────────────────────────┘     │
│          │                                                           │
│          │  ┌──────────────────┐  ┌──────────────────────────┐     │
│          │  │ Top Categories   │  │ Sentiment Distribution    │     │
│          │  │ 🥇 Điện thoại   │  │ 😀 Positive: 67%         │     │
│          │  │ 🥈 Thời trang   │  │ 😐 Neutral:  21%         │     │
│          │  │ 🥉 Gia dụng    │  │ 😡 Negative: 12%         │     │
│          │  └──────────────────┘  └──────────────────────────┘     │
└──────────┴───────────────────────────────────────────────────────────┘
```

---

## 7. Kỹ năng cải thiện cho DE/DA

### 7.1. Kỹ năng THIẾU cho Data Engineer

| Kỹ năng | Mức độ thiếu | Cách bổ sung trong đồ án mới |
|---------|-------------|------------------------------|
| **SQL nâng cao** | ⚠️ Trung bình | Viết complex queries trong Trino + dbt models |
| **Data Modeling** | ❌ Thiếu | Thiết kế Star Schema cho Gold layer |
| **CI/CD** | ❌ Thiếu | GitHub Actions: lint → test → deploy |
| **Monitoring** | ❌ Thiếu | Prometheus + Grafana dashboards |
| **Data Catalog** | ❌ Thiếu | dbt docs generate → Data Dictionary |
| **API Design** | ❌ Thiếu | FastAPI RESTful endpoints |
| **Testing** | ⚠️ Yếu | pytest + Great Expectations + E2E tests |
| **Cost Optimization** | ❌ Thiếu | Partition pruning, data lifecycle, compaction |
| **Security** | ⚠️ Yếu | JWT auth, secrets management, RBAC |
| **Documentation** | ⚠️ Trung bình | API docs, Data Dictionary, Runbook |

### 7.2. Kỹ năng THIẾU cho Data Analyst

| Kỹ năng | Mức độ thiếu | Cách bổ sung |
|---------|-------------|-------------|
| **EDA sâu** | ⚠️ Trung bình | Jupyter notebooks với proper EDA workflow |
| **Statistical Analysis** | ❌ Thiếu | Hypothesis testing, A/B test framework |
| **Advanced Visualization** | ⚠️ Trung bình | Interactive charts (Plotly, D3.js) |
| **Storytelling with Data** | ❌ Thiếu | Dashboard narrative, insight reports |
| **Business Metrics** | ❌ Thiếu | Conversion, retention, LTV calculations |
| **A/B Testing** | ❌ Thiếu | Giả lập A/B test cho pricing strategy |
| **Excel/Spreadsheet** | ✅ Đã có | — |
| **Power BI** | ✅ Đã có | Kết nối với Trino Gold layer |

### 7.3. Action Items cụ thể

#### Giai đoạn 1: Foundation (Tuần 1-2)
```
□ Học FastAPI basics (docs.fastapi.tiangolo.com)
□ Học Next.js App Router (nextjs.org/docs)
□ Học dbt fundamentals (courses.getdbt.com — FREE)
□ Setup project structure + Docker Compose
```

#### Giai đoạn 2: Data Pipeline (Tuần 3-5)
```
□ Viết scrapers (Scrapy/BeautifulSoup)
□ Kafka producers + Bronze streaming
□ Silver transformations + NLP sentiment
□ Gold aggregations (price trends, category stats)
□ Airflow DAGs cho orchestration
□ dbt models + tests
```

#### Giai đoạn 3: Web Dashboard (Tuần 6-8)
```
□ FastAPI backend (REST endpoints)
□ Next.js frontend (dashboard pages)
□ Interactive charts (Recharts)
□ Authentication (JWT/NextAuth)
□ Real-time updates (WebSocket/SSE)
```

#### Giai đoạn 4: Polish (Tuần 9-10)
```
□ Monitoring (Prometheus + Grafana)
□ CI/CD (GitHub Actions)
□ Unit tests + Integration tests
□ Documentation (README, API docs, Data Dictionary)
□ Demo video + Portfolio write-up
```

---

## 8. Timeline thực hiện

```
Tuần 1-2:  ████░░░░░░  Setup + Ingestion
Tuần 3-4:  ░░████░░░░  Bronze + Silver + NLP
Tuần 5:    ░░░░██░░░░  Gold + Airflow + dbt
Tuần 6-7:  ░░░░░░████  Backend API + Frontend
Tuần 8:    ░░░░░░░░██  Dashboard polish + Charts
Tuần 9:    ░░░░░░░░░█  Monitoring + CI/CD
Tuần 10:   ░░░░░░░░░█  Testing + Docs + Demo
```

**Tổng thời gian: ~10 tuần** (part-time, 15-20 giờ/tuần)

---

## 9. So sánh với đồ án Crypto

| Aspect | Crypto Lakehouse ✅ | E-Commerce Platform 🆕 |
|--------|---------------------|------------------------|
| **Medallion Architecture** | ✅ Bronze/Silver/Gold | ✅ Bronze/Silver/Gold |
| **Kafka Streaming** | ✅ WebSocket → Kafka | ✅ Scrapers → Kafka |
| **Spark ETL** | ✅ PySpark batch + streaming | ✅ PySpark batch + streaming |
| **Delta Lake** | ✅ ACID on GCS | ✅ ACID on GCS/MinIO |
| **Airflow** | ✅ 5 DAGs | ✅ 6 DAGs |
| **Trino SQL** | ✅ Ad-hoc queries | ✅ Ad-hoc + API backend |
| **Docker** | ✅ Compose v3.8 | ✅ Compose + dev override |
| **Data Quality** | ✅ Inline DQ + quarantine | ✅ Pydantic + dbt tests + GE |
| **NLP** | ❌ | 🆕 Sentiment Analysis |
| **Full-stack Web** | ❌ (Flask basic) | 🆕 FastAPI + Next.js |
| **REST API** | ❌ | 🆕 FastAPI endpoints |
| **Monitoring** | ❌ | 🆕 Prometheus + Grafana |
| **CI/CD** | ❌ | 🆕 GitHub Actions |
| **Testing** | ⚠️ Minimal | 🆕 Unit + Integration + E2E |
| **Data Catalog** | ❌ | 🆕 dbt docs |
| **Star Schema** | ❌ | 🆕 Dimensional modeling |
| **Caching** | ❌ | 🆕 Redis |
| **Auth** | ❌ | 🆕 JWT + NextAuth |

### Kỹ năng mới sẽ có sau khi hoàn thành

```
Data Engineering:
  ✅ Pipeline design (streaming + batch)    ← đã có
  🆕 API design (FastAPI)                   ← MỚI
  🆕 Data Modeling (Star Schema, dbt)       ← MỚI
  🆕 Monitoring & Observability             ← MỚI
  🆕 CI/CD pipelines                        ← MỚI
  🆕 Testing practices                      ← MỚI

Data Analysis:
  ✅ EDA & visualization                    ← đã có
  🆕 NLP / Text Analytics                   ← MỚI
  🆕 Interactive Dashboards                 ← MỚI
  🆕 Business Metrics design                ← MỚI

Software Engineering:
  🆕 Full-stack development                 ← MỚI
  🆕 REST API design                        ← MỚI
  🆕 Frontend (React/Next.js)               ← MỚI
  🆕 Authentication & Authorization         ← MỚI
```

---

## Kết luận

Đồ án mới **E-Commerce Analytics Platform** sẽ giúp bạn:

1. **Giữ nguyên** mọi kỹ năng Big Data đã có từ Crypto project
2. **Bổ sung** 10+ kỹ năng mới quan trọng cho DE/DA
3. **Tạo portfolio** đa dạng (Finance + E-Commerce)
4. **Xây dựng** sản phẩm end-to-end mà recruiter dễ hiểu và ấn tượng
5. **Chuẩn bị** cho interview với kiến thức toàn diện

> 💡 **Tip**: Khi interview, bạn có thể so sánh 2 dự án để thể hiện khả năng áp dụng kiến trúc tương tự cho domain khác nhau — đây là dấu hiệu của một kỹ sư trưởng thành.
