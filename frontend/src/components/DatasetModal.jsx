import React, { useEffect, useState } from 'react';
import { X, Database, ShieldCheck, CheckCircle2, AlertCircle } from 'lucide-react';
import { api } from '../api/client';

export default function DatasetModal({ isOpen, onClose }) {
  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      api
        .getDatasetInfo()
        .then((data) => setInfo(data))
        .catch((err) => console.error(err))
        .finally(() => setLoading(false));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl max-w-lg w-full max-h-[90vh] overflow-hidden flex flex-col shadow-2xl border border-gray-200">
        {/* Header */}
        <div className="bg-whatsapp-dark text-white px-5 py-4 flex items-center justify-between border-b border-whatsapp-teal/40">
          <div className="flex items-center space-x-2.5">
            <Database className="w-5 h-5 text-emerald-300" />
            <div>
              <h2 className="font-bold text-base leading-tight">Dataset Schema & Integrity</h2>
              <p className="text-xs text-emerald-200">Kaggle: Student Academic Performance Dataset</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-full text-white/80 hover:text-white hover:bg-whatsapp-teal transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 overflow-y-auto space-y-4 text-xs text-gray-700">
          {/* Rule-based badge */}
          <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3 flex items-start space-x-2.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 mt-0.5 flex-shrink-0" />
            <div>
              <strong className="text-emerald-950 font-bold block mb-0.5">
                100% Rule-Based Engine (Zero LLMs / Gemini / OpenAI)
              </strong>
              <p className="text-emerald-800">
                All evaluations, advice, and responses are derived strictly from predefined Python conditional statements in Flask, preserving the raw dataset values without fabrication.
              </p>
            </div>
          </div>

          {/* Dataset Metrics */}
          <div className="grid grid-cols-2 gap-2 text-center">
            <div className="bg-gray-50 border border-gray-200 p-2.5 rounded-xl">
              <span className="text-gray-500 text-[11px] block">Total Student Records</span>
              <span className="text-lg font-extrabold text-whatsapp-dark">
                {info ? info.total_students : '2,000'}
              </span>
            </div>
            <div className="bg-gray-50 border border-gray-200 p-2.5 rounded-xl">
              <span className="text-gray-500 text-[11px] block">Student ID Range</span>
              <span className="text-lg font-extrabold text-whatsapp-dark">S1000 – S2999</span>
            </div>
          </div>

          {/* Confirmed Columns */}
          <div>
            <h3 className="font-bold text-gray-900 text-xs uppercase tracking-wider mb-2 flex items-center space-x-1.5">
              <ShieldCheck className="w-4 h-4 text-whatsapp-teal" />
              <span>Confirmed Dataset Columns (7 Total)</span>
            </h3>
            <div className="divide-y divide-gray-100 border border-gray-200 rounded-xl overflow-hidden bg-gray-50/50">
              {[
                { name: 'Student_ID', type: 'Unique Identifier', range: 'S1000 - S2999' },
                { name: 'Attendance (%)', type: 'Percentage Metric', range: '52% - 100%' },
                { name: 'Internal Test 1 (out of 40)', type: 'Exam Assessment', range: '18 - 40 marks' },
                { name: 'Internal Test 2 (out of 40)', type: 'Exam Assessment', range: '16 - 40 marks' },
                { name: 'Assignment Score (out of 10)', type: 'Coursework Metric', range: '4 - 10 score' },
                { name: 'Daily Study Hours', type: 'Behavioral Metric', range: '1 - 5 hrs/day' },
                { name: 'Final Exam Marks (out of 100)', type: 'End-Semester', range: '25 - 100 marks' },
              ].map((col, idx) => (
                <div key={idx} className="p-2.5 flex items-center justify-between hover:bg-white transition">
                  <div>
                    <span className="font-semibold text-gray-900 font-mono text-[11.5px] block">{col.name}</span>
                    <span className="text-[10px] text-gray-500">{col.type}</span>
                  </div>
                  <span className="text-[11px] font-medium bg-emerald-100/70 text-whatsapp-dark px-2 py-0.5 rounded border border-emerald-300">
                    {col.range}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Backend Architecture Note */}
          <div className="bg-gray-50 border border-gray-200 rounded-xl p-3 text-[11px] text-gray-600 leading-relaxed">
            <strong className="text-gray-900 block mb-1">Session Security Notice:</strong>
            Student records are secured via backend session tokens generated at verification. The frontend cannot access records of other students or modify grading thresholds.
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-100 px-5 py-3 flex justify-end border-t border-gray-200">
          <button
            onClick={onClose}
            className="bg-whatsapp-dark hover:bg-whatsapp-teal text-white text-xs font-semibold px-4 py-2 rounded-lg transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

