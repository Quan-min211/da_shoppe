"use client";

import {
  ScatterChart as RechartsScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ZAxis
} from "recharts";

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white border border-gray-200 rounded-xl p-3 shadow-lg max-w-[200px]">
        <p className="text-xs text-[#1A1A2E] font-medium line-clamp-2 mb-1">{data.name}</p>
        <p className="text-xs text-gray-500">Giá: <span className="font-bold text-emerald-600">₫{data.price?.toLocaleString("vi-VN")}</span></p>
        <p className="text-xs text-gray-500">Rating: <span className="font-bold text-amber-500">{data.rating} ⭐</span></p>
        <p className="text-xs text-gray-500">Reviews: <span className="font-bold text-[#7C5CFC]">{data.reviews}</span></p>
      </div>
    );
  }
  return null;
};

export default function ScatterChart({ data, height = 280, title = "Phân tán Giá vs Đánh giá" }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-[#1A1A2E]">{title}</h3>
      </div>
      <ResponsiveContainer width="100%" height={height}>
        <RechartsScatterChart margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#F0F0F0" />
          <XAxis 
            type="number" 
            dataKey="price" 
            name="Giá" 
            tickFormatter={(val) => `₫${(val/1000)}k`}
            tick={{ fill: "#6B7280", fontSize: 11 }} 
            axisLine={false} 
            tickLine={false}
          />
          <YAxis 
            type="number" 
            dataKey="rating" 
            name="Rating" 
            domain={[0, 5]} 
            tick={{ fill: "#9CA3AF", fontSize: 11 }} 
            axisLine={false} 
            tickLine={false}
          />
          <ZAxis type="number" dataKey="reviews" range={[20, 200]} name="Đánh giá" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<CustomTooltip />} />
          <Scatter name="Sản phẩm" data={data} fill="#7C5CFC" fillOpacity={0.6} />
        </RechartsScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
