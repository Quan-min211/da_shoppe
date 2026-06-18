"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Package, BarChart3, ShoppingCart } from "lucide-react";

const navItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/products", label: "Products", icon: Package },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed top-0 left-0 h-screen w-[260px] bg-[#0F0F1A] flex flex-col z-50 rounded-r-3xl">
      {/* Logo */}
      <div className="p-6 pb-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#7C5CFC] flex items-center justify-center">
            <ShoppingCart className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight">Analytics</h1>
            <p className="text-[11px] text-gray-500">E-Commerce Platform</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 space-y-1">
        {navItems.map(({ href, label, icon: Icon }) => {
          const isActive = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-medium transition-all duration-200 group ${
                isActive
                  ? "bg-[#7C5CFC] text-white shadow-lg shadow-[#7C5CFC]/25"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <Icon className={`w-5 h-5 transition-transform duration-200 ${!isActive ? "group-hover:scale-110" : ""}`} />
              {label}
              {isActive && (
                <span className="ml-auto w-2 h-2 rounded-full bg-[#C8FF00]" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* Bottom Card */}
      <div className="p-4">
        <div className="px-4 py-4 rounded-2xl bg-gradient-to-br from-[#7C5CFC]/20 to-[#7C5CFC]/5 border border-[#7C5CFC]/20">
          <p className="text-xs text-gray-500 mb-1">Data Source</p>
          <p className="text-sm text-white font-semibold">Shopee Vietnam 🇻🇳</p>
          <p className="text-[11px] text-gray-500 mt-1">Gold Layer • Parquet</p>
        </div>
      </div>
    </aside>
  );
}
