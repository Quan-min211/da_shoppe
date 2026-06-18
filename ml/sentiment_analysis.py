"""
ML/NLP Sentiment Analysis — Phân tích cảm xúc Review tiếng Việt.

Đọc Silver Reviews (Parquet) bằng pandas, chạy underthesea.sentiment()
trên từng review, và lưu kết quả ra Gold Layer (Parquet).

Chạy: python -m ml.sentiment_analysis
"""

import sys
from pathlib import Path

import pandas as pd
from loguru import logger

project_root = Path(__file__).resolve().parent.parent

# Paths
SILVER_REVIEWS_PATH = project_root / "data" / "silver" / "reviews"
GOLD_SENTIMENT_PATH = project_root / "data" / "gold" / "reviews_sentiment"


def analyze_sentiment(text: str) -> dict:
    """
    Phân tích cảm xúc của 1 đoạn text tiếng Việt bằng underthesea.
    Trả về dict với sentiment_label và sentiment_score.
    """
    if not text or not isinstance(text, str) or text.strip() == "":
        return {"sentiment_label": "neutral", "sentiment_score": 0.0}

    try:
        from underthesea import sentiment

        result = sentiment(text)

        # underthesea.sentiment() trả về string: 'positive', 'negative', hoặc 'neutral'
        label = str(result).lower().strip()

        # Map label sang score
        score_map = {"positive": 1.0, "negative": -1.0, "neutral": 0.0}

        # Đôi khi underthesea trả về format khác
        if "positive" in label:
            final_label = "positive"
        elif "negative" in label:
            final_label = "negative"
        else:
            final_label = "neutral"

        return {
            "sentiment_label": final_label,
            "sentiment_score": score_map.get(final_label, 0.0),
        }
    except Exception as e:
        logger.warning(f"Lỗi sentiment analysis: {e}")
        return {"sentiment_label": "neutral", "sentiment_score": 0.0}


def run_sentiment_analysis():
    """Pipeline chính: đọc reviews → phân tích cảm xúc → lưu kết quả."""
    logger.info("🧠 Bắt đầu phân tích cảm xúc (Sentiment Analysis)...")

    # 1. Đọc Silver Reviews
    parquet_files = list(SILVER_REVIEWS_PATH.glob("*.parquet"))
    if not parquet_files:
        logger.error(f"Không tìm thấy file Parquet tại: {SILVER_REVIEWS_PATH}")
        return

    dfs = [pd.read_parquet(f) for f in parquet_files]
    df = pd.concat(dfs, ignore_index=True)
    logger.info(f"📄 Đã đọc {len(df)} reviews từ Silver Layer")
    logger.info(f"   Columns: {list(df.columns)}")

    # 2. Tìm cột chứa nội dung review
    text_col = None
    for col_name in ["review_text", "comment", "content", "text"]:
        if col_name in df.columns:
            text_col = col_name
            break

    if text_col is None:
        logger.error(f"Không tìm thấy cột review text. Các cột hiện có: {list(df.columns)}")
        return

    logger.info(f"   Sử dụng cột '{text_col}' để phân tích cảm xúc")

    # 3. Chạy sentiment analysis
    total = len(df)
    results = []

    for i, row in df.iterrows():
        text = row.get(text_col, "")
        result = analyze_sentiment(text)
        results.append(result)

        # Progress logging mỗi 10 reviews
        if (i + 1) % 10 == 0 or (i + 1) == total:
            logger.info(f"   Tiến độ: {i + 1}/{total} ({(i + 1) / total * 100:.0f}%)")

    # 4. Merge kết quả vào DataFrame
    sentiment_df = pd.DataFrame(results)
    df["sentiment_label"] = sentiment_df["sentiment_label"]
    df["sentiment_score"] = sentiment_df["sentiment_score"]

    # 5. Thống kê kết quả
    counts = df["sentiment_label"].value_counts()
    logger.info("📊 Kết quả phân tích:")
    for label, count in counts.items():
        pct = count / total * 100
        emoji = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}.get(label, "⚪")
        logger.info(f"   {emoji} {label}: {count} ({pct:.1f}%)")

    # 6. Lưu ra Gold Layer
    GOLD_SENTIMENT_PATH.mkdir(parents=True, exist_ok=True)
    output_file = GOLD_SENTIMENT_PATH / "reviews_sentiment.parquet"
    df.to_parquet(output_file, index=False)
    logger.success(f"✅ Đã lưu {len(df)} reviews với sentiment tại: {output_file}")


if __name__ == "__main__":
    run_sentiment_analysis()
