"""
Data Service: Đọc dữ liệu từ Gold/Silver Layer (Parquet files) bằng pandas.
Hoàn toàn không cần Spark/JVM — khởi động nhanh, nhẹ, ổn định.
"""

import pandas as pd
from pathlib import Path
from loguru import logger
from backend.app.config import GOLD_PRODUCT_METRICS_PATH, SILVER_REVIEWS_PATH


class DataService:
    """
    Singleton service đọc dữ liệu từ Parquet files và cache trong memory.
    Gọi load_data() một lần khi server khởi động, sau đó dùng lại.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance
    
    def load_data(self):
        """Đọc tất cả Parquet files từ Gold Layer vào memory."""
        if self._loaded:
            return
        
        logger.info("Đang load dữ liệu từ Gold Layer...")
        
        # Đọc Gold Product Metrics
        self.df_product_metrics = self._read_parquet_dir(GOLD_PRODUCT_METRICS_PATH)
        logger.info(f"  → Product Metrics: {len(self.df_product_metrics)} rows")
        
        # Đọc Silver Reviews (để có chi tiết review)
        self.df_reviews = self._read_parquet_dir(SILVER_REVIEWS_PATH)
        logger.info(f"  → Reviews: {len(self.df_reviews)} rows")
        
        self._loaded = True
        logger.success("✅ Dữ liệu đã được load vào memory!")
    
    def reload_data(self):
        """Force reload dữ liệu (gọi sau khi ETL pipeline chạy xong)."""
        self._loaded = False
        self.load_data()
    
    def _read_parquet_dir(self, directory: Path) -> pd.DataFrame:
        """Đọc tất cả file .parquet trong thư mục thành 1 DataFrame."""
        parquet_files = list(directory.glob("*.parquet"))
        if not parquet_files:
            logger.warning(f"Không tìm thấy file .parquet trong: {directory}")
            return pd.DataFrame()
        
        dfs = [pd.read_parquet(f) for f in parquet_files]
        return pd.concat(dfs, ignore_index=True)
    
    # === Product Queries ===
    
    def get_products(
        self, 
        page: int = 1, 
        page_size: int = 20, 
        search: str = None,
        sort_by: str = "avg_rating",
        sort_order: str = "desc"
    ) -> tuple[list[dict], int]:
        """Lấy danh sách sản phẩm có pagination, search, sort."""
        df = self.df_product_metrics.copy()
        
        # Search theo tên sản phẩm
        if search:
            df = df[df["name"].str.contains(search, case=False, na=False)]
        
        total = len(df)
        
        # Sort
        ascending = sort_order.lower() == "asc"
        if sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=ascending, na_position="last")
        
        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        df_page = df.iloc[start:end]
        
        # Convert to list of dicts, xử lý NaN
        records = df_page.where(df_page.notna(), None).to_dict(orient="records")
        return records, total
    
    def get_product_by_id(self, product_id: str) -> dict | None:
        """Lấy chi tiết 1 sản phẩm theo product_id."""
        df = self.df_product_metrics
        matches = df[df["product_id"] == product_id]
        if matches.empty:
            return None
        row = matches.iloc[0]
        return row.where(row.notna(), None).to_dict()
    
    # === Analytics Queries ===
    
    def get_overview(self) -> dict:
        """Tổng quan: tổng sản phẩm, giá trung bình, rating trung bình."""
        df = self.df_product_metrics
        return {
            "total_products": int(len(df)),
            "avg_price": round(float(df["price"].mean()), 0) if "price" in df.columns else 0,
            "avg_rating": round(float(df["avg_rating"].mean()), 2) if "avg_rating" in df.columns else 0,
            "total_reviews": int(df["total_reviews"].sum()) if "total_reviews" in df.columns else 0,
        }
    
    def get_top_products(
        self, 
        metric: str = "avg_rating", 
        limit: int = 10
    ) -> list[dict]:
        """Top N sản phẩm theo metric (avg_rating, total_reviews, sold_count)."""
        df = self.df_product_metrics.copy()
        
        if metric not in df.columns:
            metric = "avg_rating"
        
        # Lọc sản phẩm có ít nhất 1 review để ranking có ý nghĩa
        if "total_reviews" in df.columns:
            df = df[df["total_reviews"] > 0]
        
        df = df.sort_values(by=metric, ascending=False).head(limit)
        return df.where(df.notna(), None).to_dict(orient="records")
    
    def get_rating_distribution(self) -> dict:
        """Phân bố đánh giá (1-5 sao) trên toàn bộ sản phẩm."""
        df = self.df_product_metrics
        
        distribution = {}
        for star in range(1, 6):
            col_name = f"star_{star}_count"
            if col_name in df.columns:
                distribution[f"star_{star}"] = int(df[col_name].sum())
            else:
                distribution[f"star_{star}"] = 0
        
        total = sum(distribution.values())
        distribution["total"] = total
        
        return distribution


# Singleton instance
data_service = DataService()
