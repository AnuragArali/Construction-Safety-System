import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Video,
  AlertTriangle,
  History,
  BarChart3,
  BookOpen,
  Settings as SettingsIcon,
  HardHat,
  Cpu,
  ShieldCheck,
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Live Monitoring', href: '/live', icon: Video },
  { name: 'Safety Alerts', href: '/alerts', icon: AlertTriangle },
  { name: 'Safety History', href: '/history', icon: History },
  { name: 'Safety Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Safety Guidelines', href: '/info', icon: BookOpen },
  { name: 'System Settings', href: '/settings', icon: SettingsIcon },
];

export default function Sidebar({ monitoringActive }) {
  return (
    <aside className="w-64 bg-[#0a0f1d] border-r border-slate-800 flex flex-col h-screen fixed left-0 top-0 z-30 select-none">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800 flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-orange-600 to-amber-500 flex items-center justify-center shadow-lg shadow-orange-600/20 text-white">
          <HardHat className="w-6 h-6" />
        </div>
        <div>
          <h1 className="font-bold text-sm tracking-tight text-white flex items-center gap-1.5">
            SafeEdge <span className="text-orange-500 text-xs px-1.5 py-0.2 bg-orange-500/10 border border-orange-500/20 rounded">AI</span>
          </h1>
          <p className="text-[10px] text-slate-400 uppercase tracking-widest font-mono">
            SIT Tumakuru • ECE
          </p>
        </div>
      </div>

      {/* Edge System Status Pill */}
      <div className="px-4 py-3 border-b border-slate-800/80 bg-slate-900/40">
        <div className="flex items-center justify-between text-xs">
          <span className="flex items-center gap-1.5 text-slate-400">
            <Cpu className="w-3.5 h-3.5 text-emerald-400" />
            RPi Edge Unit
          </span>
          <span className={`inline-flex items-center gap-1 text-[11px] font-mono px-2 py-0.5 rounded-full ${
            monitoringActive
              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
              : 'bg-slate-800 text-slate-400'
          }`}>
            <span className={`w-1.5 h-1.5 rounded-full ${monitoringActive ? 'bg-emerald-400 animate-ping' : 'bg-slate-400'}`} />
            {monitoringActive ? 'ACTIVE' : 'STANDBY'}
          </span>
        </div>
      </div>

      {/* Nav Links */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {navigation.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-orange-600 text-white shadow-md shadow-orange-600/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/70'
                }`
              }
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Privacy Guarantee Footer */}
      <div className="p-4 border-t border-slate-800/80 bg-[#0a0f1d]">
        <div className="bg-slate-900/80 rounded-lg p-3 border border-slate-800 text-xs">
          <div className="flex items-center gap-2 text-emerald-400 font-semibold mb-1">
            <ShieldCheck className="w-4 h-4" />
            <span>Privacy Guard</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Zero raw video cloud streaming. All CV inferencing computed strictly on local Raspberry Pi RAM.
          </p>
        </div>
      </div>
    </aside>
  );
}
