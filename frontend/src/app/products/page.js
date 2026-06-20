"use client";

import { useEffect, useState, useCallback } from "react";
import { Search, ChevronLeft, ChevronRight, Star, ArrowUpDown, Eye, MessageSquare } from "lucide-react";
import { getProducts } from "@/lib/api";
import ProductModal from "@/components/ProductModal";
import ReviewsModal from "@/components/ReviewsModal";

const SortHeader = ({ column, children, align = "left", sortBy, handleSort }) => (
  <th
    onClick={() => handleSort(column)}
    className={`text-${align} text-[11px] font-medium text-gray-400 uppercase tracking-wider pb-4 px-3 cursor-pointer hover:text-[#7C5CFC] transition-colors select-none`}
  >
    <div className={`flex items-center gap-1 ${align === "right" ? "justify-end" : ""}`}>
      {children}
      <ArrowUpDown className={`w-3 h-3 ${sortBy === column ? "text-[#7C5CFC]" : ""}`} />
    </div>
  </th>
);

export default function ProductsPage() {
  const [data, setData] = useState({ data: [], total: 0, page: 1, page_size: 15, total_pages: 0 });
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("avg_rating");
  const [sortOrder, setSortOrder] = useState("desc");
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modals
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [reviewsTarget, setReviewsTarget] = useState(null);

  useEffect(() => {
    let ignore = false;
    async function fetchData() {
      setLoading(true);
      try {
        const result = await getProducts({ page, pageSize: 15, search, sortBy, sortOrder });
        if (!ignore) {
          setData(result);
          setLoading(false);
        }
      } catch (err) {
        if (!ignore) {
          setError(err.message);
          setLoading(false);
        }
      }
    }
    fetchData();
    return () => { ignore = true; };
  }, [page, search, sortBy, sortOrder]);

  useEffect(() => {
    const timer = setTimeout(() => setPage(1), 300);
    return () => clearTimeout(timer);
  }, [search]);

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === "desc" ? "asc" : "desc");
    } else {
      setSortBy(column);
      setSortOrder("desc");
    }
    setPage(1);
  };


  if (error) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="text-center space-y-3">
          <span className="text-4xl">⚠️</span>
          <p className="text-[#1A1A2E] font-semibold">Không thể tải dữ liệu</p>
          <p className="text-sm text-red-400">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-6 animate-fade-in">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-[#1A1A2E] tracking-tight">Products</h1>
            <p className="text-gray-500 mt-1 text-sm">{data.total} sản phẩm trong cơ sở dữ liệu</p>
          </div>
          <div className="relative w-full sm:w-80">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Tìm kiếm sản phẩm..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-[#1A1A2E] placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#7C5CFC]/30 focus:border-[#7C5CFC]/30 transition-all shadow-sm"
            />
          </div>
        </div>

        {/* Table */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left text-[11px] font-medium text-gray-400 uppercase tracking-wider pb-4 pl-5 pr-2 pt-4 w-12">#</th>
                  <SortHeader column="name" sortBy={sortBy} handleSort={handleSort}>Sản phẩm</SortHeader>
                  <SortHeader column="price" align="right" sortBy={sortBy} handleSort={handleSort}>Giá</SortHeader>
                  <SortHeader column="avg_rating" align="right" sortBy={sortBy} handleSort={handleSort}>Rating</SortHeader>
                  <SortHeader column="total_reviews" align="right" sortBy={sortBy} handleSort={handleSort}>Reviews</SortHeader>
                  <th className="text-left text-[11px] font-medium text-gray-400 uppercase tracking-wider pb-4 px-3 pt-4">Shop</th>
                  <th className="text-center text-[11px] font-medium text-gray-400 uppercase tracking-wider pb-4 px-3 pt-4">Hành động</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {loading
                  ? Array.from({ length: 8 }).map((_, i) => (
                      <tr key={i}>
                        <td colSpan={7} className="p-4"><div className="skeleton h-6 w-full" /></td>
                      </tr>
                    ))
                  : data.data.map((product, index) => (
                      <tr key={product.product_id || index} className="hover:bg-[#F5F5F0]/50 transition-colors duration-150">
                        <td className="pl-5 pr-2 py-3.5 text-sm text-gray-400 font-mono">
                          {(page - 1) * 15 + index + 1}
                        </td>
                        <td className="px-3 py-3.5">
                          <p className="text-sm text-[#1A1A2E] font-medium line-clamp-1 max-w-[280px]">
                            {product.name || "N/A"}
                          </p>
                        </td>
                        <td className="px-3 py-3.5 text-right">
                          <span className="text-sm text-emerald-600 font-semibold">
                            {product.price ? `₫${Number(product.price).toLocaleString("vi-VN")}` : "—"}
                          </span>
                        </td>
                        <td className="px-3 py-3.5 text-right">
                          <div className="flex items-center justify-end gap-1">
                            <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                            <span className="text-sm text-[#1A1A2E] font-medium">
                              {product.avg_rating ? Number(product.avg_rating).toFixed(1) : "0"}
                            </span>
                          </div>
                        </td>
                        <td className="px-3 py-3.5 text-right text-sm text-gray-500">
                          {product.total_reviews || 0}
                        </td>
                        <td className="px-3 py-3.5">
                          <span className="text-xs text-gray-400 bg-gray-50 px-2.5 py-1 rounded-lg border border-gray-100">
                            {product.shop_name || "N/A"}
                          </span>
                        </td>
                        <td className="px-3 py-3.5">
                          <div className="flex items-center justify-center gap-1.5">
                            <button
                              onClick={() => setSelectedProduct(product)}
                              title="Xem chi tiết"
                              className="w-8 h-8 rounded-lg bg-[#7C5CFC]/5 text-[#7C5CFC] flex items-center justify-center hover:bg-[#7C5CFC]/15 transition-colors"
                            >
                              <Eye className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => setReviewsTarget({ id: product.product_id, name: product.name })}
                              title="Xem bình luận"
                              className="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center hover:bg-amber-100 transition-colors"
                            >
                              <MessageSquare className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {data.total_pages > 1 && (
            <div className="flex items-center justify-between px-5 py-4 border-t border-gray-100">
              <p className="text-sm text-gray-400">
                Trang {data.page} / {data.total_pages}
              </p>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setPage(Math.max(1, page - 1))}
                  disabled={page === 1}
                  className="flex items-center gap-1 px-3 py-1.5 text-sm bg-white border border-gray-200 rounded-xl text-gray-500 hover:border-[#7C5CFC]/30 hover:text-[#7C5CFC] disabled:opacity-30 disabled:cursor-not-allowed transition-all"
                >
                  <ChevronLeft className="w-4 h-4" /> Trước
                </button>
                <button
                  onClick={() => setPage(Math.min(data.total_pages, page + 1))}
                  disabled={page >= data.total_pages}
                  className="flex items-center gap-1 px-3 py-1.5 text-sm bg-white border border-gray-200 rounded-xl text-gray-500 hover:border-[#7C5CFC]/30 hover:text-[#7C5CFC] disabled:opacity-30 disabled:cursor-not-allowed transition-all"
                >
                  Tiếp <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Modals */}
      {selectedProduct && (
        <ProductModal
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
          onViewReviews={(pid) => {
            setReviewsTarget({ id: pid, name: selectedProduct.name });
            setSelectedProduct(null);
          }}
        />
      )}
      {reviewsTarget && (
        <ReviewsModal
          productId={reviewsTarget.id}
          productName={reviewsTarget.name}
          onClose={() => setReviewsTarget(null)}
        />
      )}
    </>
  );
}
