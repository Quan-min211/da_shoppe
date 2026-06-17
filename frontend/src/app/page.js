"use client";

import { useEffect, useState } from "react";
import { Package, DollarSign, Star, MessageSquare } from "lucide-react";
import KpiCard from "@/components/KpiCard";
import RatingChart from "@/components/RatingChart";
import TopProductsTable from "@/components/TopProductsTable";
import { getOverview, getRatingDistribution, getTopProducts } from "@/lib/api";

export default function OverviewPage() {
  const [overview, setOverview] = useState(null);
  const [ratingDist, setRatingDist] = useState(null);
  const [topProducts, setTopProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const [ov, rd, tp] = await Promise.all([
          getOverview(),
          getRatingDistribution(),
          getTopProducts("avg_rating", 5),
        ]);
        setOverview(ov);
        setRatingDist(rd);
        setTopProducts(tp);
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
        <div className="text-center space-y-4">
          <div className="w-16 h-16 mx-auto rounded-full bg-red-500/10 flex items-center justify-center">
            <span className="text-3xl">⚠️</span>
          </div>
          <h2 className="text-xl font-semibold text-white">Không thể kết nối API</h2>
          <p className="text-slate-400 text-sm max-w-md">
            Hãy đảm bảo Backend API đang chạy tại{" "}
            <code className="text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded">localhost:8000</code>
          </p>
          <p className="text-xs text-red-400">{error}</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="space-y-8">
        <div className="space-y-2">
          <div className="skeleton h-8 w-48" />
          <div className="skeleton h-4 w-72" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton h-32 rounded-2xl" />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="skeleton h-80 rounded-2xl" />
          <div className="skeleton h-80 rounded-2xl" />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Dashboard Overview</h1>
        <p className="text-slate-400 mt-1">Tổng quan dữ liệu thương mại điện tử Shopee</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 stagger-children">
        <KpiCard
          title="Tổng sản phẩm"
          value={overview?.total_products?.toLocaleString("vi-VN") || "0"}
          subtitle="Trong cơ sở dữ liệu"
          icon={Package}
          color="indigo"
        />
        <KpiCard
          title="Giá trung bình"
          value={`₫${(overview?.avg_price || 0).toLocaleString("vi-VN")}`}
          subtitle="Trên tất cả sản phẩm"
          icon={DollarSign}
          color="emerald"
        />
        <KpiCard
          title="Rating trung bình"
          value={`${(overview?.avg_rating || 0).toFixed(1)} ⭐`}
          subtitle="Điểm đánh giá trung bình"
          icon={Star}
          color="amber"
        />
        <KpiCard
          title="Tổng đánh giá"
          value={(overview?.total_reviews || 0).toLocaleString("vi-VN")}
          subtitle="Lượt review từ người dùng"
          icon={MessageSquare}
          color="rose"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RatingChart data={ratingDist} height={280} />
        <TopProductsTable products={topProducts} title="🏆 Top 5 sản phẩm (Rating)" />
      </div>
    </div>
  );
}
