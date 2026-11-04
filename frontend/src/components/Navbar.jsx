import React from 'react';
import { ShieldCheck, Volume2, Globe, Bell, RefreshCw, Power } from 'lucide-react';

export default function Navbar({
  monitoringActive,
  onToggleMonitoring,
  currentLanguage,
  onLanguageChange,
  unreadAlertsCount = 0,
}) {
  const languages = [
    { code: 'en', label: 'English' },
    { code: 'hi', label: 'हिन्दी' },
    { code: 'kn', label: 'ಕನ್ನಡ' },
    { code: 'es', label: 'Español' },
  ];

  return (
    <header className="h-16 bg-[#0f172a]/90 backdrop-blur-md border-b border-slate-800 px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Left Title / Location */}
      <div className="flex items-center gap-4">
        <div>
          <span className="text-xs uppercase tracking-widest text-slate-400 font-mono">
            Location: Site Zone Alpha (Gate 3 Scaffolding)
          </span>
          <h2 className="text-sm font-semibold text-slate-200">
            Real-Time Edge Computer Vision Monitor
          </h2>
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-4">
        {/* Language Quick Switcher */}
        <div className="flex items-center bg-slate-900 border border-slate-700/80 rounded-lg p-1">
          <Globe className="w-3.5 h-3.5 text-slate-400 ml-2 mr-1" />
          <select
            value={currentLanguage}
            onChange={(e) => onLanguageChange && onLanguageChange(e.target.value)}
            className="bg-transparent text-xs text-slate-200 focus:outline-none cursor-pointer pr-2 py-1 font-medium"
          >
            {languages.map((l) => (
              <option key={l.code} value={l.code} className="bg-slate-900 text-slate-200">
                {l.label}
              </option>
            ))}
          </select>
        </div>

        {/* Privacy Verified Badge */}
        <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Local-Only Processing</span>
        </div>

        {/* Live Monitoring Button */}
        <button
          onClick={onToggleMonitoring}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all shadow-md ${
            monitoringActive
              ? 'bg-rose-600 hover:bg-rose-700 text-white shadow-rose-600/20'
              : 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-600/20'
          }`}
        >
          <Power className="w-3.5 h-3.5" />
          {monitoringActive ? 'Stop Monitoring' : 'Start Monitoring'}
        </button>
      </div>
    </header>
  );
}
