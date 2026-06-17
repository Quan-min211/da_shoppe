"use client";

import { Star } from "lucide-react";

export default function TopProductsTable({ products, title = "Top sản phẩm" }) {
  if (!products || products.length === 0) {
    return (
      <div className="rounded-2xl bg-slate-800/50 border border-slate-700/30 p-6">
        <h3 className="text-lg font-semibold text-white mb-4">{title}</h3>
        <p className="text-slate-500 text-sm">Chưa có dữ liệu.</p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/30 p-6 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-white mb-4">{title}</h3>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-700/50">
              <th className="text-left text-xs font-medium text-slate-400 uppercase tracking-wider pb-3 pr-4">
                #
              </th>
              <th className="text-left text-xs font-medium text-slate-400 uppercase tracking-wider pb-3 pr-4">
                Sản phẩm
              </th>
              <th className="text-right text-xs font-medium text-slate-400 uppercase tracking-wider pb-3 pr-4">
                Giá
              </th>
              <th className="text-right text-xs font-medium text-slate-400 uppercase tracking-wider pb-3 pr-4">
                Rating
              </th>
              <th className="text-right text-xs font-medium text-slate-400 uppercase tracking-wider pb-3">
                Reviews
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/30">
            {products.map((product, index) => (
              <tr
                key={product.product_id || index}
                className="hover:bg-slate-700/20 transition-colors duration-150"
              >
                <td className="py-3 pr-4">
                  <span className={`text-sm font-bold ${
                    index === 0 ? "text-amber-400" : 
                    index === 1 ? "text-slate-300" : 
                    index === 2 ? "text-amber-600" : "text-slate-500"
                  }`}>
                    {index + 1}
                  </span>
                </td>
                <td className="py-3 pr-4">
                  <p className="text-sm text-slate-200 font-medium line-clamp-1 max-w-xs">
                    {product.name || "N/A"}
                  </p>
                  <p className="text-xs text-slate-500 mt-0.5">
                    {product.shop_name || ""}
                  </p>
                </td>
                <td className="py-3 pr-4 text-right">
                  <span className="text-sm text-emerald-400 font-semibold">
                    {product.price
                      ? `₫${Number(product.price).toLocaleString("vi-VN")}`
                      : "N/A"}
                  </span>
                </td>
                <td className="py-3 pr-4 text-right">
                  <div className="flex items-center justify-end gap-1">
                    <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                    <span className="text-sm text-white font-medium">
                      {product.avg_rating ? Number(product.avg_rating).toFixed(1) : "0"}
                    </span>
                  </div>
                </td>
                <td className="py-3 text-right">
                  <span className="text-sm text-slate-300">
                    {product.total_reviews || 0}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
