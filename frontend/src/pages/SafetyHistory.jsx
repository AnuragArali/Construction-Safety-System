import React, { useState, useEffect } from 'react';
import {
  History,
  Search,
  Filter,
  Download,
  Calendar,
  ShieldAlert,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import api from '../services/api';
import StatusBadge from '../components/StatusBadge';

export default function SafetyHistory() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [page, setPage] = useState(0);
  const pageSize = 15;

  useEffect(() => {
    fetchEvents();
  }, [search, severityFilter, categoryFilter, page]);

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const res = await api.getEvents({
        limit: pageSize,
        offset: page * pageSize,
        violation_type: search || undefined,
        severity: severityFilter || undefined,
        category: categoryFilter || undefined,
      });
      setEvents(res.data);
    } catch (err) {
      console.error('Failed to load safety events history:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = () => {
    if (events.length === 0) return;
    const headers = ['Event UUID', 'Timestamp', 'Violation Type', 'Severity', 'Category', 'Worker Tag', 'Confidence', 'Recommendation'];
    const rows = events.map((e) => [
      e.event_uuid,
      e.timestamp,
      `"${e.violation_type}"`,
      e.severity,
      e.category,
      `"${e.worker_tag}"`,
      e.confidence,
      `"${e.recommendation.replace(/"/g, '""')}"`
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `safety_events_log_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-[#0f172a] p-5 rounded-2xl border border-slate-800 shadow-lg">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-orange-400 mb-1">
            <History className="w-4 h-4" />
            <span>SQLite Local Audit Log</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">
            Safety Event Historical Records
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Minimal metadata stored on-device. No raw video footage is persisted.
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-xs font-semibold transition-all"
        >
          <Download className="w-4 h-4" />
          Export Audit CSV
        </button>
      </div>

      {/* Filters Bar */}
      <div className="bg-[#0f172a] p-4 rounded-xl border border-slate-800 shadow-md flex flex-wrap items-center gap-3">
        <div className="flex-1 min-w-[200px] relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search violation type (e.g. Helmet, Vest)..."
            className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-orange-500"
          />
        </div>

        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none"
        >
          <option value="">All Severities</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
        </select>

        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none"
        >
          <option value="">All Categories</option>
          <option value="PPE">PPE</option>
          <option value="ZONE_BOUNDARY">Zone Boundary</option>
        </select>
      </div>

      {/* Event Table */}
      <div className="bg-[#0f172a] border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900/80 text-[11px] uppercase tracking-wider text-slate-400 border-b border-slate-800 font-mono">
              <tr>
                <th className="py-3.5 px-4">Timestamp</th>
                <th className="py-3.5 px-4">Violation Type</th>
                <th className="py-3.5 px-4">Severity</th>
                <th className="py-3.5 px-4">Subject Tag</th>
                <th className="py-3.5 px-4">Workspace Zone</th>
                <th className="py-3.5 px-4">Confidence</th>
                <th className="py-3.5 px-4">Corrective Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {events.length === 0 ? (
                <tr>
                  <td colSpan="7" className="py-12 text-center text-slate-400">
                    No safety records found matching your filter criteria.
                  </td>
                </tr>
              ) : (
                events.map((e) => (
                  <tr key={e.id || e.event_uuid} className="hover:bg-slate-900/40 transition-colors">
                    <td className="py-3.5 px-4 font-mono text-slate-400 whitespace-nowrap">
                      {new Date(e.timestamp).toLocaleString()}
                    </td>
                    <td className="py-3.5 px-4 font-semibold text-white whitespace-nowrap">
                      {e.violation_type.replace(/_/g, ' ')}
                    </td>
                    <td className="py-3.5 px-4 whitespace-nowrap">
                      <StatusBadge status={e.severity} />
                    </td>
                    <td className="py-3.5 px-4 font-mono text-slate-300 whitespace-nowrap">
                      {e.worker_tag}
                    </td>
                    <td className="py-3.5 px-4 text-slate-400 whitespace-nowrap">
                      {e.zone_name}
                    </td>
                    <td className="py-3.5 px-4 font-mono text-emerald-400 font-semibold whitespace-nowrap">
                      {Math.round(e.confidence * 100)}%
                    </td>
                    <td className="py-3.5 px-4 text-slate-300 max-w-md truncate">
                      {e.recommendation}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className="p-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <span>Showing page {page + 1}</span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(0, p - 1))}
              disabled={page === 0}
              className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 disabled:opacity-40 border border-slate-800"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => setPage((p) => p + 1)}
              disabled={events.length < pageSize}
              className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 disabled:opacity-40 border border-slate-800"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
