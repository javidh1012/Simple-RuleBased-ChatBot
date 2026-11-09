import React from 'react';
import { GraduationCap, ShieldCheck, LogOut, Database, MoreVertical, Sparkles } from 'lucide-react';

export default function ChatHeader({
  studentId,
  isAuthenticated,
  isTyping,
  onLogout,
  onOpenDatasetModal,
  onOpenProfile,
}) {
  return (
    <header className="bg-whatsapp-dark text-white px-4 py-3 flex items-center justify-between shadow-md select-none z-10 border-b border-whatsapp-teal/30">
      <div className="flex items-center space-x-3">
        {/* Avatar with status ring */}
        <div className="relative">
          <div className="w-10 h-10 rounded-full bg-whatsapp-teal flex items-center justify-center text-white ring-2 ring-emerald-400/80 shadow-inner">
            <GraduationCap className="w-6 h-6" />
          </div>
          <span className="absolute bottom-0 right-0 w-3 h-3 bg-emerald-400 border-2 border-whatsapp-dark rounded-full"></span>
        </div>

        {/* Title and Status */}
        <div className="flex flex-col">
          <div className="flex items-center space-x-2">
            <h1 className="font-semibold text-base leading-tight">Student Academic Assistant</h1>
            <span className="text-[10px] bg-emerald-700/70 text-emerald-200 px-1.5 py-0.5 rounded font-mono font-medium">
              Rule-Based
            </span>
          </div>
          <p className="text-xs text-emerald-100/90 flex items-center space-x-1.5">
            {isTyping ? (
              <span className="text-emerald-300 font-medium italic animate-pulse">typing...</span>
            ) : isAuthenticated ? (
              <span className="flex items-center space-x-1 text-emerald-200">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                <span>Online • Session Active</span>
              </span>
            ) : (
              <span>Online • Awaiting Student ID</span>
            )}
          </p>
        </div>
      </div>

      {/* Right Actions */}
      <div className="flex items-center space-x-2">
        {/* Kaggle Dataset Info Pill */}
        <button
          onClick={onOpenDatasetModal}
          title="Inspect Kaggle Dataset Columns & Verification"
          className="flex items-center space-x-1 text-xs bg-whatsapp-teal hover:bg-emerald-700 px-2.5 py-1.5 rounded-full transition text-white border border-emerald-400/30"
        >
          <Database className="w-3.5 h-3.5 text-emerald-200" />
          <span className="hidden sm:inline font-medium">Dataset Info</span>
        </button>

        {/* Authenticated Student Pill */}
        {isAuthenticated && (
          <>
            <button
              onClick={onOpenProfile}
              className="flex items-center space-x-1.5 bg-emerald-900/70 hover:bg-emerald-900 text-xs px-2.5 py-1.5 rounded-full border border-emerald-400/50 transition"
              title="Click to view full student profile"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span className="font-semibold text-emerald-200">{studentId}</span>
            </button>

            <button
              onClick={onLogout}
              className="p-1.5 text-emerald-100 hover:text-white hover:bg-whatsapp-teal/80 rounded-full transition"
              title="Logout / Switch Student"
            >
              <LogOut className="w-4 h-4 text-rose-300 hover:text-rose-200" />
            </button>
          </>
        )}
      </div>
    </header>
  );
}

