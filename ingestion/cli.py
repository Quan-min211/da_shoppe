"""
CLI Entry Point — Chạy scraper từ command line.

Usage:
    # Scrape 1 keyword
    python -m ingestion.cli scrape --keyword "bàn phím cơ" --pages 2

    # Scrape nhiều keywords từ file
    python -m ingestion.cli scrape --keywords-file keywords.txt --pages 1

    # Hiện thông tin settings
    python -m ingestion.cli info
"""

import argparse
import sys
from pathlib import Path

from loguru import logger

from ingestion.config import get_settings


def setup_logging(log_level: str = "INFO", log_dir: str = "./logs") -> None:
    """Cấu hình loguru logging.

    Output:
        - Console: colored, human-readable
        - File: JSON format, rotated daily
    """
    # Remove default handler
    logger.remove()

    # Console handler — colored output
    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{extra[platform]:>7}</cyan> | "
            "<level>{message}</level>"
        ),
        filter=lambda record: "platform" in record["extra"],
    )

    # Fallback console handler — for messages without platform
    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<level>{message}</level>"
        ),
        filter=lambda record: "platform" not in record["extra"],
    )

    # File handler — JSON format, daily rotation
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_path / "scraper_{time:YYYY-MM-DD}.log",
        level="DEBUG",
        rotation="1 day",
        retention="7 days",
        encoding="utf-8",
        serialize=True,  # JSON format
    )


def cmd_scrape(args: argparse.Namespace) -> None:
    """Thực thi lệnh scrape."""
    from ingestion.scrapers.shopee_scraper import ShopeeScraper
    from ingestion.writers.jsonl_writer import JsonlWriter

    settings = get_settings()

    # Determine keywords
    keywords: list[str] = []
    if args.keyword:
        keywords = [args.keyword]
    elif args.keywords_file:
        kf = Path(args.keywords_file)
        if not kf.exists():
            logger.error(f"❌ File không tồn tại: {kf}")
            sys.exit(1)
        keywords = [
            line.strip()
            for line in kf.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    else:
        logger.error("❌ Phải cung cấp --keyword hoặc --keywords-file")
        sys.exit(1)

    if not keywords:
        logger.error("❌ Không có keyword nào để scrape")
        sys.exit(1)

    max_pages = args.pages or settings.MAX_PAGES_PER_KEYWORD

    logger.info(f"🚀 Bắt đầu scrape {len(keywords)} keywords, max {max_pages} pages/keyword")

    # Init writer
    writer = JsonlWriter(base_dir=settings.RAW_DATA_DIR, data_type="products")

    # Run scraper
    with ShopeeScraper() as scraper:
        if len(keywords) == 1:
            products = scraper.scrape_products(keywords[0], max_pages=max_pages)
            if products:
                output_path = writer.write(products, keyword=keywords[0])
                logger.success(f"📁 Output: {output_path}")
            else:
                logger.warning("⚠️ Không thu thập được sản phẩm nào")
        else:
            results = scraper.scrape_multiple_keywords(keywords, max_pages=max_pages)
            output_files = writer.write_multiple(results)
            logger.success(f"📁 Đã ghi {len(output_files)} files")

    logger.info("🏁 Hoàn tất!")


def cmd_info(args: argparse.Namespace) -> None:
    """Hiện thông tin settings."""
    settings = get_settings()
    print("\n📋 Current Settings:")
    print(f"  Chrome CDP URL:    {settings.CHROME_CDP_URL}")
    print(f"  Request Delay:     {settings.REQUEST_DELAY_SECONDS}s")
    print(f"  Max Pages/Keyword: {settings.MAX_PAGES_PER_KEYWORD}")
    print(f"  Data Directory:    {settings.RAW_DATA_DIR}")
    print(f"  Log Level:         {settings.LOG_LEVEL}")
    print(f"  Log Directory:     {settings.LOG_DIR}")
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="ingestion",
        description="🛒 Vietnam E-Commerce Data Ingestion Tool",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # === scrape command ===
    scrape_parser = subparsers.add_parser("scrape", help="Scrape sản phẩm từ Shopee")
    scrape_parser.add_argument(
        "--keyword", "-k",
        type=str,
        help="Keyword tìm kiếm (VD: 'bàn phím cơ')",
    )
    scrape_parser.add_argument(
        "--keywords-file", "-f",
        type=str,
        help="File chứa danh sách keywords (1 keyword/dòng)",
    )
    scrape_parser.add_argument(
        "--pages", "-p",
        type=int,
        default=None,
        help="Số trang tối đa per keyword (default: from settings)",
    )
    scrape_parser.set_defaults(func=cmd_scrape)

    # === info command ===
    info_parser = subparsers.add_parser("info", help="Hiện thông tin settings")
    info_parser.set_defaults(func=cmd_info)

    # Parse
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Setup logging
    settings = get_settings()
    setup_logging(log_level=settings.LOG_LEVEL, log_dir=settings.LOG_DIR)

    # Execute command
    args.func(args)


if __name__ == "__main__":
    main()
