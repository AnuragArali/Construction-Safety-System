import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  HardHat,
  Shield,
  AlertTriangle,
  Globe,
  CheckCircle,
  FileText
} from 'lucide-react';
import api from '../services/api';

export default function SafetyInformation({ currentLanguage }) {
  const [guidelines, setGuidelines] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGuidelines(currentLanguage);
  }, [currentLanguage]);

  const fetchGuidelines = async (lang) => {
    try {
      const res = await api.getRecommendations(lang);
      setGuidelines(res.data);
    } catch (err) {
      console.error('Failed to load safety guidelines:', err);
    } finally {
      setLoading(false);
    }
  };

  const ppeList = guidelines?.ppe_requirements || [
    {
      equipment: 'Hard Hat / Safety Helmet',
      standard: 'ANSI/ISEA Z89.1 / EN 397',
      purpose: 'Shields against falling tools, overhead collisions, and electrical hazards.',
      mandatory_areas: 'All active construction zones and scaffolding perimeters.',
    },
    {
      equipment: 'High-Visibility Reflective Vest',
      standard: 'ANSI/ISEA 107 Class 2/3 / EN ISO 20471',
      purpose: 'Provides 360-degree high-contrast optical conspicuity for machine operators.',
      mandatory_areas: 'Roadwork, crane swing radiuses, and transport corridors.',
    },
    {
      equipment: 'Hazard Exclusion Perimeter',
      standard: 'OSHA 1926 Heavy Equipment Boundaries',
      purpose: 'Prohibits unauthorized personnel inside active heavy equipment operation zones.',
      mandatory_areas: 'Excavator radiuses, suspended loads, and trench margins.',
    },
  ];

  const actions = guidelines?.corrective_actions || {};

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-[#0f172a] p-5 rounded-2xl border border-slate-800 shadow-lg">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-orange-400 mb-1">
          <BookOpen className="w-4 h-4" />
          <span>Construction Site Standards</span>
        </div>
        <h1 className="text-xl font-bold text-white tracking-tight">
          Safety Guidelines & Worker Instructions
        </h1>
        <p className="text-xs text-slate-400 mt-0.5">
          OSHA, ANSI, and EN compliant workspace protocols and corrective recommendations.
        </p>
      </div>

      {/* PPE Standards Cards */}
      <div>
        <h3 className="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
          <HardHat className="w-4 h-4 text-orange-400" />
          Mandatory Personal Protective Equipment (PPE)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {ppeList.map((item, idx) => (
            <div
              key={idx}
              className="bg-[#0f172a] border border-slate-800 p-5 rounded-2xl shadow-lg space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono px-2 py-0.5 bg-orange-500/10 text-orange-400 border border-orange-500/20 rounded">
                  {item.standard}
                </span>
                <CheckCircle className="w-4 h-4 text-emerald-400" />
              </div>
              <h4 className="text-base font-bold text-white">{item.equipment}</h4>
              <p className="text-xs text-slate-300 leading-relaxed">{item.purpose}</p>
              <div className="pt-2 border-t border-slate-800/80 text-[11px] text-slate-400">
                <span className="text-slate-400 font-medium">Mandatory Zones: </span>
                {item.mandatory_areas}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Dynamic Native-Language Voice Broadcast Cards */}
      <div className="bg-[#0f172a] border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <Globe className="w-4 h-4 text-orange-400" />
              Dynamic Corrective Voice Messages ({currentLanguage?.toUpperCase() || 'EN'})
            </h3>
            <p className="text-xs text-slate-400">
              Audio synthesized locally on Raspberry Pi via pyttsx3 offline engine.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(actions).map(([typeKey, actionData]) => (
            <div
              key={typeKey}
              className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-2"
            >
              <span className="text-[11px] font-mono text-orange-400 uppercase">
                {typeKey.replace(/_/g, ' ')}
              </span>
              <h5 className="text-sm font-semibold text-white">{actionData.alert}</h5>
              <p className="text-xs text-slate-300 bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
                {actionData.recommendation}
              </p>
              <div className="text-[11px] text-emerald-400 font-mono flex items-center gap-1.5 pt-1">
                <span>🔊 Voice: "{actionData.voice}"</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
