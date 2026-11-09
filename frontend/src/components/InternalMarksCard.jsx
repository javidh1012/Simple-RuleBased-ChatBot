import React from 'react';
import { BookOpen, TrendingUp, TrendingDown, Minus, Award, AlertCircle } from 'lucide-react';

export default function InternalMarksCard({ data }) {
  if (!data) return null;

  const { test_1, test_2, average, average_percentage, trend, trend_description } = data;

  const getTestColor = (category) => {
    if (category?.includes('Excellent')) {
      return {
        badge: 'bg-emerald-50 text-emerald-700 border-emerald-200',
        bar: 'bg-emerald-500',
        scoreColor: 'text-emerald-700',
      };
    }
    if (category?.includes('Needs Improvement')) {
      return {
        badge: 'bg-amber-50 text-amber-700 border-amber-200',
        bar: 'bg-amber-500',
        scoreColor: 'text-amber-700',
      };
    }
    return {
      badge: 'bg-rose-50 text-rose-700 border-rose-200',
      bar: 'bg-rose-500',
      scoreColor: 'text-rose-700',
    };
  };

  const t1Style = test_1 ? getTestColor(test_1.category) : null;
  const t2Style = test_2 ? getTestColor(test_2.category) : null;

  return (
    <div className="mt-2.5 pt-2.5 border-t border-gray-100 text-gray-800">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-1.5 text-xs font-semibold text-gray-600 uppercase tracking-wider">
          <BookOpen className="w-3.5 h-3.5 text-whatsapp-teal" />
          <span>Internal Assessment (Scale: /40)</span>
        </div>
        {average !== null && (
          <span className="text-xs font-bold text-whatsapp-dark bg-emerald-100/80 px-2 py-0.5 rounded-full border border-emerald-300">
            Avg: {average} / 40 ({average_percentage}%)
          </span>
        )}
      </div>

      {/* Side-by-side or stacked tests */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-2.5">
        {/* Test 1 */}
        {test_1 && (
          <div className="bg-gray-50/90 rounded-xl p-2.5 border border-gray-200/80">
            <div className="flex justify-between items-baseline mb-1">
              <span className="text-xs font-bold text-gray-700">Internal Test 1</span>
              <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded border ${t1Style.badge}`}>
                {test_1.category}
              </span>
            </div>
            <div className="flex items-baseline space-x-1 mb-1">
              <span className={`text-xl font-extrabold ${t1Style.scoreColor}`}>{test_1.score}</span>
              <span className="text-xs text-gray-400">/ 40</span>
              <span className="text-[11px] text-gray-500 font-medium ml-auto">({test_1.percentage}%)</span>
            </div>
            {/* Progress bar */}
            <div className="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden mb-1.5">
              <div
                className={`h-full ${t1Style.bar} rounded-full`}
                style={{ width: `${test_1.percentage}%` }}
              ></div>
            </div>
            <p className="text-[11px] text-gray-600 italic bg-white/80 p-1.5 rounded border border-gray-100">
              "{test_1.feedback}"
            </p>
          </div>
        )}

        {/* Test 2 */}
        {test_2 && (
          <div className="bg-gray-50/90 rounded-xl p-2.5 border border-gray-200/80">
            <div className="flex justify-between items-baseline mb-1">
              <span className="text-xs font-bold text-gray-700">Internal Test 2</span>
              <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded border ${t2Style.badge}`}>
                {test_2.category}
              </span>
            </div>
            <div className="flex items-baseline space-x-1 mb-1">
              <span className={`text-xl font-extrabold ${t2Style.scoreColor}`}>{test_2.score}</span>
              <span className="text-xs text-gray-400">/ 40</span>
              <span className="text-[11px] text-gray-500 font-medium ml-auto">({test_2.percentage}%)</span>
            </div>
            {/* Progress bar */}
            <div className="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden mb-1.5">
              <div
                className={`h-full ${t2Style.bar} rounded-full`}
                style={{ width: `${test_2.percentage}%` }}
              ></div>
            </div>
            <p className="text-[11px] text-gray-600 italic bg-white/80 p-1.5 rounded border border-gray-100">
              "{test_2.feedback}"
            </p>
          </div>
        )}
      </div>

      {/* Trend Summary */}
      {trend_description && (
        <div className="bg-emerald-50/70 border border-emerald-200/80 rounded-lg p-2 text-xs flex items-center justify-between">
          <div className="flex items-center space-x-1.5 text-gray-700">
            {trend === 'Improving' && <TrendingUp className="w-4 h-4 text-emerald-600" />}
            {trend === 'Declining' && <TrendingDown className="w-4 h-4 text-rose-500" />}
            {trend === 'Consistent' && <Minus className="w-4 h-4 text-blue-500" />}
            <span className="font-medium">{trend_description}</span>
          </div>
          <span className="text-[10px] text-gray-500 uppercase font-semibold">Trend</span>
        </div>
      )}
    </div>
  );
}

