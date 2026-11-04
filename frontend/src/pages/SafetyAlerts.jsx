import React, { useState, useEffect } from 'react';
import {
  AlertTriangle,
  Volume2,
  ShieldAlert,
  Clock,
  Filter,
  RefreshCw,
  Info,
  CheckCircle,
  X
} from 'lucide-react';
import api from '../services/api';
import AlertCard from '../components/AlertCard';
import StatusBadge from '../components/StatusBadge';

export default function SafetyAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [filterSeverity, setFilterSeverity] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchAlerts = async () => {
    try {
      const res = await api.getLatestAlerts(25);
      setAlerts(res.data);
    } catch (err) {
      console.error('Failed to load alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredAlerts = alerts.filter((a) => {
    if (filterSeverity === 'ALL') return true;
    return a.severity === filterSeverity;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-[#0f172a] p-5 rounded-2xl border border-slate-800 shadow-lg">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-orange-400 mb-1">
            <AlertTriangle className="w-4 h-4" />
            <span>Active Safety Warning Queue</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">
            Real-Time Voice & Visual Safety Alerts
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time notifications generated locally by the Edge AI safety analysis engine.
          </p>
        </div>

        {/* Severity Filter */}
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none"
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">Critical Only</option>
            <option value="HIGH">High Severity</option>
            <option value="MEDIUM">Medium Severity</option>
          </select>
        </div>
      </div>

      {/* Alerts Grid */}
      {filteredAlerts.length === 0 ? (
        <div className="text-center py-16 bg-[#0f172a] border border-slate-800 rounded-2xl p-8 shadow-lg">
          <CheckCircle className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
          <h3 className="text-sm font-semibold text-slate-200">No Active Violations</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            All workers in monitored sectors are currently adhering to mandatory PPE and workspace rules.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredAlerts.map((alert) => (
            <AlertCard
              key={alert.id || alert.event_uuid}
              alert={alert}
              onSelect={(a) => setSelectedAlert(a)}
            />
          ))}
        </div>
      )}

      {/* Alert Detail Modal */}
      {selectedAlert && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0f172a] border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative space-y-4">
            <button
              onClick={() => setSelectedAlert(null)}
              className="absolute top-4 right-4 text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-3">
              <div className="p-3 rounded-xl bg-orange-500/10 text-orange-400 border border-orange-500/20">
                <ShieldAlert className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">
                  {selectedAlert.violation_type.replace(/_/g, ' ')}
                </h3>
                <p className="text-xs text-slate-400">
                  Event UUID: {selectedAlert.event_uuid}
                </p>
              </div>
            </div>

            <div className="space-y-3 bg-slate-900/60 p-4 rounded-xl border border-slate-800 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Severity</span>
                <StatusBadge status={selectedAlert.severity} />
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Timestamp</span>
                <span className="text-slate-200 font-mono">
                  {new Date(selectedAlert.timestamp).toLocaleString()}
                </span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Subject Tag</span>
                <span className="text-slate-200">{selectedAlert.worker_tag}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Workspace Zone</span>
                <span className="text-slate-200">{selectedAlert.zone_name}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-400">Detection Confidence</span>
                <span className="text-emerald-400 font-mono font-bold">
                  {Math.round(selectedAlert.confidence * 100)}%
                </span>
              </div>
            </div>

            <div className="bg-amber-950/20 border border-amber-500/30 p-3.5 rounded-xl text-xs space-y-1">
              <span className="font-semibold text-amber-400 flex items-center gap-1.5">
                <Info className="w-4 h-4" />
                Corrective Recommendation
              </span>
              <p className="text-slate-300 leading-relaxed">
                {selectedAlert.recommendation}
              </p>
            </div>

            <div className="flex items-center justify-between pt-2">
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <Volume2 className="w-4 h-4 text-emerald-400" />
                <span>Voice Alert: Delivered in {selectedAlert.language?.toUpperCase() || 'EN'}</span>
              </div>
              <button
                onClick={() => setSelectedAlert(null)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold"
              >
                Close Details
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
