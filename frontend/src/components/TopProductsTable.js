"use client";

import { Star } from "lucide-react";

export default function TopProductsTable({ products, title = "Top sản phẩm", onClickProduct }) {
  if (!products || products.length === 0) {
    return (
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
        <h3 className="text-base font-semibold text-[#1A1A2E] mb-4">{title}</h3>
        <p className="text-gray-400 text-sm">Chưa có dữ liệu.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
      <h3 className="text-base font-semibold text-[#1A1A2E] mb-4">{title}</h3>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-100">
              <th className="text-left text-[11px] font-medium text-gray-400 uppercase tracking-wider pb-3 pr-3">#</th>
              <th className="text-left text-[11px] font-medium text-gray-400 uppercase tracking-wider pb-3 pr-3">Sản phẩm</th>
              <th className="text-right text-[11px] font-medium text-gray-400 uppercase tracking-wider pb-3 pr-3">Giá</th>
              <th className="text-right text-[11px] font-medium text-gray-400 uppercase tracking-wider pb-3 pr-3">Rating</th>
              <th className="text-right text-[11px] font-medium text-gray-400 uppercase tracking-wider pb-3">Reviews</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {products.map((product, index) => (
              <tr
                key={product.product_id || index}
                onClick={() => onClickProduct && onClickProduct(product)}
                className={`hover:bg-[#7C5CFC]/[0.03] transition-colors duration-150 ${onClickProduct ? "cursor-pointer" : ""}`}
              >
                <td className="py-3 pr-3">
                  <span className={`text-xs font-bold ${
                    index === 0 ? "text-amber-500" : index === 1 ? "text-gray-400" : index === 2 ? "text-amber-700" : "text-gray-300"
                  }`}>
                    {index + 1}
                  </span>
                </td>
                <td className="py-3 pr-3">
                  <p className="text-sm text-[#1A1A2E] font-medium line-clamp-1 max-w-[200px]">
                    {product.name || "N/A"}
                  </p>
                  <p className="text-[11px] text-gray-400 mt-0.5">{product.shop_name || ""}</p>
                </td>
                <td className="py-3 pr-3 text-right">
                  <span className="text-sm text-emerald-600 font-semibold">
                    {product.price ? `₫${Number(product.price).toLocaleString("vi-VN")}` : "—"}
                  </span>
                </td>
                <td className="py-3 pr-3 text-right">
                  <div className="flex items-center justify-end gap-1">
                    <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
                    <span className="text-sm text-[#1A1A2E] font-medium">
                      {product.avg_rating ? Number(product.avg_rating).toFixed(1) : "0"}
                    </span>
                  </div>
                </td>
                <td className="py-3 text-right">
                  <span className="text-sm text-gray-500">{product.total_reviews || 0}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
