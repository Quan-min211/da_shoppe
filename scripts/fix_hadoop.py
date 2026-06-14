import os
from pathlib import Path

def fix_hadoop_dll():
    project_root = Path(__file__).resolve().parent.parent
    hadoop_dll = project_root / "hadoop" / "bin" / "hadoop.dll"
    
    if hadoop_dll.exists():
        try:
            hadoop_dll.unlink()
            print("✅ Đã XÓA THÀNH CÔNG file hadoop.dll gây lỗi treo máy!")
        except Exception as e:
            print(f"❌ Không thể xóa file: {e}. Vui lòng tự vào {hadoop_dll} để xóa bằng tay.")
    else:
        print("✅ File hadoop.dll đã được xóa từ trước, hệ thống đã sạch sẽ!")

if __name__ == "__main__":
    fix_hadoop_dll()
