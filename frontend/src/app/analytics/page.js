"use client";

import { useEffect, useState } from "react";
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
import { getRatingDistribution, getTopProducts } from "@/lib/api";
import RatingChart from "@/components/RatingChart";

export default function AnalyticsPage() {
  const [ratingDist, setRatingDist] = useState(null);
  const [topByRating, setTopByRating] = useState([]);
  const [topByReviews, setTopByReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const [rd, tr, tv] = await Promise.all([
          getRatingDistribution(),
          getTopProducts("avg_rating", 10),
          getTopProducts("total_reviews", 10),
        ]);
        setRatingDist(rd);
        setTopByRating(tr);
        setTopByReviews(tv);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

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

  if (loading) {
    return (
      <div className="space-y-8">
        <div className="skeleton h-8 w-48" />
        <div className="skeleton h-80 rounded-2xl" />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="skeleton h-96 rounded-2xl" />
          <div className="skeleton h-96 rounded-2xl" />
        </div>
      </div>
    );
  }

  // Prepare horizontal bar chart data
  const ratingChartData = topByRating
    .map((p) => ({
      name: (p.name || "").slice(0, 25) + ((p.name || "").length > 25 ? "..." : ""),
      avg_rating: Number(p.avg_rating || 0).toFixed(1),
      fullName: p.name,
    }))
    .reverse();

  const reviewsChartData = topByReviews
    .map((p) => ({
      name: (p.name || "").slice(0, 25) + ((p.name || "").length > 25 ? "..." : ""),
      total_reviews: p.total_reviews || 0,
      fullName: p.name,
    }))
    .reverse();

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-800 border border-slate-600 rounded-xl p-3 shadow-xl">
          <p className="text-sm text-white font-medium">{payload[0].payload.fullName}</p>
          <p className="text-sm text-indigo-400 mt-1">
            {payload[0].name === "avg_rating" ? "Rating: " : "Reviews: "}
            <span className="font-bold">{payload[0].value}</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Analytics</h1>
        <p className="text-slate-400 mt-1">Phân tích chuyên sâu dữ liệu sản phẩm Shopee</p>
      </div>

      {/* Rating Distribution */}
      <RatingChart data={ratingDist} height={320} />

      {/* Two Column Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top by Rating */}
        <div className="rounded-2xl bg-slate-800/50 border border-slate-700/30 p-6 backdrop-blur-sm">
          <h3 className="text-lg font-semibold text-white mb-4">
            ⭐ Top 10 — Rating cao nhất
          </h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={ratingChartData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
              <XAxis type="number" domain={[0, 5]} tick={{ fill: "#94a3b8", fontSize: 12 }} />
              <YAxis type="category" dataKey="name" width={150} tick={{ fill: "#94a3b8", fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="avg_rating" radius={[0, 6, 6, 0]} maxBarSize={24}>
                {ratingChartData.map((_, i) => (
                  <Cell key={i} fill={`hsl(${250 + i * 8}, 70%, ${55 + i * 2}%)`} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Top by Reviews */}
        <div className="rounded-2xl bg-slate-800/50 border border-slate-700/30 p-6 backdrop-blur-sm">
          <h3 className="text-lg font-semibold text-white mb-4">
            💬 Top 10 — Nhiều Reviews nhất
          </h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={reviewsChartData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
              <XAxis type="number" tick={{ fill: "#94a3b8", fontSize: 12 }} />
              <YAxis type="category" dataKey="name" width={150} tick={{ fill: "#94a3b8", fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="total_reviews" radius={[0, 6, 6, 0]} maxBarSize={24}>
                {reviewsChartData.map((_, i) => (
                  <Cell key={i} fill={`hsl(${160 + i * 8}, 65%, ${45 + i * 2}%)`} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
