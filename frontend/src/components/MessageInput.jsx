import React, { useState } from 'react';
import { Send, Smile, Paperclip, Sparkles, Mic } from 'lucide-react';

export default function MessageInput({
  onSendMessage,
  disabled = false,
  isAuthenticated = false,
  onQuickStudentSelect,
}) {
  const [inputText, setInputText] = useState('');

  const sampleStudents = [
    { id: 'S1000', label: 'S1000 (Standard)' },
    { id: 'S1001', label: 'S1001 (Excellent 91%)' },
    { id: 'S1031', label: 'S1031 (Borderline 75%)' },
    { id: 'S1002', label: 'S1002 (Warning 73%)' },
    { id: 'S1678', label: 'S1678 (Critical 60%)' },
    { id: 'S1118', label: 'S1118 (Low Internals)' },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = inputText.trim();
    if (!trimmed || disabled) return;
    onSendMessage(trimmed);
    setInputText('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="bg-whatsapp-panel border-t border-gray-200/80 px-3 py-2 z-10">
      {/* Sample Student IDs Bar if not authenticated */}
      {!isAuthenticated && (
        <div className="mb-2 px-1 flex items-center space-x-1.5 overflow-x-auto pb-1 text-xs">
          <span className="text-[11px] font-semibold text-gray-500 flex items-center space-x-1 flex-shrink-0">
            <Sparkles className="w-3 h-3 text-whatsapp-teal" />
            <span>Sample IDs:</span>
          </span>
          {sampleStudents.map((s) => (
            <button
              key={s.id}
              type="button"
              onClick={() => onQuickStudentSelect(s.id)}
              className="px-2 py-0.5 rounded-full bg-white hover:bg-emerald-50 text-whatsapp-dark font-medium border border-gray-200 hover:border-whatsapp-teal transition flex-shrink-0 text-[11px] shadow-2xs"
            >
              {s.label}
            </button>
          ))}
        </div>
      )}

      {/* Main input form */}
      <form onSubmit={handleSubmit} className="flex items-center space-x-2">
        <button
          type="button"
          className="text-gray-500 hover:text-gray-700 p-1.5 rounded-full hover:bg-gray-200/70 transition hidden sm:block"
          title="Emojis"
        >
          <Smile className="w-5 h-5" />
        </button>

        <button
          type="button"
          className="text-gray-500 hover:text-gray-700 p-1.5 rounded-full hover:bg-gray-200/70 transition hidden sm:block"
          title="Attach"
        >
          <Paperclip className="w-5 h-5" />
        </button>

        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder={
            isAuthenticated
              ? "Type a message or menu number (1-6)..."
              : "Enter your Student ID (e.g., S1000)..."
          }
          className="flex-1 bg-white text-gray-800 placeholder-gray-400 text-sm rounded-xl px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-whatsapp-teal border border-gray-200/90 shadow-inner"
        />

        {inputText.trim() ? (
          <button
            type="submit"
            disabled={disabled}
            className="w-10 h-10 rounded-full bg-whatsapp-teal hover:bg-emerald-700 text-white flex items-center justify-center transition shadow-md active:scale-95 disabled:opacity-50"
            title="Send"
          >
            <Send className="w-5 h-5 ml-0.5" />
          </button>
        ) : (
          <button
            type="button"
            className="w-10 h-10 rounded-full bg-whatsapp-teal/80 text-white flex items-center justify-center transition hover:bg-whatsapp-teal shadow-md"
            title="Voice message placeholder"
          >
            <Mic className="w-5 h-5" />
          </button>
        )}
      </form>
    </div>
  );
}

