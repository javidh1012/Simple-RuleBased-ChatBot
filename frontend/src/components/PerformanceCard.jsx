import React from 'react';
import { BarChart3, Clock, FileCheck, GraduationCap, CheckCircle, AlertCircle } from 'lucide-react';

export default function PerformanceCard({ data }) {
  if (!data) return null;

  const { composite_score, overall_standing, overall_color, metrics } = data;
  const { assignment, study_hours, final_exam } = metrics || {};

  const getStandingBadge = (color) => {
    switch (color) {
      case 'emerald':
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
      case 'green':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'amber':
        return 'bg-amber-100 text-amber-800 border-amber-300';
      case 'rose':
        return 'bg-rose-100 text-rose-800 border-rose-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div className="mt-2.5 pt-2.5 border-t border-gray-100 text-gray-800">
      {/* Overall Standing Banner */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-1.5 text-xs font-semibold text-gray-600 uppercase tracking-wider">
          <BarChart3 className="w-3.5 h-3.5 text-whatsapp-teal" />
          <span>Academic Scorecard</span>
        </div>
        {composite_score && (
          <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${getStandingBadge(overall_color)}`}>
            {overall_standing} ({composite_score}%)
          </span>
        )}
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 gap-2 mb-2">
        {/* Final Exam Marks */}
        {final_exam && final_exam.available && (
          <div className="bg-gray-50/90 rounded-xl p-2.5 border border-gray-200">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-bold text-gray-800 flex items-center space-x-1">
                <GraduationCap className="w-3.5 h-3.5 text-whatsapp-teal" />
                <span>Final Exam Marks</span>
              </span>
              <span className="text-xs font-bold text-whatsapp-dark bg-emerald-100/80 px-2 py-0.5 rounded border border-emerald-300">
                {final_exam.display_value}
              </span>
            </div>
            <div className="text-[11px] flex justify-between font-medium text-gray-600 mb-1">
              <span>Grade: <strong className="text-gray-900">{final_exam.grade}</strong></span>
              <span className="text-gray-500">Scale: 0-100</span>
            </div>
            <p className="text-[11px] text-gray-600 bg-white p-1.5 rounded border border-gray-100">
              💡 {final_exam.explanation}
            </p>
          </div>
        )}

        {/* Assignment Score */}
        {assignment && assignment.available && (
          <div className="bg-gray-50/90 rounded-xl p-2.5 border border-gray-200">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-bold text-gray-800 flex items-center space-x-1">
                <FileCheck className="w-3.5 h-3.5 text-whatsapp-teal" />
                <span>Assignment Score</span>
              </span>
              <span className="text-xs font-bold text-whatsapp-dark bg-emerald-100/80 px-2 py-0.5 rounded border border-emerald-300">
                {assignment.display_value}
              </span>
            </div>
            <div className="text-[11px] flex justify-between font-medium text-gray-600 mb-1">
              <span>Status: <strong className="text-gray-900">{assignment.status}</strong></span>
              <span className="text-gray-500">Scale: 0-10</span>
            </div>
            <p className="text-[11px] text-gray-600 bg-white p-1.5 rounded border border-gray-100">
              💡 {assignment.explanation}
            </p>
          </div>
        )}

        {/* Daily Study Hours */}
        {study_hours && study_hours.available && (
          <div className="bg-gray-50/90 rounded-xl p-2.5 border border-gray-200">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-bold text-gray-800 flex items-center space-x-1">
                <Clock className="w-3.5 h-3.5 text-whatsapp-teal" />
                <span>Daily Study Routine</span>
              </span>
              <span className="text-xs font-bold text-whatsapp-dark bg-emerald-100/80 px-2 py-0.5 rounded border border-emerald-300">
                {study_hours.display_value}
              </span>
            </div>
            <div className="text-[11px] flex justify-between font-medium text-gray-600 mb-1">
              <span>Status: <strong className="text-gray-900">{study_hours.status}</strong></span>
              <span className="text-gray-500">Recommended: 3+ hrs/day</span>
            </div>
            <p className="text-[11px] text-gray-600 bg-white p-1.5 rounded border border-gray-100">
              💡 {study_hours.explanation}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

