"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

const COLORS = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#6366f1"];
const LABELS = ["1 ⭐", "2 ⭐", "3 ⭐", "4 ⭐", "5 ⭐"];

export default function RatingChart({ data, height = 300 }) {
  if (!data) return null;

  const chartData = [
    { name: LABELS[0], value: data.star_1 || 0 },
    { name: LABELS[1], value: data.star_2 || 0 },
    { name: LABELS[2], value: data.star_3 || 0 },
    { name: LABELS[3], value: data.star_4 || 0 },
    { name: LABELS[4], value: data.star_5 || 0 },
  ];

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/30 p-6 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-white mb-4">Phân bố đánh giá</h3>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 13 }} />
          <YAxis tick={{ fill: "#94a3b8", fontSize: 12 }} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#1e293b",
              border: "1px solid #475569",
              borderRadius: "12px",
              color: "#f1f5f9",
            }}
            cursor={{ fill: "rgba(99, 102, 241, 0.1)" }}
          />
          <Bar dataKey="value" radius={[8, 8, 0, 0]} maxBarSize={60}>
            {chartData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <p className="text-center text-sm text-slate-500 mt-2">
        Tổng: {data.total || 0} đánh giá
      </p>
    </div>
  );
}
