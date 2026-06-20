# Skills & Competencies — Data Analytics Portfolio

> Documented skills and hands-on experience gained from building the **Vietnam E-Commerce Analytics Platform**, an end-to-end data engineering and analytics project covering data collection, ETL processing, NLP analysis, API development, and dashboard visualization.

---

## 1. Data Collection & Web Scraping

- Designed and implemented automated data collection pipelines using **Playwright** with Chrome DevTools Protocol (CDP) to extract structured data from Shopee Vietnam.
- Intercepted real-time API responses at the network layer to capture product metadata, pricing, and customer reviews — bypassing traditional HTML scraping limitations.
- Built a modular scraper architecture with configurable parameters (keyword, pagination depth, review limits) and robust error handling for production-grade reliability.
- Structured raw output into **JSONL** format with schema validation using **Pydantic**, ensuring data quality from the point of collection.

**Tools:** Playwright, Chrome CDP, Pydantic, Python

---

## 2. Data Engineering & ETL Pipeline

- Architected a **Medallion Data Lakehouse** (Bronze → Silver → Gold) using **Apache Spark** and **Delta Lake**, following industry-standard patterns used at Databricks and major tech companies.
- **Bronze Layer** — Ingested raw JSONL files into Delta Lake with full schema preservation and ACID transaction guarantees.
- **Silver Layer** — Implemented data cleansing pipelines: deduplication by primary key, text normalization (whitespace, newlines), timestamp parsing, and null handling.
- **Gold Layer** — Built aggregation jobs computing product-level metrics: average ratings, star distributions (1–5), review counts, and derived KPIs such as 5-star percentage.
- Applied **PySpark DataFrame API** for distributed data transformations including `groupBy`, `agg`, `join`, `withColumn`, `fillna`, and window functions.
- Managed data partitioning and storage optimization with Parquet columnar format for efficient analytical queries.

**Tools:** Apache Spark (PySpark), Delta Lake, Parquet, pandas

---

## 3. Data Analysis & Metrics Design

- Defined and computed key business metrics for e-commerce analytics:
  - **Average Rating** — Weighted mean of customer ratings per product.
  - **Star Distribution** — Breakdown of 1-star through 5-star reviews with percentage calculations.
  - **Review Volume** — Total review counts as a proxy for product popularity and engagement.
  - **Price Analysis** — Average pricing across product categories.
- Designed a **Gold Layer schema** optimized for analytical queries, joining product attributes with aggregated review statistics in a single denormalized table.
- Applied statistical thinking to filter meaningful rankings (e.g., excluding products with zero reviews from top-rated lists).

**Tools:** PySpark, pandas, SQL-style DataFrame operations

---

## 4. NLP & Sentiment Analysis

- Implemented **Vietnamese-language sentiment analysis** using the `underthesea` NLP library to classify customer reviews as positive, negative, or neutral.
- Built a batch processing pipeline that reads cleaned review text, applies sentiment classification, and persists results as enriched Parquet files in the Gold Layer.
- Computed aggregate sentiment metrics (distribution percentages, counts by label) for both product-level and platform-level analysis.
- Integrated sentiment labels into the API and dashboard, enabling visual exploration of customer perception trends.

**Tools:** underthesea, pandas, scikit-learn, Python NLP

---

## 5. Backend API Development

- Designed and built a **RESTful API** using **FastAPI** with 9 endpoints serving analytics data, product listings, review details, and sentiment summaries.
- Implemented a high-performance data access layer using **pandas** and **pyarrow** to read Parquet files directly into memory — achieving sub-50ms response times without a traditional database.
- Applied software engineering best practices:
  - **Singleton pattern** for the data service layer to ensure single-load, shared-memory data access.
  - **Pydantic models** for request/response validation and automatic OpenAPI documentation.
  - **CORS middleware** for secure cross-origin frontend communication.
  - **Lifespan events** for data preloading on server startup.
- Built pagination, full-text search, and multi-column sorting for the product listing endpoint.

**Tools:** FastAPI, pandas, pyarrow, Pydantic, Uvicorn

---

## 6. Data Visualization & Dashboard

- Built an interactive analytics dashboard using **Next.js** (App Router) with **TailwindCSS** and **Recharts**.
- Designed and implemented multiple visualization types:
  - **KPI Cards** — At-a-glance metrics (total products, average price, average rating, total reviews).
  - **Bar Charts** — Star rating distribution and top product rankings.
  - **Donut Chart** — Sentiment analysis breakdown (positive / negative / neutral).
  - **Data Tables** — Sortable, searchable, paginated product listings with inline actions.
- Created interactive modal components for drill-down analysis:
  - **Product Detail Modal** — Full product information with star distribution progress bars.
  - **Reviews Modal** — Scrollable review list with sentiment badges and star ratings.
- Implemented responsive design, skeleton loading states, and staggered animations for polished user experience.

**Tools:** Next.js, React, TailwindCSS, Recharts, Lucide Icons

---

## 7. DevOps & Deployment

- Wrote multi-stage **Dockerfiles** for both backend (Python/FastAPI) and frontend (Node.js/Next.js), optimizing image size with selective layer copying and non-root user execution.
- Configured **Docker Compose** to orchestrate multi-container deployment with service networking, health checks, and volume mounts for the data layer.
- Set up **GitHub Actions CI/CD** pipeline with three automated jobs:
  - Python linting (Ruff) and unit testing (pytest) across Python 3.10 and 3.11.
  - Frontend linting (ESLint) and production build verification.
  - Docker image build checks for deployment readiness.
- Wrote 14 unit tests covering configuration, schema validation, data service logic, and ML module edge cases using pytest with mock data fixtures.

**Tools:** Docker, Docker Compose, GitHub Actions, pytest, Ruff

---

## 8. Software Engineering Practices

- Structured a large Python project using **pyproject.toml** with optional dependency groups (`backend`, `processing`, `ml`, `dev`) for modular installation.
- Maintained clean separation of concerns across layers: ingestion, processing, backend, frontend, and ML — each independently testable and deployable.
- Used **Loguru** for structured, leveled logging throughout all pipeline stages.
- Applied environment variable management with **python-dotenv** for configuration portability across development and production environments.
- Maintained version control with **Git**, writing descriptive conventional commits (`feat`, `fix`, `docs`, `ci`) and pushing to GitHub.

---

## Summary of Technical Skills

| Category | Skills |
|----------|--------|
| Programming | Python, JavaScript, SQL |
| Data Processing | Apache Spark, PySpark, pandas, Delta Lake, Parquet |
| NLP / ML | underthesea, scikit-learn, sentiment analysis |
| Backend | FastAPI, REST API design, Pydantic |
| Frontend | Next.js, React, TailwindCSS, Recharts |
| Data Collection | Playwright, web scraping, API interception |
| DevOps | Docker, Docker Compose, GitHub Actions, CI/CD |
| Data Architecture | Medallion Architecture, Data Lakehouse, ETL pipelines |
| Testing | pytest, unit testing, mock data |
| Tools | Git, VS Code, Chrome DevTools, Uvicorn |
