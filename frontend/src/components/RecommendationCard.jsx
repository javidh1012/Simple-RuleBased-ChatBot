import React from 'react';
import { Target, AlertCircle, CheckCircle2, ListOrdered, Sparkles } from 'lucide-react';

export default function RecommendationCard({ data }) {
  if (!data) return null;

  const { overall_status, summary, weak_areas = [], satisfactory_areas = [], action_items = [] } = data;

  return (
    <div className="mt-2.5 pt-2.5 border-t border-gray-100 text-gray-800">
      {/* Diagnostic Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-1.5 text-xs font-semibold text-gray-600 uppercase tracking-wider">
          <Target className="w-3.5 h-3.5 text-whatsapp-teal" />
          <span>Study Plan & Recommendations</span>
        </div>
        <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">
          {overall_status}
        </span>
      </div>

      {/* Summary Quote Box */}
      <div className="bg-emerald-50/70 border border-emerald-200/90 rounded-xl p-2.5 mb-2.5">
        <p className="text-xs text-emerald-950 font-medium italic leading-relaxed">
          "{summary}"
        </p>
      </div>

      {/* Weak Areas vs Strengths */}
      <div className="space-y-2 mb-2.5">
        {weak_areas.length > 0 && (
          <div className="bg-rose-50/70 border border-rose-200/80 rounded-xl p-2.5">
            <span className="text-[11px] font-bold uppercase tracking-wider text-rose-800 flex items-center space-x-1 mb-1.5">
              <AlertCircle className="w-3.5 h-3.5 text-rose-600" />
              <span>Priority Focus Areas (Needs Attention)</span>
            </span>
            <div className="space-y-1">
              {weak_areas.map((w, idx) => (
                <div key={idx} className="text-xs text-gray-700 bg-white/80 p-1.5 rounded border border-rose-100">
                  <strong className="text-rose-900">{w.area}: </strong>
                  <span>{w.detail}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {satisfactory_areas.length > 0 && (
          <div className="bg-emerald-50/60 border border-emerald-200/80 rounded-xl p-2.5">
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800 flex items-center space-x-1 mb-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              <span>Current Strengths</span>
            </span>
            <div className="space-y-1">
              {satisfactory_areas.map((s, idx) => (
                <div key={idx} className="text-xs text-gray-700 bg-white/80 p-1.5 rounded border border-emerald-100">
                  <strong className="text-emerald-900">{s.area}: </strong>
                  <span>{s.detail}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Prioritized Action Checklist */}
      {action_items.length > 0 && (
        <div className="bg-gray-50/90 rounded-xl p-2.5 border border-gray-200">
          <span className="text-[11px] font-bold uppercase tracking-wider text-gray-700 flex items-center space-x-1 mb-2">
            <ListOrdered className="w-3.5 h-3.5 text-whatsapp-teal" />
            <span>Prioritized Action Steps</span>
          </span>
          <div className="space-y-1.5">
            {action_items.map((act, idx) => {
              const badgeColor =
                act.urgency === 'High'
                  ? 'bg-rose-100 text-rose-800 border-rose-300'
                  : act.urgency === 'Medium'
                  ? 'bg-amber-100 text-amber-800 border-amber-300'
                  : 'bg-emerald-100 text-emerald-800 border-emerald-300';

              return (
                <div key={idx} className="bg-white p-2 rounded-lg border border-gray-200/80 shadow-xs">
                  <div className="flex items-center justify-between mb-0.5">
                    <span className="text-xs font-bold text-gray-900">
                      {idx + 1}. {act.title}
                    </span>
                    <span className={`text-[10px] font-bold px-1.5 py-0.2 rounded border ${badgeColor}`}>
                      {act.urgency} Priority
                    </span>
                  </div>
                  <p className="text-[11px] text-gray-600 leading-snug">{act.action}</p>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

