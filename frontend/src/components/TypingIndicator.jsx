import React from 'react';

export default function TypingIndicator() {
  return (
    <div className="flex items-end mb-3 space-x-1">
      <div className="relative bg-white text-gray-800 rounded-2xl rounded-bl-none px-4 py-3 shadow-sm border border-gray-200/50 bubble-in-tail flex items-center space-x-2">
        <span className="text-xs text-gray-500 font-medium mr-1">Evaluating rules</span>
        <div className="flex space-x-1.5 items-center">
          <span className="w-2 h-2 rounded-full bg-whatsapp-teal animate-dot-1"></span>
          <span className="w-2 h-2 rounded-full bg-whatsapp-teal animate-dot-2"></span>
          <span className="w-2 h-2 rounded-full bg-whatsapp-teal animate-dot-3"></span>
        </div>
      </div>
    </div>
  );
}

