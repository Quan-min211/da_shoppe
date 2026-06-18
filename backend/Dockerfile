# ==============================
# Backend Dockerfile — FastAPI
# ==============================
# Multi-stage build: chỉ cài đúng dependencies cần thiết

FROM python:3.10-slim AS base

# Tránh .pyc files và buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ---- Stage 1: Dependencies ----
FROM base AS deps

# Cài system dependencies cho underthesea
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

# Cài backend + ml dependencies
RUN pip install --no-cache-dir -e ".[backend,ml]" 2>/dev/null || \
    pip install --no-cache-dir \
    "fastapi>=0.104.0" \
    "uvicorn[standard]>=0.24.0" \
    "pandas>=2.1.0" \
    "pyarrow>=14.0.0" \
    "underthesea>=6.8.0" \
    "scikit-learn>=1.3.0" \
    "pydantic>=2.5.0" \
    "pydantic-settings>=2.1.0" \
    "loguru>=0.7.0" \
    "python-dotenv>=1.0.0"

# ---- Stage 2: Runtime ----
FROM base AS runtime

# Copy installed packages from deps stage
COPY --from=deps /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy application code
COPY backend/ ./backend/
COPY ml/ ./ml/
COPY pyproject.toml ./

# Data sẽ được mount qua volume
# COPY data/ ./data/

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

# Chạy uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
