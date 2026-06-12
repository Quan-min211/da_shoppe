"""
Lớp Silver: Đọc Reviews từ Bronze, làm sạch dữ liệu, drop duplicates và ghi vào Silver.
"""

import sys
from pathlib import Path
from loguru import logger
from pyspark.sql.functions import col, to_timestamp, current_timestamp, regexp_replace

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from processing.utils.spark_session import get_spark_session


def clean_reviews():
    spark = get_spark_session("SilverReviewsCleansing")
    
    bronze_path = str(project_root / "data" / "bronze" / "reviews")
    silver_path = str(project_root / "data" / "silver" / "reviews")
    
    logger.info(f"Đang đọc Bronze Reviews từ: {bronze_path}")
    try:
        df = spark.read.format("delta").load(bronze_path)
    except Exception as e:
        logger.error(f"Không thể đọc Bronze data: {e}")
        return

    # 1. Drop duplicates dựa trên review_id
    df_clean = df.dropDuplicates(["review_id"])
    
    # 2. Xử lý text: Loại bỏ khoảng trắng thừa, ký tự xuống dòng
    if "review_text" in df_clean.columns:
        df_clean = df_clean.withColumn("review_text", regexp_replace(col("review_text"), r"[\n\r]+", " "))
        
    # Xử lý timestamp
    if "created_at" in df_clean.columns:
        df_clean = df_clean.withColumn("created_at", to_timestamp("created_at"))
        
    if "scraped_at" in df_clean.columns:
        df_clean = df_clean.withColumn("scraped_at", to_timestamp("scraped_at"))
        
    # Thêm timestamp processing_time
    df_clean = df_clean.withColumn("processed_at", current_timestamp())

    # Ghi ra Silver
    logger.info(f"Ghi Silver Reviews tới: {silver_path}")
    (
        df_clean.write
        .format("delta")
        .mode("overwrite")
        .save(silver_path)
    )
    logger.success(f"✅ Đã ghi Silver Reviews ({df_clean.count()} rows)")
    
    # Hiển thị vài dòng
    df_clean.select("review_id", "product_id", "rating", "review_text").show(5, truncate=40)
    
    spark.stop()

if __name__ == "__main__":
    clean_reviews()
