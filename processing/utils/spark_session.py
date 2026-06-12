"""
Utility functions to create and manage SparkSession for Delta Lake.
"""

from loguru import logger
from pyspark.sql import SparkSession


def get_spark_session(app_name: str = "EcommerceDataLake") -> SparkSession:
    """Create or get a SparkSession with Delta Lake configurations.

    Args:
        app_name: Name of the Spark application.

    Returns:
        SparkSession configured for Delta Lake.
    """
    logger.info(f"Khởi tạo SparkSession: {app_name}")
    
    # Delta Lake configuration
    # https://docs.delta.io/latest/quick-start.html#set-up-apache-spark-with-delta-lake
    
    spark = (
        SparkSession.builder.appName(app_name)
        # Packages
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.0.0")
        # SQL Extensions
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        # Catalog implementation
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        # Tuning cho local mode
        .config("spark.sql.shuffle.partitions", "4")  # Giảm số partitions khi chạy local
        .config("spark.default.parallelism", "4")
        .config("spark.driver.memory", "4g")
        # Khắc phục lỗi timezone warning
        .config("spark.sql.session.timeZone", "Asia/Ho_Chi_Minh")
        .getOrCreate()
    )
    
    # Đặt log level ERROR để bớt log rác từ Spark
    spark.sparkContext.setLogLevel("ERROR")
    
    return spark
