"""
Script tải winutils.exe và hadoop.dll (Hadoop 3.3.5) cho PySpark 3.5.x
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
    
    # URL phiên bản Hadoop 3.3.5 (Tương thích chuẩn nhất với PySpark 3.5.x)
    base_url = "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.3.5/bin/"
    files = ["winutils.exe", "hadoop.dll"]
    
    for f in files:
        file_path = bin_dir / f
        url = base_url + f
        logger.info(f"Đang tải {f} từ {url}...")
        try:
            # Ghi đè file cũ để đảm bảo không bị sót phiên bản lỗi
            urllib.request.urlretrieve(url, str(file_path))
            logger.success(f"Đã tải xong {f} vào {file_path}")
        except Exception as e:
            logger.error(f"Lỗi tải {f}: {e}")
                
    logger.info("Hoàn tất cài đặt winutils!")
    logger.info(f"Đường dẫn HADOOP_HOME của bạn là: {hadoop_home}")

if __name__ == "__main__":
    download_hadoop_winutils()
