"""
Ingestion từ Raw JSONL (Local Storage) vào Bronze Layer (Delta Lake).
Đọc toàn bộ file jsonl trong data/raw/ và lưu vào data/bronze/ dưới định dạng Delta.
"""

import sys
from pathlib import Path
from loguru import logger

# Thêm root_dir vào sys.path để có thể import từ processing.utils
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from processing.utils.spark_session import get_spark_session


def run_bronze_ingestion():
    spark = get_spark_session("BronzeIngestion")
    
    # Đường dẫn
    raw_dir = project_root / "data" / "raw"
    bronze_dir = project_root / "data" / "bronze"
    
    products_raw_path = str(raw_dir / "products" / "*" / "*.jsonl")
    reviews_raw_path = str(raw_dir / "reviews" / "*" / "*.jsonl")
    
    products_bronze_path = str(bronze_dir / "products")
    reviews_bronze_path = str(bronze_dir / "reviews")
    
    # 1. Ingest Products
    logger.info(f"Đang đọc Raw Products từ: {products_raw_path}")
    try:
        df_products = spark.read.json(products_raw_path)
        
        # Ghi vào Bronze (Append mode)
        # Sử dụng write.format("delta")
        (
            df_products.write
            .format("delta")
            .mode("overwrite") # Overwrite cho đơn giản lúc dev, nếu prod thì append/merge
            .save(products_bronze_path)
        )
        logger.success(f"✅ Đã ghi Bronze Products tới {products_bronze_path} ({df_products.count()} rows)")
    except Exception as e:
        logger.warning(f"Không thể xử lý Products (Có thể chưa có file raw nào): {e}")

    # 2. Ingest Reviews
    logger.info(f"Đang đọc Raw Reviews từ: {reviews_raw_path}")
    try:
        df_reviews = spark.read.json(reviews_raw_path)
        
        (
            df_reviews.write
            .format("delta")
            .mode("overwrite")
            .save(reviews_bronze_path)
        )
        logger.success(f"✅ Đã ghi Bronze Reviews tới {reviews_bronze_path} ({df_reviews.count()} rows)")
    except Exception as e:
        logger.warning(f"Không thể xử lý Reviews (Có thể chưa có file raw nào): {e}")
        
    spark.stop()

if __name__ == "__main__":
    run_bronze_ingestion()
