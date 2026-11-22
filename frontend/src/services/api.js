import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // System Status
  getStatus: () => apiClient.get('/status'),

  // Monitoring
  startMonitoring: (source = '0', language = 'en') =>
    apiClient.post('/monitoring/start', { source, language }),
  stopMonitoring: () => apiClient.post('/monitoring/stop'),
  getLatestDetections: () => apiClient.get('/monitoring/detections'),
  getStreamUrl: () => `${API_BASE_URL}/monitoring/stream`,

  // Video Upload
  uploadVideo: (formData) =>
    apiClient.post('/upload/video', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  // Alerts & Events
  getLatestAlerts: (limit = 8) => apiClient.get(`/alerts/latest?limit=${limit}`),
  getEvents: (params = {}) => apiClient.get('/events', { params }),
  getStatistics: () => apiClient.get('/events/statistics'),

  // Safety Rules
  getRules: () => apiClient.get('/rules'),
  toggleRule: (rule_code, is_enabled) =>
    apiClient.post('/rules/toggle', { rule_code, is_enabled }),

  // Recommendations & Information
  getRecommendations: (language = 'en') =>
    apiClient.get(`/recommendations?language=${language}`),

  // Privacy Compliance
  getPrivacyCompliance: () => apiClient.get('/privacy/compliance'),
  purgeRecords: (days) => apiClient.post(`/privacy/purge?days=${days || ''}`),

  // Settings
  getSettings: () => apiClient.get('/settings'),
  updateSettings: (data) => apiClient.post('/settings', data),

  // Worker Biometrics & Directory
  getWorkers: () => apiClient.get('/workers'),
  createWorker: (data) => apiClient.post('/workers', data),
  deleteWorker: (worker_id) => apiClient.delete(`/workers/${worker_id}`),
  getBiometricsStatus: () => apiClient.get('/biometrics/status'),
  enrollFingerprint: (data) => apiClient.post('/biometrics/fingerprint/enroll', data),
  verifyFingerprint: (data = {}) => apiClient.post('/biometrics/fingerprint/verify', data),
  enrollFace: (worker_id, formData) =>
    apiClient.post(`/biometrics/face/enroll?worker_id=${worker_id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  verifyFace: (formData) =>
    apiClient.post('/biometrics/face/verify', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  // Doorway / Mock Work Area Checkpoint
  verifyCheckpoint: (data = {}) => apiClient.post('/checkpoint/verify', data),
  getCheckpointLogs: (params = {}) => apiClient.get('/checkpoint/logs', { params }),
  getCheckpointStats: () => apiClient.get('/checkpoint/stats'),
};

export default api;
