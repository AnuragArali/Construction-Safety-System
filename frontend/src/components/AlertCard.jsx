import React from 'react';
import { AlertTriangle, ShieldAlert, Volume2, Clock, CheckCircle } from 'lucide-react';
import StatusBadge from './StatusBadge';

export default function AlertCard({ alert, onSelect }) {
  const isCritical = alert.severity === 'CRITICAL';
  const isHigh = alert.severity === 'HIGH';

  const formattedTime = alert.timestamp
    ? new Date(alert.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    : 'Just now';

  return (
    <div
      onClick={() => onSelect && onSelect(alert)}
      className={`p-4 rounded-xl border transition-all cursor-pointer ${
        isCritical
          ? 'bg-rose-950/20 border-rose-500/40 hover:border-rose-500/80 shadow-rose-950/20'
          : isHigh
          ? 'bg-orange-950/20 border-orange-500/30 hover:border-orange-500/60'
          : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
      } shadow-md`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div
            className={`p-2 rounded-lg ${
              isCritical
                ? 'bg-rose-500/20 text-rose-400'
                : isHigh
                ? 'bg-orange-500/20 text-orange-400'
                : 'bg-amber-500/20 text-amber-400'
            }`}
          >
            {isCritical ? <ShieldAlert className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
          </div>
          <div>
            <h4 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              {alert.violation_type.replace(/_/g, ' ')}
            </h4>
            <div className="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
              <span className="flex items-center gap-1 font-mono">
                <Clock className="w-3.5 h-3.5" />
                {formattedTime}
              </span>
              <span>•</span>
              <span className="text-slate-300 font-medium">{alert.worker_tag || 'Worker'}</span>
              <span>•</span>
              <span className="text-slate-400">{alert.zone_name || 'General'}</span>
            </div>
          </div>
        </div>
        <StatusBadge status={alert.severity} />
      </div>

      <div className="mt-3 text-xs bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80 text-slate-300">
        <span className="text-amber-400 font-medium">Recommended Action: </span>
        {alert.recommendation}
      </div>

      <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800/60">
        <span className="flex items-center gap-1 text-emerald-400">
          <Volume2 className="w-3.5 h-3.5" />
          Voice Broadcast: {alert.language ? alert.language.toUpperCase() : 'EN'}
        </span>
        <span className="font-mono text-slate-400">
          Conf: {Math.round((alert.confidence || 0.85) * 100)}%
        </span>
      </div>
    </div>
  );
}
