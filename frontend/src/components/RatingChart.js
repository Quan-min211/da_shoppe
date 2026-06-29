"use client";

import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from "recharts";

const COLORS = ["#EF4444", "#F97316", "#EAB308", "#22C55E", "#7C5CFC"];
const LABELS = ["1 ⭐", "2 ⭐", "3 ⭐", "4 ⭐", "5 ⭐"];

export default function RatingChart({ data, height = 280, title = "Phân bố đánh giá", onBarClick }) {
  if (!data) return null;

  const chartData = [
    { name: LABELS[0], value: data.star_1 || 0 },
    { name: LABELS[1], value: data.star_2 || 0 },
    { name: LABELS[2], value: data.star_3 || 0 },
    { name: LABELS[3], value: data.star_4 || 0 },
    { name: LABELS[4], value: data.star_5 || 0 },
  ];

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-[#1A1A2E]">{title}</h3>
        <span className="text-xs text-gray-400">Tổng: {data.total || 0}</span>
      </div>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={chartData} margin={{ top: 5, right: 10, left: -10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#F0F0F0" vertical={false} />
          <XAxis dataKey="name" tick={{ fill: "#6B7280", fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: "#9CA3AF", fontSize: 11 }} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#FFFFFF",
              border: "1px solid #E5E7EB",
              borderRadius: "12px",
              color: "#1A1A2E",
              boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
            }}
            cursor={{ fill: "rgba(124, 92, 252, 0.06)" }}
          />
          <Bar 
            dataKey="value" 
            radius={[8, 8, 0, 0]} 
            maxBarSize={48}
            cursor={onBarClick ? "pointer" : "default"}
            onClick={(data, index) => onBarClick && onBarClick(index + 1)}
          >
            {chartData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
