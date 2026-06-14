"""
Script tải winutils.exe và hadoop.dll phiên bản 3.3.5 (Tương thích chính xác với PySpark 3.5.x)
"""
import os
import urllib.request
from pathlib import Path

def download_hadoop_winutils():
    # Thư mục chứa winutils
    project_root = Path(__file__).resolve().parent.parent
    hadoop_home = project_root / "hadoop"
    bin_dir = hadoop_home / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    # URL tải winutils.exe và hadoop.dll CHUẨN cho Hadoop 3.3.5
    base_url = "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.3.5/bin/"
    files = ["winutils.exe", "hadoop.dll"]
    
    for f in files:
        file_path = bin_dir / f
        url = base_url + f
        print(f"Đang tải {f} từ {url}...")
        try:
            urllib.request.urlretrieve(url, str(file_path))
            print(f"✅ Đã tải xong {f} vào {file_path}")
        except Exception as e:
            print(f"❌ Lỗi tải {f}: {e}")
                
    print("🚀 Hoàn tất cài đặt bản chuẩn winutils 3.3.5!")

if __name__ == "__main__":
    download_hadoop_winutils()
