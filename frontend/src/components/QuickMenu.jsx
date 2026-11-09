import React from 'react';
import { User, Calendar, BookOpen, BarChart3, Target, HelpCircle } from 'lucide-react';

export default function QuickMenu({ onSelectOption, disabled = false }) {
  const options = [
    { id: 'profile', label: '1. My Profile', icon: User, command: '1' },
    { id: 'attendance', label: '2. Attendance Report', icon: Calendar, command: '2' },
    { id: 'internals', label: '3. Internal Examination Marks', icon: BookOpen, command: '3' },
    { id: 'performance', label: '4. Academic Performance', icon: BarChart3, command: '4' },
    { id: 'recommendations', label: '5. Study Recommendations', icon: Target, command: '5' },
    { id: 'help', label: '6. Help & Support', icon: HelpCircle, command: '6' },
  ];

  return (
    <div className="my-2 p-2 bg-white/70 backdrop-blur-xs rounded-xl border border-gray-200/70 shadow-xs">
      <div className="text-[11px] font-semibold text-gray-500 uppercase tracking-wider mb-1.5 px-1 flex items-center justify-between">
        <span>Interactive Academic Menu</span>
        <span className="text-[10px] text-whatsapp-teal font-normal">Tap any option</span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
        {options.map((opt) => {
          const Icon = opt.icon;
          return (
            <button
              key={opt.id}
              disabled={disabled}
              onClick={() => onSelectOption(opt.command, opt.label)}
              className="flex items-center space-x-2 text-left text-xs font-semibold px-3 py-2 rounded-lg bg-emerald-50/70 hover:bg-emerald-100/90 text-whatsapp-dark border border-emerald-200/80 transition-all duration-150 active:scale-98 disabled:opacity-50 disabled:pointer-events-none shadow-xs"
            >
              <div className="w-5 h-5 rounded-full bg-emerald-200/80 flex items-center justify-center flex-shrink-0 text-whatsapp-dark">
                <Icon className="w-3 h-3" />
              </div>
              <span className="truncate">{opt.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

