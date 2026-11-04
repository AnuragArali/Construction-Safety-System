import React from 'react';

export default function StatusBadge({ status, size = 'sm' }) {
  const s = (status || '').toUpperCase();

  const styles = {
    COMPLIANT: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    SAFE: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    ONLINE: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    VIOLATION: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    CRITICAL: 'bg-rose-600/20 text-rose-400 border-rose-600/30 animate-pulse',
    HIGH: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
    MEDIUM: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    LOW: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    IDLE: 'bg-slate-500/10 text-slate-400 border-slate-500/20',
  };

  const currentStyle = styles[s] || styles.IDLE;
  const sizeStyle = size === 'lg' ? 'px-3 py-1 text-xs' : 'px-2 py-0.5 text-[11px]';

  return (
    <span
      className={`inline-flex items-center font-medium uppercase tracking-wider rounded-full border ${currentStyle} ${sizeStyle}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current mr-1.5"></span>
      {status}
    </span>
  );
}
