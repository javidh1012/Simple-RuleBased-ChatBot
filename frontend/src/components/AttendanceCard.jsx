import React from 'react';
import { Calendar, AlertTriangle, CheckCircle2, ShieldAlert, Award } from 'lucide-react';

export default function AttendanceCard({ data }) {
  if (!data) return null;

  const {
    percentage,
    status,
    badge,
    advice,
    color,
    is_safe,
    safe_threshold = 75,
    excellent_threshold = 85,
  } = data;

  // Determine color styling based on evaluation
  const colorMap = {
    emerald: {
      bar: 'bg-emerald-500',
      text: 'text-emerald-700',
      bg: 'bg-emerald-50 border-emerald-200',
      icon: CheckCircle2,
    },
    green: {
      bar: 'bg-green-500',
      text: 'text-green-700',
      bg: 'bg-green-50 border-green-200',
      icon: CheckCircle2,
    },
    yellow: {
      bar: 'bg-amber-400',
      text: 'text-amber-800',
      bg: 'bg-amber-50 border-amber-200',
      icon: AlertTriangle,
    },
    amber: {
      bar: 'bg-orange-500',
      text: 'text-orange-700',
      bg: 'bg-orange-50 border-orange-200',
      icon: AlertTriangle,
    },
    rose: {
      bar: 'bg-rose-500',
      text: 'text-rose-700',
      bg: 'bg-rose-50 border-rose-200',
      icon: ShieldAlert,
    },
  };

  const currentTheme = colorMap[color] || colorMap.green;
  const IconComponent = currentTheme.icon;

  return (
    <div className="mt-2.5 pt-2.5 border-t border-gray-100/90 text-gray-800">
      {/* Top Header Row */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-1.5 text-xs font-semibold text-gray-600 uppercase tracking-wider">
          <Calendar className="w-3.5 h-3.5 text-whatsapp-teal" />
          <span>Attendance Evaluation</span>
        </div>
        <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full border ${currentTheme.bg} ${currentTheme.text}`}>
          {status}
        </span>
      </div>

      {/* Main Percentage Display & Progress Bar */}
      <div className="bg-gray-50/90 rounded-xl p-3 border border-gray-200/80 mb-2.5">
        <div className="flex items-baseline justify-between mb-1.5">
          <div className="flex items-baseline space-x-1">
            <span className="text-2xl font-extrabold text-gray-900">{percentage}%</span>
            <span className="text-xs text-gray-500 font-medium">recorded</span>
          </div>
          <div className="text-right">
            <span className="text-[11px] text-gray-500 font-medium">Safe Threshold: </span>
            <span className="text-xs font-bold text-gray-700">{safe_threshold}%</span>
          </div>
        </div>

        {/* Visual Progress Bar */}
        <div className="relative w-full h-3 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={`h-full ${currentTheme.bar} rounded-full transition-all duration-700 ease-out`}
            style={{ width: `${Math.min(100, Math.max(0, percentage))}%` }}
          ></div>
        </div>

        {/* Markers Row */}
        <div className="relative flex justify-between text-[10px] text-gray-400 font-mono mt-1 px-0.5">
          <span>0%</span>
          <span className="text-orange-500">65% (Risk)</span>
          <span className="text-amber-600 font-semibold">75% (Safe)</span>
          <span className="text-emerald-600 font-semibold">85% (Distinction)</span>
          <span>100%</span>
        </div>
      </div>

      {/* Personalized Advice Box */}
      <div className={`p-2.5 rounded-lg border flex items-start space-x-2 text-xs leading-relaxed ${currentTheme.bg}`}>
        <IconComponent className={`w-4 h-4 flex-shrink-0 mt-0.5 ${currentTheme.text}`} />
        <div>
          <span className="font-semibold block mb-0.5 text-gray-900">Advice:</span>
          <p className="text-gray-700">{advice}</p>
        </div>
      </div>
    </div>
  );
}

