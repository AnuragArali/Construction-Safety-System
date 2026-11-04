import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import LiveMonitoring from './pages/LiveMonitoring';
import SafetyAlerts from './pages/SafetyAlerts';
import SafetyHistory from './pages/SafetyHistory';
import Analytics from './pages/Analytics';
import SafetyInformation from './pages/SafetyInformation';
import Settings from './pages/Settings';
import api from './services/api';

export default function App() {
  const [monitoringActive, setMonitoringActive] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [unreadAlerts, setUnreadAlerts] = useState(0);

  useEffect(() => {
    checkSystemStatus();
    const interval = setInterval(checkSystemStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  const checkSystemStatus = async () => {
    try {
      const res = await api.getStatus();
      setMonitoringActive(res.data.monitoring.monitoring_active);
      setCurrentLanguage(res.data.current_language || 'en');
    } catch (err) {
      console.warn('Backend not yet reachable:', err.message);
    }
  };

  const handleToggleMonitoring = async () => {
    try {
      if (monitoringActive) {
        await api.stopMonitoring();
        setMonitoringActive(false);
      } else {
        await api.startMonitoring('0', currentLanguage);
        setMonitoringActive(true);
      }
    } catch (err) {
      console.error('Failed to toggle monitoring:', err);
    }
  };

  const handleLanguageChange = async (newLang) => {
    setCurrentLanguage(newLang);
    try {
      await api.updateSettings({ language: newLang });
    } catch (err) {
      console.error('Failed to update language:', err);
    }
  };

  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-[#0a0f1d] text-slate-100">
        {/* Left Fixed Sidebar */}
        <Sidebar monitoringActive={monitoringActive} />

        {/* Main Content Area */}
        <div className="flex-1 ml-64 flex flex-col min-h-screen">
          <Navbar
            monitoringActive={monitoringActive}
            onToggleMonitoring={handleToggleMonitoring}
            currentLanguage={currentLanguage}
            onLanguageChange={handleLanguageChange}
            unreadAlertsCount={unreadAlerts}
          />

          <main className="flex-1 p-6 overflow-y-auto">
            <Routes>
              <Route
                path="/"
                element={
                  <Dashboard
                    monitoringActive={monitoringActive}
                    onToggleMonitoring={handleToggleMonitoring}
                  />
                }
              />
              <Route
                path="/live"
                element={
                  <LiveMonitoring
                    monitoringActive={monitoringActive}
                    onToggleMonitoring={handleToggleMonitoring}
                    currentLanguage={currentLanguage}
                  />
                }
              />
              <Route path="/alerts" element={<SafetyAlerts />} />
              <Route path="/history" element={<SafetyHistory />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route
                path="/info"
                element={<SafetyInformation currentLanguage={currentLanguage} />}
              />
              <Route
                path="/settings"
                element={
                  <Settings
                    currentLanguage={currentLanguage}
                    onLanguageChange={handleLanguageChange}
                  />
                }
              />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}
