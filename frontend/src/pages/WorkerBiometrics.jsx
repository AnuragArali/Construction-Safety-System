import React, { useState, useEffect } from 'react';
import {
  Users,
  Fingerprint,
  ScanFace,
  Plus,
  Trash2,
  CheckCircle2,
  XCircle,
  Cpu,
  RefreshCw,
  Shield,
  Upload,
  UserPlus,
  Radio,
  HardHat,
  Sparkles,
} from 'lucide-react';
import api from '../services/api';

export default function WorkerBiometrics() {
  const [workers, setWorkers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [bioStatus, setBioStatus] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showFaceModal, setShowFaceModal] = useState(false);
  const [selectedWorker, setSelectedWorker] = useState(null);
  const [faceFile, setFaceFile] = useState(null);
  const [actionMessage, setActionMessage] = useState(null);

  // New Worker Form State
  const [newWorker, setNewWorker] = useState({
    worker_id: '',
    name: '',
    role: 'Technician',
    department: 'Construction & Framing',
    authorized_zones: ['General Worksite', 'Doorway-North'],
  });

  useEffect(() => {
    loadWorkersAndStatus();
  }, []);

  const loadWorkersAndStatus = async () => {
    setLoading(true);
    try {
      const [wRes, bRes] = await Promise.all([
        api.getWorkers(),
        api.getBiometricsStatus(),
      ]);
      setWorkers(wRes.data || []);
      setBioStatus(bRes.data || null);
    } catch (err) {
      console.error('Failed to load workers or biometric status:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateWorker = async (e) => {
    e.preventDefault();
    if (!newWorker.worker_id || !newWorker.name) return;

    try {
      await api.createWorker(newWorker);
      setShowAddModal(false);
      setNewWorker({
        worker_id: '',
        name: '',
        role: 'Technician',
        department: 'Construction & Framing',
        authorized_zones: ['General Worksite', 'Doorway-North'],
      });
      showMessage('Worker created successfully!', 'success');
      loadWorkersAndStatus();
    } catch (err) {
      showMessage(err.response?.data?.detail || 'Failed to create worker.', 'error');
    }
  };

  const handleDeleteWorker = async (workerId) => {
    if (!window.confirm(`Are you sure you want to remove worker ${workerId}?`)) return;
    try {
      await api.deleteWorker(workerId);
      showMessage(`Worker ${workerId} removed.`, 'info');
      loadWorkersAndStatus();
    } catch (err) {
      showMessage('Failed to delete worker.', 'error');
    }
  };

  const handleEnrollFingerprint = async (workerId) => {
    try {
      const res = await api.enrollFingerprint({ worker_id: workerId });
      showMessage(res.data.message || 'Fingerprint enrolled successfully!', 'success');
      loadWorkersAndStatus();
    } catch (err) {
      showMessage(err.response?.data?.detail || 'Fingerprint enrollment failed.', 'error');
    }
  };

  const handleEnrollFaceSubmit = async (e) => {
    e.preventDefault();
    if (!selectedWorker) return;

    const formData = new FormData();
    if (faceFile) {
      formData.append('file', faceFile);
    }

    try {
      const res = await api.enrollFace(selectedWorker.worker_id, formData);
      setShowFaceModal(false);
      setFaceFile(null);
      showMessage(res.data.message || 'Face biometrics enrolled!', 'success');
      loadWorkersAndStatus();
    } catch (err) {
      showMessage(err.response?.data?.detail || 'Face enrollment failed.', 'error');
    }
  };

  const showMessage = (msg, type = 'info') => {
    setActionMessage({ text: msg, type });
    setTimeout(() => setActionMessage(null), 4500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
            <Fingerprint className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              Worker Biometrics & Identity Management
              <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">
                Edge Biometrics
              </span>
            </h2>
            <p className="text-xs text-slate-400">
              Fingerprint Enrollment (AS608/R503) & Local Face Recognition (OpenCV 128-D Embeddings)
            </p>
          </div>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="px-4 py-2 rounded-lg bg-orange-600 hover:bg-orange-500 text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-orange-600/20 transition self-start sm:self-auto"
        >
          <UserPlus className="w-4 h-4" />
          Register New Worker
        </button>
      </div>

      {/* Action Notification Banner */}
      {actionMessage && (
        <div
          className={`p-3.5 rounded-lg border text-xs font-medium flex items-center gap-2 ${
            actionMessage.type === 'success'
              ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-300'
              : actionMessage.type === 'error'
              ? 'bg-rose-950/40 border-rose-500/40 text-rose-300'
              : 'bg-slate-900 border-slate-700 text-slate-300'
          }`}
        >
          {actionMessage.type === 'success' ? (
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          ) : (
            <XCircle className="w-4 h-4 text-rose-400 shrink-0" />
          )}
          <span>{actionMessage.text}</span>
        </div>
      )}

      {/* Hardware Diagnostics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Fingerprint Hardware Card */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
            <span className="text-xs font-semibold text-white flex items-center gap-2">
              <Fingerprint className="w-4 h-4 text-cyan-400" />
              Optical Fingerprint Sensor
            </span>
            <span
              className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                bioStatus?.fingerprint?.hardware_connected
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              }`}
            >
              {bioStatus?.fingerprint?.operating_mode || 'EDGE_SIMULATION'}
            </span>
          </div>
          <div className="mt-3 space-y-1.5 text-xs text-slate-400 font-mono">
            <div className="flex justify-between">
              <span>Model / Chipset:</span>
              <span className="text-slate-200">AS608 / R503 DSP</span>
            </div>
            <div className="flex justify-between">
              <span>Serial Port:</span>
              <span className="text-slate-200">{bioStatus?.fingerprint?.port || '/dev/serial0'}</span>
            </div>
            <div className="flex justify-between">
              <span>Baud Rate:</span>
              <span className="text-slate-200">57600 bps</span>
            </div>
            <div className="flex justify-between">
              <span>Enrolled Templates:</span>
              <span className="text-cyan-400 font-bold">
                {bioStatus?.fingerprint?.enrolled_fingerprints || 0} / {bioStatus?.fingerprint?.max_capacity || 300}
              </span>
            </div>
          </div>
        </div>

        {/* Face Recognition Card */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
            <span className="text-xs font-semibold text-white flex items-center gap-2">
              <ScanFace className="w-4 h-4 text-purple-400" />
              Edge Face Recognizer
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
              OFFLINE / EDGE
            </span>
          </div>
          <div className="mt-3 space-y-1.5 text-xs text-slate-400 font-mono">
            <div className="flex justify-between">
              <span>Feature Descriptor:</span>
              <span className="text-slate-200">Spatial LBP + DCT</span>
            </div>
            <div className="flex justify-between">
              <span>Embedding Vector:</span>
              <span className="text-purple-300 font-bold">128-Dimensional</span>
            </div>
            <div className="flex justify-between">
              <span>Distance Metric:</span>
              <span className="text-slate-200">Cosine Similarity (Unit L2)</span>
            </div>
            <div className="flex justify-between">
              <span>Match Threshold:</span>
              <span className="text-emerald-400 font-bold">70% (0.70)</span>
            </div>
          </div>
        </div>

        {/* Raspberry Pi Hardware Pinout Card */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
            <span className="text-xs font-semibold text-white flex items-center gap-2">
              <Cpu className="w-4 h-4 text-emerald-400" />
              Raspberry Pi GPIO Pinout
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              RPi 4 / 5 Ready
            </span>
          </div>
          <div className="mt-3 space-y-1.5 text-xs text-slate-400 font-mono">
            <div className="flex justify-between">
              <span>Turnstile Relay:</span>
              <span className="text-emerald-400 font-bold">BCM 17 (Physical Pin 11)</span>
            </div>
            <div className="flex justify-between">
              <span>Green Access LED:</span>
              <span className="text-emerald-400 font-bold">BCM 27 (Physical Pin 13)</span>
            </div>
            <div className="flex justify-between">
              <span>Red Alert LED:</span>
              <span className="text-rose-400 font-bold">BCM 22 (Physical Pin 15)</span>
            </div>
            <div className="flex justify-between">
              <span>Sensor UART TX/RX:</span>
              <span className="text-cyan-400 font-bold">Pins 8 / 10 (/dev/serial0)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Enrolled Workers Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Users className="w-4 h-4 text-orange-400" />
            <h3 className="text-sm font-semibold text-white">Registered Construction Personnel Directory</h3>
          </div>
          <button
            onClick={loadWorkersAndStatus}
            className="text-xs text-slate-400 hover:text-white flex items-center gap-1 font-mono transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Refresh
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800 font-mono">
              <tr>
                <th className="py-3 px-4">Worker ID</th>
                <th className="py-3 px-4">Full Name & Role</th>
                <th className="py-3 px-4">Department</th>
                <th className="py-3 px-4">Fingerprint</th>
                <th className="py-3 px-4">Face Recognition</th>
                <th className="py-3 px-4">Authorized Zones</th>
                <th className="py-3 px-4 text-right">Biometric Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {loading ? (
                <tr>
                  <td colSpan="7" className="py-8 text-center text-slate-500">
                    Loading enrolled personnel...
                  </td>
                </tr>
              ) : workers.length === 0 ? (
                <tr>
                  <td colSpan="7" className="py-8 text-center text-slate-500">
                    No workers enrolled yet. Click 'Register New Worker' above.
                  </td>
                </tr>
              ) : (
                workers.map((w) => (
                  <tr key={w.worker_id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3 px-4 font-mono font-bold text-orange-400">
                      {w.worker_id}
                    </td>
                    <td className="py-3 px-4 font-semibold text-white">
                      {w.name}
                      <span className="text-[11px] text-slate-400 font-normal block">{w.role}</span>
                    </td>
                    <td className="py-3 px-4 text-slate-400">{w.department}</td>
                    <td className="py-3 px-4 font-mono">
                      {w.fingerprint_enrolled ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-[10px] font-bold">
                          <CheckCircle2 className="w-3 h-3" />
                          SLOT #{w.fingerprint_id || 1}
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">
                          <XCircle className="w-3 h-3" />
                          NOT ENROLLED
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4 font-mono">
                      {w.face_enrolled ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 text-[10px] font-bold">
                          <CheckCircle2 className="w-3 h-3" />
                          128-D ENROLLED
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">
                          <XCircle className="w-3 h-3" />
                          NOT ENROLLED
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-slate-400 text-[11px] max-w-xs truncate">
                      {w.authorized_zones?.join(', ')}
                    </td>
                    <td className="py-3 px-4 text-right space-x-1.5 whitespace-nowrap">
                      <button
                        onClick={() => handleEnrollFingerprint(w.worker_id)}
                        className="px-2 py-1 rounded bg-cyan-950/60 hover:bg-cyan-900 border border-cyan-500/30 text-cyan-300 text-[11px] font-mono transition"
                        title="Enroll Fingerprint template"
                      >
                        <Fingerprint className="w-3 h-3 inline mr-1" />
                        Enroll Print
                      </button>

                      <button
                        onClick={() => {
                          setSelectedWorker(w);
                          setShowFaceModal(true);
                        }}
                        className="px-2 py-1 rounded bg-purple-950/60 hover:bg-purple-900 border border-purple-500/30 text-purple-300 text-[11px] font-mono transition"
                        title="Upload Face Photo"
                      >
                        <ScanFace className="w-3 h-3 inline mr-1" />
                        Enroll Face
                      </button>

                      <button
                        onClick={() => handleDeleteWorker(w.worker_id)}
                        className="p-1 rounded hover:bg-rose-950 text-slate-400 hover:text-rose-400 transition"
                        title="Delete Worker"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal: Register New Worker */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 w-full max-w-md shadow-2xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <UserPlus className="w-5 h-5 text-orange-400" />
                Register Construction Worker
              </h3>
              <button
                onClick={() => setShowAddModal(false)}
                className="text-slate-400 hover:text-white text-sm"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateWorker} className="space-y-3.5 text-xs">
              <div>
                <label className="text-slate-300 block mb-1">Worker Badge ID *</label>
                <input
                  type="text"
                  placeholder="e.g. W-105"
                  value={newWorker.worker_id}
                  onChange={(e) => setNewWorker({ ...newWorker, worker_id: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 text-white px-3 py-2 rounded focus:outline-none focus:border-orange-500 font-mono"
                  required
                />
              </div>

              <div>
                <label className="text-slate-300 block mb-1">Full Name *</label>
                <input
                  type="text"
                  placeholder="e.g. Anand Gowda"
                  value={newWorker.name}
                  onChange={(e) => setNewWorker({ ...newWorker, name: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 text-white px-3 py-2 rounded focus:outline-none focus:border-orange-500"
                  required
                />
              </div>

              <div>
                <label className="text-slate-300 block mb-1">Role / Designation</label>
                <input
                  type="text"
                  placeholder="e.g. Steel Fixer / Scaffolder"
                  value={newWorker.role}
                  onChange={(e) => setNewWorker({ ...newWorker, role: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 text-white px-3 py-2 rounded focus:outline-none focus:border-orange-500"
                />
              </div>

              <div>
                <label className="text-slate-300 block mb-1">Department</label>
                <input
                  type="text"
                  placeholder="e.g. Framing & Rigging"
                  value={newWorker.department}
                  onChange={(e) => setNewWorker({ ...newWorker, department: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 text-white px-3 py-2 rounded focus:outline-none focus:border-orange-500"
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded bg-orange-600 hover:bg-orange-500 text-white font-semibold shadow"
                >
                  Save & Register
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Enroll Face Photo */}
      {showFaceModal && selectedWorker && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 w-full max-w-md shadow-2xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <ScanFace className="w-5 h-5 text-purple-400" />
                Enroll Face: {selectedWorker.name}
              </h3>
              <button
                onClick={() => {
                  setShowFaceModal(false);
                  setFaceFile(null);
                }}
                className="text-slate-400 hover:text-white text-sm"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-slate-400">
              Upload a clear photo or snapshot of the worker. The Raspberry Pi edge engine extracts a 128-D spatial LBP/DCT feature vector and stores it locally in SQLite.
            </p>

            <form onSubmit={handleEnrollFaceSubmit} className="space-y-4 text-xs">
              <div className="border-2 border-dashed border-slate-700 hover:border-purple-500 rounded-xl p-6 text-center transition cursor-pointer bg-slate-950/60">
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setFaceFile(e.target.files[0] || null)}
                  className="hidden"
                  id="face-photo-input"
                />
                <label htmlFor="face-photo-input" className="cursor-pointer block space-y-2">
                  <Upload className="w-8 h-8 text-purple-400 mx-auto" />
                  <span className="text-slate-300 font-medium block">
                    {faceFile ? faceFile.name : 'Click to select face photo'}
                  </span>
                  <span className="text-[11px] text-slate-500 block font-mono">
                    PNG, JPG, or JPEG (Processed strictly on-device)
                  </span>
                </label>
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => {
                    setShowFaceModal(false);
                    setFaceFile(null);
                  }}
                  className="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded bg-purple-600 hover:bg-purple-500 text-white font-semibold shadow"
                >
                  Extract Embedding & Enroll
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
