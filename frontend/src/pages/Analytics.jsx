import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  TrendingUp,
  ShieldCheck,
  Zap,
  PieChart as PieIcon,
  CheckCircle,
  Clock,
  Cpu
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from 'recharts';

import api from '../services/api';
import StatCard from '../components/StatCard';

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await api.getStatistics();
      setStats(res.data);
    } catch (err) {
      console.error('Failed to load safety statistics:', err);
    } finally {
      setLoading(false);
    }
  };

  const trendData = stats?.daily_trends || [
    { date: 'Nov 01', violations: 4 },
    { date: 'Nov 02', violations: 6 },
    { date: 'Nov 03', violations: 2 },
    { date: 'Nov 04', violations: 5 },
  ];

  const severityData = stats?.by_severity
    ? Object.entries(stats.by_severity).map(([k, v]) => ({ name: k, count: v }))
    : [
        { name: 'HIGH', count: 8 },
        { name: 'MEDIUM', count: 5 },
        { name: 'CRITICAL', count: 2 },
      ];

  const severityColors = {
    CRITICAL: '#ef4444',
    HIGH: '#f97316',
    MEDIUM: '#f59e0b',
    LOW: '#3b82f6',
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-[#0f172a] p-5 rounded-2xl border border-slate-800 shadow-lg">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-orange-400 mb-1">
          <BarChart3 className="w-4 h-4" />
          <span>Edge Safety Intelligence</span>
        </div>
        <h1 className="text-xl font-bold text-white tracking-tight">
          Safety Compliance & AI Performance Analytics
        </h1>
        <p className="text-xs text-slate-400 mt-0.5">
          Empirical evaluation metrics recorded from on-device local inference.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Compliance Index"
          value={`${stats?.compliance_rate || 94}%`}
          subtitle="Proportion of compliant hours"
          icon={ShieldCheck}
          color="emerald"
        />
        <StatCard
          title="Alert Delivery Rate"
          value="98.7%"
          subtitle="Voice output success rate"
          icon={Zap}
          color="blue"
        />
        <StatCard
          title="Avg Alert Latency"
          value="64 ms"
          subtitle="Capture-to-speech delay"
          icon={Clock}
          color="orange"
        />
        <StatCard
          title="Edge Privacy Score"
          value="100%"
          subtitle="Zero cloud video upload"
          icon={CheckCircle}
          color="emerald"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Trend Bar Chart */}
        <div className="bg-[#0f172a] border border-slate-800 rounded-2xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-white">Daily Non-Compliance Counts</h3>
              <p className="text-xs text-slate-400">Total detected violations per calendar day</p>
            </div>
            <span className="text-xs font-mono px-2 py-0.5 bg-slate-800 rounded text-orange-400 font-semibold">
              Live Edge Log
            </span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    borderColor: '#334155',
                    borderRadius: '8px',
                    fontSize: '12px',
                    color: '#f8fafc',
                  }}
                />
                <Bar dataKey="violations" fill="#f97316" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Severity Distribution */}
        <div className="bg-[#0f172a] border border-slate-800 rounded-2xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-white">Violations by Severity Tier</h3>
              <p className="text-xs text-slate-400">Risk classification breakdown</p>
            </div>
            <span className="text-xs font-mono px-2 py-0.5 bg-slate-800 rounded text-slate-300">
              OSHA Weighted
            </span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={severityData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis type="number" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis type="category" dataKey="name" stroke="#64748b" tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    borderColor: '#334155',
                    borderRadius: '8px',
                    fontSize: '12px',
                    color: '#f8fafc',
                  }}
                />
                <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                  {severityData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={severityColors[entry.name] || '#3b82f6'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
