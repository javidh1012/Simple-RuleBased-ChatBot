import React from 'react';
import { CheckCheck } from 'lucide-react';
import AttendanceCard from './AttendanceCard';
import InternalMarksCard from './InternalMarksCard';
import PerformanceCard from './PerformanceCard';
import RecommendationCard from './RecommendationCard';
import QuickMenu from './QuickMenu';

export default function ChatMessage({ message, onButtonClick }) {
  const isUser = message.sender === 'user';

  // Format text helper for WhatsApp-like markdown (*bold*, _italic_)
  const formatText = (text) => {
    if (!text) return null;
    const lines = text.split('\n');

    return lines.map((line, lIdx) => {
      // Parse *bold* and _italic_
      const parts = line.split(/(\*[^*]+\*|_[^_]+_)/g);

      return (
        <span key={lIdx} className="block min-h-[1.15rem]">
          {parts.map((part, pIdx) => {
            if (part.startsWith('*') && part.endsWith('*')) {
              return <strong key={pIdx} className="font-bold text-gray-950">{part.slice(1, -1)}</strong>;
            }
            if (part.startsWith('_') && part.endsWith('_')) {
              return <em key={pIdx} className="italic text-gray-800">{part.slice(1, -1)}</em>;
            }
            return part;
          })}
        </span>
      );
    });
  };

  return (
    <div className={`flex flex-col mb-3 ${isUser ? 'items-end' : 'items-start'}`}>
      <div
        className={`relative max-w-[88%] sm:max-w-[78%] md:max-w-[68%] rounded-2xl px-3.5 py-2.5 shadow-sm text-sm ${
          isUser
            ? 'bg-whatsapp-bubbleOut text-gray-900 rounded-tr-none bubble-out-tail border border-emerald-200/50'
            : 'bg-whatsapp-bubbleIn text-gray-900 rounded-tl-none bubble-in-tail border border-gray-200/60'
        }`}
      >
        {/* Message body */}
        <div className="leading-relaxed whitespace-pre-wrap break-words text-[13.5px]">
          {formatText(message.text)}
        </div>

        {/* Embedded Dynamic Rich Cards */}
        {message.card_type === 'attendance' && <AttendanceCard data={message.card_data} />}
        {message.card_type === 'internals' && <InternalMarksCard data={message.card_data} />}
        {message.card_type === 'performance' && <PerformanceCard data={message.card_data} />}
        {message.card_type === 'recommendations' && <RecommendationCard data={message.card_data} />}

        {/* Dynamic Buttons (e.g., Quick Menu options) */}
        {message.buttons && message.buttons.length > 0 && (
          <div className="mt-3 pt-2 border-t border-gray-200/60 flex flex-wrap gap-1.5">
            {message.buttons.map((btn) => (
              <button
                key={btn.id}
                onClick={() => onButtonClick(btn.command || btn.id, btn.label)}
                className="text-xs bg-emerald-50 hover:bg-emerald-100 text-whatsapp-dark font-semibold px-2.5 py-1.5 rounded-lg border border-emerald-300 transition active:scale-95 shadow-2xs"
              >
                {btn.label}
              </button>
            ))}
          </div>
        )}

        {/* Timestamp and Checkmarks */}
        <div className="flex items-center justify-end space-x-1 mt-1 text-[10px] text-gray-400 select-none">
          <span>{message.timestamp}</span>
          {isUser && (
            <CheckCheck className="w-3.5 h-3.5 text-[#53bdeb]" />
          )}
        </div>
      </div>
    </div>
  );
}

