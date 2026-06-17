"use client";

export default function KpiCard({ title, value, subtitle, icon: Icon, color = "indigo" }) {
  const colorMap = {
    indigo: {
      gradient: "from-indigo-500/10 to-indigo-600/5",
      border: "border-indigo-500/20",
      iconBg: "bg-indigo-500/15",
      iconColor: "text-indigo-400",
      valueColor: "text-indigo-50",
    },
    emerald: {
      gradient: "from-emerald-500/10 to-emerald-600/5",
      border: "border-emerald-500/20",
      iconBg: "bg-emerald-500/15",
      iconColor: "text-emerald-400",
      valueColor: "text-emerald-50",
    },
    amber: {
      gradient: "from-amber-500/10 to-amber-600/5",
      border: "border-amber-500/20",
      iconBg: "bg-amber-500/15",
      iconColor: "text-amber-400",
      valueColor: "text-amber-50",
    },
    rose: {
      gradient: "from-rose-500/10 to-rose-600/5",
      border: "border-rose-500/20",
      iconBg: "bg-rose-500/15",
      iconColor: "text-rose-400",
      valueColor: "text-rose-50",
    },
  };

  const c = colorMap[color] || colorMap.indigo;

  return (
    <div
      className={`relative overflow-hidden rounded-2xl bg-gradient-to-br ${c.gradient} border ${c.border} p-6 backdrop-blur-sm transition-all duration-300 hover:scale-[1.02] hover:shadow-lg`}
    >
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-sm font-medium text-slate-400">{title}</p>
          <p className={`text-3xl font-bold tracking-tight ${c.valueColor}`}>{value}</p>
          {subtitle && <p className="text-xs text-slate-500">{subtitle}</p>}
        </div>
        {Icon && (
          <div className={`rounded-xl ${c.iconBg} p-3`}>
            <Icon className={`w-6 h-6 ${c.iconColor}`} />
          </div>
        )}
      </div>
      {/* Decorative glow */}
      <div className={`absolute -bottom-4 -right-4 w-24 h-24 rounded-full ${c.iconBg} blur-2xl opacity-50`} />
    </div>
  );
}
