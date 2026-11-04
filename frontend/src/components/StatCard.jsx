import React from 'react';

export default function StatCard({ title, value, subtitle, icon: Icon, color = 'orange', trend }) {
  const colorMap = {
    orange: 'border-orange-500/20 bg-gradient-to-br from-orange-500/10 to-transparent text-orange-400',
    emerald: 'border-emerald-500/20 bg-gradient-to-br from-emerald-500/10 to-transparent text-emerald-400',
    rose: 'border-rose-500/20 bg-gradient-to-br from-rose-500/10 to-transparent text-rose-400',
    blue: 'border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-transparent text-blue-400',
    purple: 'border-purple-500/20 bg-gradient-to-br from-purple-500/10 to-transparent text-purple-400',
  };

  const activeColor = colorMap[color] || colorMap.orange;

  return (
    <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-5 shadow-lg relative overflow-hidden group hover:border-slate-700 transition-all">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</p>
          <h3 className="text-3xl font-bold text-slate-100 mt-2 font-mono">{value}</h3>
          {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
        </div>
        {Icon && (
          <div className={`p-3 rounded-lg border ${activeColor}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
      {trend && (
        <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center text-xs">
          <span className={trend.isPositive ? 'text-emerald-400 font-semibold' : 'text-rose-400 font-semibold'}>
            {trend.text}
          </span>
          <span className="text-slate-400 ml-2">vs. last shift</span>
        </div>
      )}
    </div>
  );
}
