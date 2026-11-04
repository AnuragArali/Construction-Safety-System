import React, { useState, useEffect, useRef } from 'react';
import {
  Video,
  Play,
  Square,
  Upload,
  RefreshCw,
  HardHat,
  ShieldCheck,
  AlertTriangle,
  Cpu,
  Layers,
  CheckCircle,
  Eye,
  Sliders
} from 'lucide-react';
import api from '../services/api';
import StatusBadge from '../components/StatusBadge';

export default function LiveMonitoring({ monitoringActive, onToggleMonitoring, currentLanguage }) {
  const [telemetry, setTelemetry] = useState(null);
  const [sourceType, setSourceType] = useState('0'); // 0 for webcam/synthetic
  const [isUploading, setIsUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');
  const [streamError, setStreamError] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    const interval = setInterval(fetchTelemetry, 1500);
    return () => clearInterval(interval);
  }, []);

  const fetchTelemetry = async () => {
    try {
      const res = await api.getLatestDetections();
      setTelemetry(res.data);
      setStreamError(false);
    } catch (err) {
      console.error('Failed to get detection telemetry:', err);
    }
  };

  const handleSourceChange = async (newSource) => {
    setSourceType(newSource);
    if (monitoringActive) {
      await api.stopMonitoring();
      await api.startMonitoring(newSource, currentLanguage);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    setIsUploading(true);
    setUploadMessage('Uploading test video to local edge device...');

    try {
      const res = await api.uploadVideo(formData);
      setUploadMessage(`Success: ${res.data.filename} loaded.`);
      setSourceType(res.data.path);
      if (monitoringActive) {
        await api.startMonitoring(res.data.path, currentLanguage);
      }
    } catch (err) {
      setUploadMessage('Failed to upload video.');
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  const streamUrl = api.getStreamUrl();

  const workers = telemetry?.workers || [];
  const compliantWorkers = workers.filter((w) => (w.violations || []).length === 0);
  const violatingWorkers = workers.filter((w) => (w.violations || []).length > 0);

  return (
    <div className="space-y-6">
      {/* Title & Control Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-[#0f172a] p-5 rounded-2xl border border-slate-800 shadow-lg">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-orange-400 mb-1">
            <Video className="w-4 h-4" />
            <span>Industrial Safety Vision Pipeline</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">
            Live Edge Video Monitoring & Detection
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time optical evaluation on local hardware. Zero cloud video transmission.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <button
            onClick={onToggleMonitoring}
            className={`flex-1 sm:flex-none flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold transition-all shadow-lg ${
              monitoringActive
                ? 'bg-rose-600 hover:bg-rose-700 text-white shadow-rose-600/30'
                : 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-600/30'
            }`}
          >
            {monitoringActive ? (
              <>
                <Square className="w-4 h-4 fill-current" />
                Stop Monitoring
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                Start Monitoring
              </>
            )}
          </button>
        </div>
      </div>

      {/* Main Grid: Video Stream (2 cols) & Telemetry Panel (1 col) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stream Canvas */}
        <div className="lg:col-span-2 bg-[#0f172a] border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col justify-between">
          <div className="flex items-center justify-between mb-3 px-1">
            <div className="flex items-center gap-2">
              <span className={`w-2.5 h-2.5 rounded-full ${monitoringActive ? 'bg-emerald-500 animate-ping' : 'bg-slate-600'}`} />
              <span className="text-xs font-mono font-semibold text-slate-300">
                FEED: CAM-01 (AR GLASSES / WORKSPACE WEBCAM)
              </span>
            </div>
            <div className="flex items-center gap-2">
              <StatusBadge status={monitoringActive ? 'ONLINE' : 'IDLE'} />
              <span className="text-[11px] font-mono text-slate-400">
                {telemetry?.fps ? `${telemetry.fps} FPS` : '0 FPS'}
              </span>
            </div>
          </div>

          {/* Video Stream Container */}
          <div className="relative w-full aspect-video bg-black rounded-xl overflow-hidden border border-slate-800 flex items-center justify-center group">
            {monitoringActive ? (
              <img
                src={streamUrl}
                alt="Live Edge Video Stream"
                className="w-full h-full object-contain"
                onError={() => setStreamError(true)}
              />
            ) : (
              <div className="text-center p-8 space-y-3">
                <div className="w-16 h-16 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center mx-auto text-slate-400">
                  <Video className="w-8 h-8" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-slate-300">Edge Stream Paused</h4>
                  <p className="text-xs text-slate-400 mt-1 max-w-sm">
                    Click 'Start Monitoring' to activate camera capture, YOLO detection, and safety analysis.
                  </p>
                </div>
              </div>
            )}

            {/* Privacy Overlay Pill */}
            <div className="absolute top-3 left-3 bg-slate-950/80 backdrop-blur-md px-2.5 py-1 rounded-md border border-slate-800/80 text-[11px] text-emerald-400 flex items-center gap-1.5 font-mono">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>FACIAL PRIVACY BLUR: ACTIVE</span>
            </div>
          </div>

          {/* Source Selection & Video Upload Strip */}
          <div className="mt-4 pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2">
              <Sliders className="w-4 h-4 text-slate-400" />
              <span className="text-slate-400 font-medium">Input Source:</span>
              <select
                value={sourceType}
                onChange={(e) => handleSourceChange(e.target.value)}
                className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1 text-slate-200 focus:outline-none"
              >
                <option value="0">Default Camera / Synthetic Scene</option>
                <option value="1">Secondary USB AR/VR Camera</option>
                {sourceType.length > 2 && (
                  <option value={sourceType}>Uploaded Sample Video</option>
                )}
              </select>
            </div>

            <div>
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileUpload}
                accept="video/*"
                className="hidden"
              />
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={isUploading}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 transition-all font-medium"
              >
                <Upload className="w-3.5 h-3.5 text-orange-400" />
                <span>{isUploading ? 'Uploading...' : 'Upload Test Video'}</span>
              </button>
            </div>
          </div>
          {uploadMessage && (
            <p className="text-[11px] text-amber-400 mt-2 px-1">{uploadMessage}</p>
          )}
        </div>

        {/* Right Telemetry & Worker Breakdown */}
        <div className="space-y-5">
          {/* Edge Performance Card */}
          <div className="bg-[#0f172a] border border-slate-800 rounded-2xl p-5 shadow-lg">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-orange-400" />
              Edge Inference Metrics
            </h3>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400">Inference Latency</span>
                <p className="text-lg font-bold font-mono text-emerald-400 mt-1">
                  {telemetry?.inference_time_ms ? `${telemetry.inference_time_ms} ms` : '0.0 ms'}
                </p>
              </div>
              <div className="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400">Processing FPS</span>
                <p className="text-lg font-bold font-mono text-orange-400 mt-1">
                  {telemetry?.fps || 0}
                </p>
              </div>
            </div>
          </div>

          {/* Active Worker Status */}
          <div className="bg-[#0f172a] border border-slate-800 rounded-2xl p-5 shadow-lg">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                <HardHat className="w-4 h-4 text-orange-400" />
                Detected Workers ({workers.length})
              </h3>
              <div className="flex items-center gap-2 text-xs">
                <span className="text-emerald-400 font-bold">{compliantWorkers.length} Safe</span>
                <span className="text-slate-600">|</span>
                <span className="text-rose-400 font-bold">{violatingWorkers.length} At Risk</span>
              </div>
            </div>

            {workers.length === 0 ? (
              <p className="text-xs text-slate-400 py-6 text-center border border-dashed border-slate-800 rounded-xl">
                No workers currently in camera frame.
              </p>
            ) : (
              <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
                {workers.map((w, idx) => {
                  const hasViolations = (w.violations || []).length > 0;
                  return (
                    <div
                      key={w.worker_id || idx}
                      className={`p-3 rounded-xl border ${
                        hasViolations
                          ? 'bg-rose-950/20 border-rose-500/30'
                          : 'bg-emerald-950/20 border-emerald-500/20'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-semibold text-white">
                          {w.worker_id}
                        </span>
                        <StatusBadge status={hasViolations ? 'VIOLATION' : 'COMPLIANT'} />
                      </div>

                      <div className="mt-2 grid grid-cols-2 gap-2 text-[11px]">
                        <div className="flex items-center gap-1.5 text-slate-300">
                          <span
                            className={`w-2 h-2 rounded-full ${w.has_helmet ? 'bg-emerald-400' : 'bg-rose-500'}`}
                          />
                          <span>Helmet: {w.has_helmet ? 'Detected' : 'MISSING'}</span>
                        </div>
                        <div className="flex items-center gap-1.5 text-slate-300">
                          <span
                            className={`w-2 h-2 rounded-full ${w.has_vest ? 'bg-emerald-400' : 'bg-rose-500'}`}
                          />
                          <span>Vest: {w.has_vest ? 'Detected' : 'MISSING'}</span>
                        </div>
                      </div>

                      {hasViolations && (
                        <p className="mt-2 text-[11px] text-rose-300 bg-rose-900/30 p-1.5 rounded border border-rose-800/40">
                          Action Required: {(w.violations || []).join(', ').replace(/_/g, ' ')}
                        </p>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
