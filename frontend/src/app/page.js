"use client";

import { useEffect, useState } from "react";
import { Package, DollarSign, Star, MessageSquare } from "lucide-react";
import KpiCard from "@/components/KpiCard";
import RatingChart from "@/components/RatingChart";
import SentimentChart from "@/components/SentimentChart";
import TopProductsTable from "@/components/TopProductsTable";
import ProductModal from "@/components/ProductModal";
import ReviewsModal from "@/components/ReviewsModal";
import { getOverview, getRatingDistribution, getTopProducts, getSentimentOverview } from "@/lib/api";

export default function OverviewPage() {
  const [overview, setOverview] = useState(null);
  const [ratingDist, setRatingDist] = useState(null);
  const [topProducts, setTopProducts] = useState([]);
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modals
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [reviewsTarget, setReviewsTarget] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const [ov, rd, tp, sm] = await Promise.all([
          getOverview(),
          getRatingDistribution(),
          getTopProducts("avg_rating", 5),
          getSentimentOverview(),
        ]);
        setOverview(ov);
        setRatingDist(rd);
        setTopProducts(tp);
        setSentiment(sm);
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
        <div className="text-center space-y-4 animate-fade-in">
          <div className="w-20 h-20 mx-auto rounded-2xl bg-red-50 flex items-center justify-center">
            <span className="text-4xl">⚠️</span>
          </div>
          <h2 className="text-xl font-bold text-[#1A1A2E]">Không thể kết nối API</h2>
          <p className="text-gray-500 text-sm max-w-md">
            Hãy đảm bảo Backend API đang chạy tại{" "}
            <code className="text-[#7C5CFC] bg-[#7C5CFC]/5 px-2 py-0.5 rounded-lg">localhost:8000</code>
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
          <div className="skeleton h-8 w-52" />
          <div className="skeleton h-4 w-80" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {[1, 2, 3, 4].map((i) => <div key={i} className="skeleton h-32 rounded-2xl" />)}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <div className="skeleton h-80 rounded-2xl" />
          <div className="skeleton h-80 rounded-2xl" />
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-6 animate-fade-in">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[#1A1A2E] tracking-tight">Dashboard Overview</h1>
            <p className="text-gray-500 mt-1 text-sm">Tổng quan dữ liệu thương mại điện tử Shopee</p>
          </div>
          <div className="text-xs text-gray-400 bg-white px-4 py-2 rounded-xl border border-gray-100">
            {new Date().toLocaleDateString("vi-VN", { day: "numeric", month: "long", year: "numeric" })}
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 stagger-children">
          <KpiCard
            title="Tổng sản phẩm"
            value={overview?.total_products?.toLocaleString("vi-VN") || "0"}
            icon={Package}
            color="purple"
          />
          <KpiCard
            title="Giá trung bình"
            value={`₫${(overview?.avg_price || 0).toLocaleString("vi-VN")}`}
            icon={DollarSign}
            color="green"
          />
          <KpiCard
            title="Rating trung bình"
            value={`${(overview?.avg_rating || 0).toFixed(1)} ⭐`}
            icon={Star}
            color="amber"
          />
          <KpiCard
            title="Tổng đánh giá"
            value={(overview?.total_reviews || 0).toLocaleString("vi-VN")}
            icon={MessageSquare}
            color="rose"
          />
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <RatingChart data={ratingDist} height={260} />
          <SentimentChart data={sentiment} />
          <TopProductsTable
            products={topProducts}
            title="🏆 Top 5 sản phẩm — Rating"
            onClickProduct={(p) => setSelectedProduct(p)}
          />
        </div>
      </div>

      {/* Product Detail Modal */}
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

      {/* Reviews Modal */}
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
