import React, { useEffect, useState } from 'react';
import { X, User, Calendar, BookOpen, Clock, FileCheck, GraduationCap, LogOut } from 'lucide-react';
import { api } from '../api/client';

export default function ProfileModal({ isOpen, onClose, sessionToken, onLogout, onSelectOption }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && sessionToken) {
      setLoading(true);
      api
        .getProfile(sessionToken)
        .then((data) => setProfile(data))
        .catch((err) => console.error(err))
        .finally(() => setLoading(false));
    }
  }, [isOpen, sessionToken]);

  if (!isOpen) return null;

  const prof = profile?.profile;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl max-w-md w-full overflow-hidden flex flex-col shadow-2xl border border-gray-200">
        {/* Header */}
        <div className="bg-whatsapp-dark text-white px-5 py-4 flex items-center justify-between border-b border-whatsapp-teal/40">
          <div className="flex items-center space-x-2.5">
            <div className="w-9 h-9 rounded-full bg-whatsapp-teal flex items-center justify-center text-white ring-2 ring-emerald-300">
              <User className="w-5 h-5" />
            </div>
            <div>
              <h2 className="font-bold text-base leading-tight">Student Profile</h2>
              <p className="text-xs text-emerald-200">Verified Academic Record</p>
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
        <div className="p-5 overflow-y-auto space-y-3 text-xs text-gray-700">
          {loading ? (
            <div className="py-8 text-center text-gray-500">Loading student details from database...</div>
          ) : prof ? (
            <>
              <div className="bg-emerald-50/80 border border-emerald-200 rounded-xl p-3 flex justify-between items-center">
                <div>
                  <span className="text-gray-500 text-[11px] block">Student Identifier</span>
                  <span className="text-lg font-extrabold text-whatsapp-dark">{prof.student_id}</span>
                </div>
                <span className="text-[11px] bg-emerald-200/80 text-emerald-900 font-bold px-2 py-0.5 rounded-full">
                  Active Verified Session
                </span>
              </div>

              {/* All 6 metrics grid */}
              <div className="grid grid-cols-2 gap-2">
                <div className="bg-gray-50 border border-gray-200 p-2.5 rounded-xl">
                  <div className="flex items-center space-x-1 text-gray-500 mb-0.5 text-[11px]">
                    <Calendar className="w-3.5 h-3.5 text-whatsapp-teal" />
                    <span>Attendance</span>
                  </div>
                  <span className="text-base font-extrabold text-gray-900">{prof.attendance_percentage}%</span>
                </div>

                <div className="bg-gray-50 border border-gray-200 p-2.5 rounded-xl">
                  <div className="flex items-center space-x-1 text-gray-500 mb-0.5 text-[11px]">
                    <Clock className="w-3.5 h-3.5 text-whatsapp-teal" />
                    <span>Daily Study</span>
                  </div>
                  <span className="text-base font-extrabold text-gray-900">{prof.daily_study_hours} hrs/day</span>
                </div>

                <div className="bg-gray-50 border border-gray-200 p-2.5 rounded-xl">
                  <div className="flex items-center space-x-1 text-gray-500 mb-0.5 text-[11px]">
                    <BookOpen className="w-3.5 h-3.5 text-whatsapp-teal" />
                    <span>Internal Test 1</span>
                  </div>
                  <span className="text-base font-extrabold text-gray-900">{prof.internal_test_1} / 40</span>
                </div>

                <div className="bg-gray-50 border border-gray-200 p-2.5 rounded-xl">
                  <div className="flex items-center space-x-1 text-gray-500 mb-0.5 text-[11px]">
                    <BookOpen className="w-3.5 h-3.5 text-whatsapp-teal" />
                    <span>Internal Test 2</span>
                  </div>
                  <span className="text-base font-extrabold text-gray-900">{prof.internal_test_2} / 40</span>
                </div>

                <div className="bg-gray-50 border border-gray-200 p-2.5 rounded-xl">
                  <div className="flex items-center space-x-1 text-gray-500 mb-0.5 text-[11px]">
                    <FileCheck className="w-3.5 h-3.5 text-whatsapp-teal" />
                    <span>Assignment</span>
                  </div>
                  <span className="text-base font-extrabold text-gray-900">{prof.assignment_score} / 10</span>
                </div>

                <div className="bg-gray-50 border border-gray-200 p-2.5 rounded-xl">
                  <div className="flex items-center space-x-1 text-gray-500 mb-0.5 text-[11px]">
                    <GraduationCap className="w-3.5 h-3.5 text-whatsapp-teal" />
                    <span>Final Exam</span>
                  </div>
                  <span className="text-base font-extrabold text-gray-900">{prof.final_exam_marks} / 100</span>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="pt-2 flex flex-wrap gap-1.5">
                <button
                  onClick={() => {
                    onClose();
                    onSelectOption('2', '2. Attendance Report');
                  }}
                  className="flex-1 bg-emerald-50 hover:bg-emerald-100 text-whatsapp-dark font-medium py-1.5 px-2 rounded-lg border border-emerald-200 text-center text-xs"
                >
                  📅 Attendance
                </button>
                <button
                  onClick={() => {
                    onClose();
                    onSelectOption('3', '3. Internal Marks');
                  }}
                  className="flex-1 bg-emerald-50 hover:bg-emerald-100 text-whatsapp-dark font-medium py-1.5 px-2 rounded-lg border border-emerald-200 text-center text-xs"
                >
                  📝 Internals
                </button>
                <button
                  onClick={() => {
                    onClose();
                    onSelectOption('5', '5. Study Recommendations');
                  }}
                  className="flex-1 bg-emerald-50 hover:bg-emerald-100 text-whatsapp-dark font-medium py-1.5 px-2 rounded-lg border border-emerald-200 text-center text-xs"
                >
                  🎯 Tips
                </button>
              </div>
            </>
          ) : (
            <p className="text-gray-500">Failed to load profile details.</p>
          )}
        </div>

        {/* Footer with Logout */}
        <div className="bg-gray-100 px-5 py-3 flex justify-between items-center border-t border-gray-200">
          <button
            onClick={() => {
              onClose();
              onLogout();
            }}
            className="flex items-center space-x-1.5 text-rose-600 hover:text-rose-700 text-xs font-semibold px-2 py-1 rounded transition"
          >
            <LogOut className="w-4 h-4" />
            <span>Switch / Logout</span>
          </button>
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

