"use client";

import { LineChart, Line, ResponsiveContainer } from "recharts";

export default function KpiCard({ title, value, subtitle, icon: Icon, trend, color = "purple", sparklineData }) {
  const colorMap = {
    purple: { bg: "bg-white", iconBg: "bg-[#7C5CFC]/10", iconColor: "text-[#7C5CFC]", trendBg: "bg-[#7C5CFC]/10", trendColor: "text-[#7C5CFC]", stroke: "#7C5CFC" },
    green:  { bg: "bg-white", iconBg: "bg-emerald-50",    iconColor: "text-emerald-600", trendBg: "bg-emerald-50", trendColor: "text-emerald-600", stroke: "#059669" },
    amber:  { bg: "bg-white", iconBg: "bg-amber-50",      iconColor: "text-amber-600",   trendBg: "bg-amber-50",  trendColor: "text-amber-600", stroke: "#D97706" },
    rose:   { bg: "bg-white", iconBg: "bg-rose-50",       iconColor: "text-rose-600",    trendBg: "bg-rose-50",   trendColor: "text-rose-600", stroke: "#E11D48" },
  };

  const c = colorMap[color] || colorMap.purple;

  return (
    <div className={`${c.bg} rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-0.5 relative overflow-hidden group`}>
      <div className="flex items-start justify-between mb-2">
        <div className={`rounded-xl ${c.iconBg} p-2.5`}>
          {Icon && <Icon className={`w-5 h-5 ${c.iconColor}`} />}
        </div>
        {trend && (
          <span className={`text-xs font-semibold px-2 py-1 rounded-full ${c.trendBg} ${c.trendColor} flex items-center gap-1`}>
            {trend.startsWith('+') ? '↑' : trend.startsWith('-') ? '↓' : ''} {trend}
          </span>
        )}
      </div>
      
      <div className="relative z-10">
        <p className="text-3xl font-bold text-[#1A1A2E] tracking-tight">{value}</p>
        <p className="text-sm text-gray-500 mt-1">{title}</p>
        {subtitle && <p className="text-xs text-gray-400 mt-0.5 line-clamp-1">{subtitle}</p>}
      </div>

      {sparklineData && sparklineData.length > 0 && (
        <div className="absolute bottom-0 left-0 right-0 h-16 opacity-30 group-hover:opacity-60 transition-opacity duration-300 pointer-events-none">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sparklineData}>
              <Line 
                type="monotone" 
                dataKey="val" 
                stroke={c.stroke} 
                strokeWidth={2} 
                dot={false}
                isAnimationActive={true}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
