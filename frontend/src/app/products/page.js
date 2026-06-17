"use client";

import { useEffect, useState, useCallback } from "react";
import { Search, ChevronLeft, ChevronRight, Star, ArrowUpDown } from "lucide-react";
import { getProducts } from "@/lib/api";

export default function ProductsPage() {
  const [data, setData] = useState({ data: [], total: 0, page: 1, page_size: 15, total_pages: 0 });
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("avg_rating");
  const [sortOrder, setSortOrder] = useState("desc");
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProducts = useCallback(async () => {
    setLoading(true);
    try {
      const result = await getProducts({
        page,
        pageSize: 15,
        search,
        sortBy,
        sortOrder,
      });
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [page, search, sortBy, sortOrder]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      setPage(1);
    }, 300);
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

  const SortHeader = ({ column, children }) => (
    <th
      onClick={() => handleSort(column)}
      className="text-left text-xs font-medium text-slate-400 uppercase tracking-wider pb-4 pr-4 cursor-pointer hover:text-white transition-colors select-none"
    >
      <div className="flex items-center gap-1.5">
        {children}
        <ArrowUpDown className={`w-3 h-3 ${sortBy === column ? "text-indigo-400" : ""}`} />
      </div>
    </th>
  );

  if (error) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="text-center space-y-3">
          <span className="text-4xl">⚠️</span>
          <p className="text-white font-semibold">Không thể tải dữ liệu</p>
          <p className="text-sm text-red-400">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Products</h1>
          <p className="text-slate-400 mt-1">
            {data.total} sản phẩm trong cơ sở dữ liệu
          </p>
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-80">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Tìm kiếm sản phẩm..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-slate-800/50 border border-slate-700/50 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all"
          />
        </div>
      </div>

      {/* Table */}
      <div className="rounded-2xl bg-slate-800/50 border border-slate-700/30 backdrop-blur-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700/50 bg-slate-800/30">
                <th className="text-left text-xs font-medium text-slate-400 uppercase tracking-wider p-4 pr-2 w-12">
                  #
                </th>
                <SortHeader column="name">Sản phẩm</SortHeader>
                <SortHeader column="price">Giá</SortHeader>
                <SortHeader column="avg_rating">Rating</SortHeader>
                <SortHeader column="total_reviews">Reviews</SortHeader>
                <th className="text-left text-xs font-medium text-slate-400 uppercase tracking-wider pb-4 pr-4">
                  Shop
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/20">
              {loading
                ? Array.from({ length: 8 }).map((_, i) => (
                    <tr key={i}>
                      <td colSpan={6} className="p-4">
                        <div className="skeleton h-6 w-full" />
                      </td>
                    </tr>
                  ))
                : data.data.map((product, index) => (
                    <tr
                      key={product.product_id || index}
                      className="hover:bg-slate-700/20 transition-colors duration-150"
                    >
                      <td className="p-4 pr-2 text-sm text-slate-500 font-mono">
                        {(page - 1) * 15 + index + 1}
                      </td>
                      <td className="py-4 pr-4">
                        <p className="text-sm text-slate-200 font-medium line-clamp-1 max-w-sm">
                          {product.name || "N/A"}
                        </p>
                      </td>
                      <td className="py-4 pr-4">
                        <span className="text-sm text-emerald-400 font-semibold">
                          {product.price
                            ? `₫${Number(product.price).toLocaleString("vi-VN")}`
                            : "N/A"}
                        </span>
                      </td>
                      <td className="py-4 pr-4">
                        <div className="flex items-center gap-1">
                          <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                          <span className="text-sm text-white font-medium">
                            {product.avg_rating
                              ? Number(product.avg_rating).toFixed(1)
                              : "0"}
                          </span>
                        </div>
                      </td>
                      <td className="py-4 pr-4 text-sm text-slate-300">
                        {product.total_reviews || 0}
                      </td>
                      <td className="py-4 pr-4">
                        <span className="text-xs text-slate-400 bg-slate-700/30 px-2.5 py-1 rounded-lg">
                          {product.shop_name || "N/A"}
                        </span>
                      </td>
                    </tr>
                  ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {data.total_pages > 1 && (
          <div className="flex items-center justify-between p-4 border-t border-slate-700/30">
            <p className="text-sm text-slate-500">
              Trang {data.page} / {data.total_pages}
            </p>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
                className="flex items-center gap-1 px-3 py-1.5 text-sm bg-slate-700/50 border border-slate-600/50 rounded-lg text-slate-300 hover:bg-slate-600/50 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
              >
                <ChevronLeft className="w-4 h-4" /> Trước
              </button>
              <button
                onClick={() => setPage(Math.min(data.total_pages, page + 1))}
                disabled={page >= data.total_pages}
                className="flex items-center gap-1 px-3 py-1.5 text-sm bg-slate-700/50 border border-slate-600/50 rounded-lg text-slate-300 hover:bg-slate-600/50 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
              >
                Tiếp <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
