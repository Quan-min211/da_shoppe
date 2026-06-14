"""
Ingestion từ Raw JSONL (Local Storage) vào Bronze Layer (Delta Lake).
Đọc toàn bộ file jsonl trong data/raw/ bằng Python thuần (bypass Hadoop NativeIO)
rồi tạo Spark DataFrame và lưu vào data/bronze/ dưới định dạng Delta.
"""

import json
import sys
from pathlib import Path
from loguru import logger

# Thêm root_dir vào sys.path để có thể import từ processing.utils
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from processing.utils.spark_session import get_spark_session


def read_jsonl_to_strings(directory: Path) -> list[str]:
    """
    Đọc tất cả file .jsonl trong thư mục (đệ quy) bằng Python thuần.
    Trả về list các JSON string (mỗi dòng = 1 string).
    Hoàn toàn bypass Hadoop NativeIO — không bao giờ bị lỗi UnsatisfiedLinkError.
    """
    json_lines = []
    if not directory.exists():
        logger.warning(f"Thư mục không tồn tại: {directory}")
        return json_lines
    
    jsonl_files = list(directory.rglob("*.jsonl"))
    if not jsonl_files:
        logger.warning(f"Không tìm thấy file .jsonl nào trong: {directory}")
        return json_lines
    
    logger.info(f"Tìm thấy {len(jsonl_files)} file .jsonl trong {directory}")
    
    for file_path in jsonl_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        json_lines.append(line)
        except Exception as e:
            logger.warning(f"Không thể đọc file {file_path}: {e}")
    
    return json_lines


def run_bronze_ingestion():
    spark = get_spark_session("BronzeIngestion")
    
    # Đường dẫn
    raw_dir = project_root / "data" / "raw"
    bronze_dir = project_root / "data" / "bronze"
    
    products_raw_dir = raw_dir / "products"
    reviews_raw_dir = raw_dir / "reviews"
    
    products_bronze_path = str(bronze_dir / "products")
    reviews_bronze_path = str(bronze_dir / "reviews")
    
    # 1. Ingest Products
    logger.info(f"Đang đọc Raw Products từ: {products_raw_dir}")
    try:
        products_lines = read_jsonl_to_strings(products_raw_dir)
        if products_lines:
            # Tạo RDD từ JSON strings → dùng spark.read.json(rdd)
            # Cách này Spark tự infer schema chuẩn (xử lý null, mixed types tốt)
            rdd = spark.sparkContext.parallelize(products_lines)
            df_products = spark.read.json(rdd)
            (
                df_products.write
                .format("delta")
                .mode("overwrite")
                .save(products_bronze_path)
            )
            logger.success(f"✅ Đã ghi Bronze Products tới {products_bronze_path} ({df_products.count()} rows)")
        else:
            logger.warning("Không có dữ liệu Products raw để xử lý.")
    except Exception as e:
        logger.error(f"Lỗi khi xử lý Products: {e}")

    # 2. Ingest Reviews
    logger.info(f"Đang đọc Raw Reviews từ: {reviews_raw_dir}")
    try:
        reviews_lines = read_jsonl_to_strings(reviews_raw_dir)
        if reviews_lines:
            rdd = spark.sparkContext.parallelize(reviews_lines)
            df_reviews = spark.read.json(rdd)
            (
                df_reviews.write
                .format("delta")
                .mode("overwrite")
                .save(reviews_bronze_path)
            )
            logger.success(f"✅ Đã ghi Bronze Reviews tới {reviews_bronze_path} ({df_reviews.count()} rows)")
        else:
            logger.warning("Không có dữ liệu Reviews raw để xử lý.")
    except Exception as e:
        logger.error(f"Lỗi khi xử lý Reviews: {e}")
        
    spark.stop()
    logger.success("🎉 Bronze Ingestion hoàn tất!")

if __name__ == "__main__":
    run_bronze_ingestion()
