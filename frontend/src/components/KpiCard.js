"use client";

export default function KpiCard({ title, value, subtitle, icon: Icon, trend, color = "purple" }) {
  const colorMap = {
    purple: { bg: "bg-white", iconBg: "bg-[#7C5CFC]/10", iconColor: "text-[#7C5CFC]", trendBg: "bg-[#7C5CFC]/10", trendColor: "text-[#7C5CFC]" },
    green:  { bg: "bg-white", iconBg: "bg-emerald-50",    iconColor: "text-emerald-600", trendBg: "bg-emerald-50", trendColor: "text-emerald-600" },
    amber:  { bg: "bg-white", iconBg: "bg-amber-50",      iconColor: "text-amber-600",   trendBg: "bg-amber-50",  trendColor: "text-amber-600" },
    rose:   { bg: "bg-white", iconBg: "bg-rose-50",       iconColor: "text-rose-600",    trendBg: "bg-rose-50",   trendColor: "text-rose-600" },
  };

  const c = colorMap[color] || colorMap.purple;

  return (
    <div className={`${c.bg} rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-0.5`}>
      <div className="flex items-start justify-between mb-4">
        <div className={`rounded-xl ${c.iconBg} p-2.5`}>
          {Icon && <Icon className={`w-5 h-5 ${c.iconColor}`} />}
        </div>
        {trend && (
          <span className={`text-xs font-semibold px-2 py-1 rounded-full ${c.trendBg} ${c.trendColor}`}>
            {trend}
          </span>
        )}
      </div>
      <p className="text-3xl font-bold text-[#1A1A2E] tracking-tight">{value}</p>
      <p className="text-sm text-gray-500 mt-1">{title}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-0.5">{subtitle}</p>}
    </div>
  );
}
