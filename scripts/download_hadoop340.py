"""
Script tải winutils.exe và hadoop.dll cho Hadoop 3.4.0 (Phiên bản tương thích với PySpark 3.5.1 / Hadoop Client 3.4.2)
"""
import os
import urllib.request
from pathlib import Path
from loguru import logger

def download_hadoop_winutils():
    project_root = Path(__file__).resolve().parent.parent
    hadoop_home = project_root / "hadoop"
    bin_dir = hadoop_home / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    # Sử dụng repo kontext-tech có chứa bản build cho Hadoop 3.4.0!
    base_url = "https://raw.githubusercontent.com/kontext-tech/winutils/master/hadoop-3.4.0/bin/"
    files = ["winutils.exe", "hadoop.dll"]
    
    for f in files:
        file_path = bin_dir / f
        url = base_url + f
        logger.info(f"Đang tải {f} từ {url}...")
        try:
            # Ghi đè file cũ
            urllib.request.urlretrieve(url, str(file_path))
            logger.success(f"Đã tải xong {f} vào {file_path}")
        except Exception as e:
            logger.error(f"Lỗi tải {f}: {e}")
                
    logger.info("Hoàn tất cài đặt winutils!")
    logger.info(f"Đường dẫn HADOOP_HOME của bạn là: {hadoop_home}")

if __name__ == "__main__":
    download_hadoop_winutils()
