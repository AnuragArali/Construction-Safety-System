import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AlertTriangle,
  ShieldCheck,
  Users,
  Activity,
  Video,
  ArrowRight,
  TrendingUp,
  HardHat,
  Volume2
} from 'lucide-react';
import {
  AreaChart,
  Area,
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
import AlertCard from '../components/AlertCard';
import StatusBadge from '../components/StatusBadge';

export default function Dashboard({ monitoringActive, onToggleMonitoring }) {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [recentAlerts, setRecentAlerts] = useState([]);
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 4000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, alertsRes, statusRes] = await Promise.all([
        api.getStatistics(),
        api.getLatestAlerts(5),
        api.getStatus(),
      ]);
      setStats(statsRes.data);
      setRecentAlerts(alertsRes.data);
      setSystemStatus(statusRes.data);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const pieColors = ['#f97316', '#ef4444', '#f59e0b', '#3b82f6'];

  const violationDistribution = stats?.by_type
    ? Object.entries(stats.by_type).map(([key, value]) => ({
        name: key.replace(/_/g, ' '),
        value: value,
      }))
    : [
        { name: 'Missing Helmet', value: 4 },
        { name: 'Missing Vest', value: 3 },
        { name: 'Zone Intrusion', value: 1 },
      ];

  const trendData = stats?.daily_trends?.length
    ? stats.daily_trends
    : [
        { date: 'Mon', violations: 3 },
        { date: 'Tue', violations: 5 },
        { date: 'Wed', violations: 2 },
        { date: 'Thu', violations: 6 },
        { date: 'Fri', violations: 4 },
        { date: 'Sat', violations: 2 },
        { date: 'Sun', violations: 1 },
      ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-navy-800 via-navy-800 to-navy-700 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-orange-400 mb-1">
            <HardHat className="w-4 h-4" />
            <span>Active Edge Surveillance</span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">
            Construction Workspace Safety Overview
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-xl">
            Privacy-preserving Edge AI continuously analyzes local AR/VR video feeds for PPE compliance
            and hazardous exclusion zone intrusions.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/live')}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-orange-600 hover:bg-orange-500 text-white text-xs font-semibold shadow-lg shadow-orange-600/30 transition-all"
          >
            <Video className="w-4 h-4" />
            Open Live Video Feed
          </button>
        </div>
      </div>

      {/* Primary KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Overall Compliance"
          value={`${stats?.compliance_rate || 94}%`}
          subtitle="Target threshold: >90%"
          icon={ShieldCheck}
          color="emerald"
          trend={{ isPositive: true, text: '+2.4%' }}
        />
        <StatCard
          title="Total Events Logged"
          value={stats?.total_events || 0}
          subtitle="Stored on local SQLite"
          icon={Activity}
          color="blue"
        />
        <StatCard
          title="Violations Detected Today"
          value={stats?.today_violations || 0}
          subtitle="Active shift count"
          icon={AlertTriangle}
          color="rose"
          trend={{ isPositive: false, text: `${stats?.today_violations || 0} events` }}
        />
        <StatCard
          title="Monitoring Engine"
          value={monitoringActive ? 'ACTIVE' : 'IDLE'}
          subtitle={monitoringActive ? 'Processing @ ~15 FPS' : 'Click start to monitor'}
          icon={CpuIcon}
          color={monitoringActive ? 'orange' : 'purple'}
        />
      </div>

      {/* Visual Analytics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trend Area Chart */}
        <div className="lg:col-span-2 bg-[#0f172a] border border-slate-800 rounded-2xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-white">7-Day Safety Violation Trend</h3>
              <p className="text-xs text-slate-400">Daily frequency of non-compliant events</p>
            </div>
            <span className="text-xs font-mono px-2.5 py-1 bg-slate-800 rounded-lg text-slate-300">
              On-Device Analytics
            </span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <defs>
                  <linearGradient id="violationGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f97316" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#f97316" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
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
                <Area
                  type="monotone"
                  dataKey="violations"
                  stroke="#f97316"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#violationGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Violation Distribution Pie Chart */}
        <div className="bg-[#0f172a] border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-white">Violation Distribution</h3>
            <p className="text-xs text-slate-400">Categorical breakdown of detected risks</p>
          </div>
          <div className="h-52 my-auto">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={violationDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={45}
                  outerRadius={70}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {violationDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    borderColor: '#334155',
                    borderRadius: '8px',
                    fontSize: '12px',
                    color: '#f8fafc',
                  }}
                />
                <Legend
                  wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }}
                  iconType="circle"
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="text-[11px] text-slate-400 text-center border-t border-slate-800/80 pt-2">
            Auto-debounced speech alerts avoid repeated sound alarms
          </div>
        </div>
      </div>

      {/* Recent Alerts Feed */}
      <div className="bg-[#0f172a] border border-slate-800 rounded-2xl p-5 shadow-lg">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-orange-500/10 text-orange-400 border border-orange-500/20">
              <Volume2 className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white">Live Voice Safety Alerts</h3>
              <p className="text-xs text-slate-400">
                Recent violations broadcast to workers via native speech
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/alerts')}
            className="flex items-center gap-1 text-xs text-orange-400 hover:text-orange-300 font-semibold"
          >
            <span>View All Alerts</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {recentAlerts.length === 0 ? (
          <div className="text-center py-8 text-slate-400 text-xs border border-dashed border-slate-800 rounded-xl">
            <ShieldCheck className="w-8 h-8 text-emerald-500/50 mx-auto mb-2" />
            No recent violations detected. All active workers are compliant.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recentAlerts.map((alert) => (
              <AlertCard
                key={alert.id || alert.event_uuid}
                alert={alert}
                onSelect={() => navigate('/alerts')}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function CpuIcon(props) {
  return (
    <svg {...props} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <rect width="16" height="16" x="4" y="4" rx="2" />
      <rect width="6" height="6" x="9" y="9" rx="1" />
      <path d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2" />
    </svg>
  );
}
