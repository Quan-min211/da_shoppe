"""
JSON Lines Writer — Lưu data scraping vào JSONL files.

Output format: 1 JSON object per line (JSONL / JSON Lines)
- Dễ đọc, dễ append, dễ import vào Spark/Pandas
- Partitioned theo ngày: data/raw/products/2024-01-15/products_143022.jsonl

Sau khi có Kafka (Phase 2), writer này vẫn hữu ích cho:
- Backup / archival
- Development & debugging
- Data replay
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger


class JsonlWriter:
    """Ghi data ra JSON Lines files, partitioned theo ngày.

    Args:
        base_dir: Thư mục gốc lưu data (default: data/raw)
        data_type: Loại data (products / reviews / ...) — dùng làm subdirectory

    Output path:
        {base_dir}/{data_type}/{YYYY-MM-DD}/{data_type}_{HHmmss}.jsonl
    """

    def __init__(self, base_dir: str = "data/raw", data_type: str = "products"):
        self.base_dir = Path(base_dir)
        self.data_type = data_type
        self.logger = logger.bind(writer="jsonl", data_type=data_type)

    def _get_output_path(self) -> Path:
        """Tạo output path partitioned theo ngày.

        Returns:
            Path object: data/raw/products/2024-01-15/products_143022.jsonl
        """
        now = datetime.now()
        date_partition = now.strftime("%Y-%m-%d")
        filename = f"{self.data_type}_{now.strftime('%H%M%S')}.jsonl"

        output_dir = self.base_dir / self.data_type / date_partition
        output_dir.mkdir(parents=True, exist_ok=True)

        return output_dir / filename

    def write(self, records: list[dict[str, Any]], keyword: str | None = None) -> Path:
        """Ghi danh sách records ra JSONL file.

        Args:
            records: List of dicts (đã validate bằng Pydantic)
            keyword: Keyword tìm kiếm (metadata)

        Returns:
            Path tới file đã ghi
        """
        if not records:
            self.logger.warning("Không có records để ghi")
            return None

        output_path = self._get_output_path()

        # Serialize datetime objects
        def json_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        with open(output_path, "w", encoding="utf-8") as f:
            for record in records:
                # Thêm metadata
                if keyword and "keyword" not in record:
                    record["keyword"] = keyword

                line = json.dumps(record, ensure_ascii=False, default=json_serializer)
                f.write(line + "\n")

        file_size_kb = output_path.stat().st_size / 1024
        self.logger.success(
            f"💾 Đã ghi {len(records)} records → {output_path} ({file_size_kb:.1f} KB)"
        )

        return output_path

    def write_multiple(
        self, keyword_results: dict[str, list[dict[str, Any]]]
    ) -> list[Path]:
        """Ghi kết quả từ nhiều keywords.

        Args:
            keyword_results: Dict mapping keyword → list of product dicts

        Returns:
            List of output file paths
        """
        output_files = []

        for keyword, records in keyword_results.items():
            path = self.write(records, keyword=keyword)
            if path:
                output_files.append(path)

        self.logger.success(f"📁 Đã ghi tổng cộng {len(output_files)} files")
        return output_files

    def read(self, file_path: str | Path) -> list[dict[str, Any]]:
        """Đọc lại JSONL file (utility method cho testing/debugging).

        Args:
            file_path: Path tới JSONL file

        Returns:
            List of dicts
        """
        records = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records
