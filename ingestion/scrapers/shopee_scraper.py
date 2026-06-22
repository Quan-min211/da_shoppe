"""
Shopee Scraper — Thu thập dữ liệu sản phẩm từ Shopee.vn

Sử dụng Playwright CDP (Chrome DevTools Protocol) để:
1. Kết nối tới Chrome đang mở sẵn (có session đăng nhập)
2. Điều hướng tới trang tìm kiếm Shopee
3. Intercept API responses nội bộ (search_items, get_ratings)
4. Parse và validate data bằng Pydantic schemas

Cách dùng:
    # Mở Chrome trước: chrome.exe --remote-debugging-port=9222
    with ShopeeScraper() as scraper:
        products = scraper.scrape_products("bàn phím cơ", max_pages=2)
"""

import time
import threading
from typing import Any, Optional
from urllib.parse import quote

from loguru import logger
from playwright.sync_api import sync_playwright, Browser, Page, Response

from ingestion.scrapers.base_scraper import BaseScraper
from ingestion.schemas.product_schema import ProductSchema
from ingestion.schemas.review_schema import ReviewSchema
from ingestion.config import get_settings


class ShopeeScraper(BaseScraper):
    """Scraper cho Shopee.vn sử dụng Playwright CDP.

    Kết nối tới Chrome đã mở sẵn qua CDP port, intercept
    internal API responses để lấy dữ liệu sản phẩm.

    Attributes:
        cdp_url: URL kết nối CDP (default: http://localhost:9222)
        request_delay: Delay giữa các request (giây)
    """

    # Shopee API patterns để intercept
    API_SEARCH_ITEMS = "search_items"
    API_GET_ITEM = "item/get"
    API_GET_RATINGS = "get_ratings"

    def __init__(
        self,
        cdp_url: Optional[str] = None,
        request_delay: Optional[float] = None,
    ):
        super().__init__(platform="shopee")

        settings = get_settings()
        self.cdp_url = cdp_url or settings.CHROME_CDP_URL
        self.request_delay = request_delay or settings.REQUEST_DELAY_SECONDS

        # Playwright instances
        self._playwright = None
        self._browser: Optional[Browser] = None

        # Data collection buffer
        self._collected_items: list[dict] = []
        self._data_received = threading.Event()

    def connect(self) -> None:
        """Kết nối tới Chrome qua CDP.

        Chrome phải được mở sẵn với flag:
            chrome.exe --remote-debugging-port=9222
        """
        self.logger.info(f"Đang kết nối tới Chrome tại {self.cdp_url}...")

        self._playwright = sync_playwright().start()

        try:
            self._browser = self._playwright.chromium.connect_over_cdp(self.cdp_url)
            self.logger.success(f"✅ Đã kết nối thành công tới Chrome (CDP)")
        except Exception as e:
            self.logger.error(
                f"❌ Không thể kết nối tới Chrome tại {self.cdp_url}. "
                f"Hãy mở Chrome với: chrome.exe --remote-debugging-port=9222"
            )
            if self._playwright:
                self._playwright.stop()
            raise ConnectionError(f"Cannot connect to Chrome CDP: {e}") from e

    def close(self) -> None:
        """Đóng kết nối Playwright (không đóng Chrome)."""
        if self._playwright:
            self._playwright.stop()
            self._playwright = None
            self._browser = None
            self.logger.info("Đã đóng kết nối Playwright")

    def _handle_search_response(self, response: Response, keyword: str) -> None:
        """Callback xử lý API response từ Shopee search_items.

        Được gọi tự động khi page nhận response chứa search_items.
        Parse items và validate bằng ProductSchema.
        """
        if self.API_SEARCH_ITEMS not in response.url:
            return
        if response.status != 200:
            return

        try:
            data = response.json()
            items = data.get("items", [])

            if not items:
                return

            self.logger.info(f"📦 Intercepted {len(items)} items từ API search_items")

            for item_data in items:
                try:
                    product = ProductSchema.from_shopee_item(item_data, keyword=keyword)
                    self._collected_items.append(product.model_dump(mode="json"))
                except Exception as e:
                    self.logger.warning(f"⚠️ Skip item (validation failed): {e}")

            # Signal rằng đã nhận được data
            self._data_received.set()

        except Exception as e:
            self.logger.debug(f"Không thể parse response: {e}")

    def _handle_ratings_response(
        self, response: Response, shop_id: int, item_id: int, reviews_list: list, event: threading.Event
    ) -> None:
        """Callback xử lý API response từ Shopee get_ratings."""
        if self.API_GET_RATINGS not in response.url:
            return
        if response.status != 200:
            return

        try:
            data = response.json()
            ratings = data.get("data", {}).get("ratings")
            if not ratings:
                return

            for r in ratings:
                try:
                    review_obj = ReviewSchema.from_shopee_rating(r, item_id, shop_id)
                    reviews_list.append(review_obj.model_dump(mode="json"))
                except Exception as e:
                    self.logger.warning(f"⚠️ Skip review (validation failed): {e}")

            # Đã nhận được mẻ review đầu tiên (thường là 50 cái)
            event.set()

        except Exception as e:
            self.logger.debug(f"Không thể parse ratings response: {e}")

    def scrape_products(self, keyword: str, max_pages: int = 1) -> list[dict[str, Any]]:
        """Thu thập sản phẩm theo keyword từ Shopee.

        Args:
            keyword: Từ khóa tìm kiếm (VD: "bàn phím cơ")
            max_pages: Số trang tối đa cần crawl (mỗi trang ~60 items)

        Returns:
            List of product dicts (đã validate bằng ProductSchema)
        """
        if not self._browser:
            raise RuntimeError("Chưa kết nối. Gọi connect() trước hoặc dùng context manager.")

        self.logger.info(f"🔍 Bắt đầu scrape: keyword='{keyword}', max_pages={max_pages}")

        # Reset collection buffer
        self._collected_items = []

        context = self._browser.contexts[0]
        # Sử dụng tab có sẵn đầu tiên, hoặc tạo mới nếu chưa có
        page: Page = context.pages[0] if context.pages else context.new_page()

        # Gắn listener để intercept API responses (chỉ gắn 1 lần)
        page.on(
            "response",
            lambda resp, kw=keyword: self._handle_search_response(resp, kw),
        )

        for page_num in range(max_pages):
            self._data_received.clear()

            # Build search URL với pagination
            # Shopee dùng offset: page 0 → newest=0, page 1 → newest=60, ...
            offset = page_num * 60
            search_url = (
                f"https://shopee.vn/search?keyword={quote(keyword)}"
                f"&page={page_num}"
            )

            self.logger.info(
                f"📄 Trang {page_num + 1}/{max_pages}: {search_url}"
            )

            try:
                if page_num == 0:
                    self.logger.info("👉 Mô phỏng thao tác người dùng: Vào trang chủ và nhập từ khóa tìm kiếm...")
                    # Vào trang chủ
                    page.goto("https://shopee.vn/", wait_until="domcontentloaded", timeout=60000)
                    
                    self.logger.info("⏳ Đang dừng 60 giây để bạn xử lý Anti-bot hoặc Đăng nhập Shopee...")
                    page.wait_for_timeout(60000)
                    
                    try:
                        # Chờ ô tìm kiếm xuất hiện (thường là input có class shopee-searchbar-input__input)
                        page.wait_for_selector("input.shopee-searchbar-input__input", timeout=10000)
                        # Gõ từ khóa vào
                        page.fill("input.shopee-searchbar-input__input", keyword)
                        # Nhấn Enter để bắt đầu tìm kiếm
                        page.press("input.shopee-searchbar-input__input", "Enter")
                        
                        self.logger.info("⏳ Đang dừng thêm 60 giây để bạn gỡ Anti-bot sau khi tìm kiếm...")
                        page.wait_for_timeout(60000)
                    except Exception as e:
                        self.logger.warning(f"⚠️ Không tìm thấy ô tìm kiếm, chuyển qua URL tĩnh... {e}")
                        page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                else:
                    page.goto(search_url, wait_until="domcontentloaded", timeout=30000)

                # Chờ API response trả về (tối đa 15 giây)
                self._data_received.wait(timeout=15)

                if not self._data_received.is_set():
                    self.logger.warning(f"⏳ Timeout chờ API response trang {page_num + 1}")

                # Scroll xuống để trigger thêm API calls (lazy loading)
                self._scroll_page(page)

                # Chờ thêm chút để bắt hết API calls
                page.wait_for_timeout(3000)

            except Exception as e:
                self.logger.error(f"❌ Lỗi trang {page_num + 1}: {e}")
            # Bỏ page.close() để tái sử dụng tab này cho các trang tiếp theo

            # Rate limiting giữa các pages
            if page_num < max_pages - 1:
                self.logger.debug(f"⏱️ Delay {self.request_delay}s trước trang tiếp...")
                time.sleep(self.request_delay)

        self.logger.success(
            f"✅ Hoàn tất scrape '{keyword}': {len(self._collected_items)} sản phẩm"
        )

        return self._collected_items

    def _scroll_page(self, page: Page, scroll_count: int = 3) -> None:
        """Scroll trang xuống để trigger lazy-loading API calls.

        Args:
            page: Playwright page instance
            scroll_count: Số lần scroll
        """
        for i in range(scroll_count):
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            page.wait_for_timeout(1000)

    def scrape_multiple_keywords(
        self, keywords: list[str], max_pages: int = 1
    ) -> dict[str, list[dict[str, Any]]]:
        """Thu thập sản phẩm cho nhiều keywords.

        Args:
            keywords: Danh sách keywords
            max_pages: Số trang tối đa per keyword

        Returns:
            Dict mapping keyword → list of product dicts
        """
        results = {}
        total = len(keywords)

        for i, keyword in enumerate(keywords, 1):
            self.logger.info(f"📋 [{i}/{total}] Keyword: '{keyword}'")
            products = self.scrape_products(keyword, max_pages=max_pages)
            results[keyword] = products

            # Delay giữa các keywords
            if i < total:
                delay = self.request_delay * 2  # Longer delay giữa keywords
                self.logger.debug(f"⏱️ Delay {delay}s giữa keywords...")
                time.sleep(delay)

        total_products = sum(len(v) for v in results.values())
        self.logger.success(
            f"✅ Hoàn tất scrape {total} keywords: tổng {total_products} sản phẩm"
        )

        return results

    def scrape_reviews(self, shop_id: int, item_id: int, max_reviews: int = 100) -> list[dict[str, Any]]:
        """Thu thập danh sách đánh giá của một sản phẩm.

        Sử dụng Network Interception thay vì fetch() để qua mặt anti-bot Shopee.

        Args:
            shop_id: ID của shop
            item_id: ID của sản phẩm
            max_reviews: Số lượng đánh giá tối đa

        Returns:
            List of raw review dicts
        """
        if not self._browser:
            raise RuntimeError("Chưa kết nối. Gọi connect() trước.")

        self.logger.info(f"⭐ Bắt đầu scrape reviews: item_id={item_id}")
        
        context = self._browser.contexts[0]
        page = context.new_page()
        reviews = []
        event = threading.Event()
        
        # Gắn listener
        page.on(
            "response",
            lambda resp: self._handle_ratings_response(resp, shop_id, item_id, reviews, event),
        )
        
        product_url = f"https://shopee.vn/product/{shop_id}/{item_id}"
        
        try:
            page.goto(product_url, wait_until="domcontentloaded", timeout=30000)
            
            # Scroll xuống phần Đánh giá để kích hoạt API get_ratings
            for _ in range(5):
                page.evaluate("window.scrollBy(0, 1000)")
                page.wait_for_timeout(1000)
                if event.is_set():
                    break
                    
            event.wait(timeout=10)
            
        except Exception as e:
            self.logger.warning(f"Lỗi khi mở trang sản phẩm: {e}")
        finally:
            page.close()
            
        # Giới hạn số lượng
        final_reviews = reviews[:max_reviews]
        self.logger.success(f"✅ Đã cào {len(final_reviews)} reviews cho item {item_id}")
        return final_reviews

    def scrape_products_with_reviews(
        self, keyword: str, max_pages: int = 1, max_reviews: int = 100
    ) -> tuple[list[dict], list[dict]]:
        """Thu thập cả sản phẩm lẫn reviews cho sản phẩm đó.
        
        Returns:
            Tuple (danh sách products, danh sách tất cả reviews)
        """
        products = self.scrape_products(keyword, max_pages)
        all_reviews = []
        
        if not products:
            return products, all_reviews
            
        total = len(products)
        self.logger.info(f"🔄 Sẽ cào reviews cho {total} sản phẩm vừa tìm được...")
        
        for i, prod in enumerate(products, 1):
            shop_id = prod.get("shop_id")
            item_id = prod.get("product_id")
            
            if not shop_id or not item_id:
                continue
                
            self.logger.info(f"[{i}/{total}] Sản phẩm: {prod.get('name', '')[:30]}...")
            reviews = self.scrape_reviews(shop_id, item_id, max_reviews)
            all_reviews.extend(reviews)
            
            if i < total:
                time.sleep(self.request_delay)
                
        return products, all_reviews
