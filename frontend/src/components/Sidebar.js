"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Package, BarChart3, Activity } from "lucide-react";

const navItems = [
  { href: "/", label: "Overview", icon: LayoutDashboard },
  { href: "/products", label: "Products", icon: Package },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed top-0 left-0 h-screen w-64 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 border-r border-slate-700/50 flex flex-col z-50">
      {/* Logo */}
      <div className="p-6 border-b border-slate-700/50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight">Analytics</h1>
            <p className="text-xs text-slate-400">E-Commerce Platform</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1.5">
        {navItems.map(({ href, label, icon: Icon }) => {
          const isActive = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group ${
                isActive
                  ? "bg-indigo-500/15 text-indigo-400 shadow-sm shadow-indigo-500/10 border border-indigo-500/20"
                  : "text-slate-400 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <Icon className={`w-5 h-5 transition-transform duration-200 ${isActive ? "text-indigo-400" : "group-hover:scale-110"}`} />
              {label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-700/50">
        <div className="px-4 py-3 rounded-xl bg-slate-800/50 border border-slate-700/30">
          <p className="text-xs text-slate-500">Data Source</p>
          <p className="text-sm text-slate-300 font-medium">Shopee Vietnam 🇻🇳</p>
        </div>
      </div>
    </aside>
  );
}
