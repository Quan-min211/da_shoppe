from playwright.sync_api import sync_playwright

def fetch_shopee_products_playwright(keyword):
    print(f"Đang khởi động trình duyệt ảo để tìm kiếm: '{keyword}'...")
    
    with sync_playwright() as p:
        # Kết nối tới Chrome của bạn đang mở sẵn qua cổng 9222
        print("Đang kết nối tới Chrome của bạn...")
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print("❌ Lỗi: Không thể kết nối tới Chrome. Vui lòng đảm bảo bạn đã tắt hết Chrome và mở lại bằng lệnh đặc biệt (xem hướng dẫn).")
            return

        # Lấy context mặc định (phiên làm việc hiện tại của bạn)
        context = browser.contexts[0]
        
        # Mở một tab mới
        page = context.new_page()

        # Cờ để kiểm tra xem đã lấy được data chưa
        data_fetched = False

        # Hàm này sẽ "bắt rập" (intercept) các gói tin mạng (API) trả về
        def handle_response(response):
            nonlocal data_fetched
            # Nếu phát hiện API search_items và trạng thái OK (200)
            if "search_items" in response.url and response.status == 200:
                try:
                    data = response.json()
                    items = data.get("items", [])
                    if items and not data_fetched:
                        data_fetched = True
                        print(f"\n✅ Lấy thành công {len(items)} sản phẩm từ API ngầm:\n")
                        for item_data in items[:5]: # Chỉ in 5 sản phẩm đầu
                            item = item_data.get("item_basic", {})
                            name = item.get("name", "N/A")
                            # Giá của Shopee nhân với 100,000 nên cần chia lại
                            price = item.get("price", 0) / 100000
                            sold = item.get("historical_sold", 0)
                            
                            print(f"📦 Tên SP: {name}")
                            print(f"💰 Giá:   {price:,.0f} VNĐ")
                            print(f"🔥 Đã bán: {sold}")
                            print("-" * 50)
                except Exception:
                    pass

        # Gắn bộ lắng nghe mạng vào trang
        page.on("response", handle_response)

        # Điều khiển trình duyệt mở trang tìm kiếm của Shopee
        url = f"https://shopee.vn/search?keyword={keyword}"
        print(f"Đang truy cập: {url}")
        page.goto(url)
        
        # Chờ tối đa 10 giây để trang load xong dữ liệu
        page.wait_for_timeout(10000) 

        # Đóng cái tab (page) mình vừa mở thôi, đừng đóng cả Chrome (browser.close)
        page.close()

if __name__ == "__main__":
    fetch_shopee_products_playwright("bàn phím cơ")
