"""
Utility functions to create and manage SparkSession for Delta Lake.
"""

import os
from pathlib import Path
from loguru import logger
from pyspark.sql import SparkSession

project_root = Path(__file__).resolve().parent.parent.parent

# Ép hệ thống dùng Java 17
os.environ["JAVA_HOME"] = r"C:\Program Files\Amazon Corretto\jdk17.0.19_10"
# Cấu hình HADOOP_HOME cho Windows
hadoop_home = str(project_root / "hadoop")
hadoop_bin = str(project_root / "hadoop" / "bin")
os.environ["HADOOP_HOME"] = hadoop_home
# QUAN TRỌNG: Thêm hadoop/bin vào PATH để JVM tìm thấy hadoop.dll
os.environ["PATH"] = hadoop_bin + ";" + os.environ.get("PATH", "")
# Sửa lỗi IP resolution
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
# Chỉ cho PySpark dùng đúng Python trong venv (tránh lỗi Microsoft Store alias trên Windows)
venv_python = str(project_root / ".venv" / "Scripts" / "python.exe")
os.environ["PYSPARK_PYTHON"] = venv_python
os.environ["PYSPARK_DRIVER_PYTHON"] = venv_python

def get_spark_session(app_name: str = "EcommerceDataLake") -> SparkSession:
    """Create or get a SparkSession with Delta Lake configurations."""
    logger.info(f"Khởi tạo SparkSession: {app_name}")
    
    spark = (
        SparkSession.builder.appName(app_name)
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.default.parallelism", "4")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.session.timeZone", "Asia/Ho_Chi_Minh")
        # Chỉ cho JVM biết đường dẫn tới native library (hadoop.dll)
        .config("spark.driver.extraLibraryPath", hadoop_bin)
        .getOrCreate()
    )
    
    spark.sparkContext.setLogLevel("ERROR")
    return spark
