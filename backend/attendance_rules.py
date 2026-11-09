"""
attendance_rules.py - Attendance evaluation rules and response formatting.
Evaluates attendance strictly based on predefined Python conditional statements.
"""

from typing import Dict, Any, Optional
from config import THRESHOLDS


def evaluate_attendance(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates attendance using rule-based Python logic.
    Returns structured evaluation with status, advice, color code, and formatting.
    """
    if not record.get("features_available", {}).get("attendance", False):
        return {
            "available": False,
            "message": "Attendance data is unavailable in the current university records dataset.",
            "percentage": None,
            "status": "Unavailable",
            "advice": "Please contact the academic office or registrar for your attendance records.",
            "color": "gray",
            "is_safe": False,
        }

    raw_attendance = record.get("mapped_fields", {}).get("attendance")
    if raw_attendance is None:
        return {
            "available": False,
            "message": "Attendance record for this student is missing or not recorded in the dataset.",
            "percentage": None,
            "status": "Missing",
            "advice": "Please reach out to your faculty advisor to update missing attendance entries.",
            "color": "gray",
            "is_safe": False,
        }

    attendance_pct = float(raw_attendance)

    # Predefined Python conditional evaluation rules
    if attendance_pct > THRESHOLDS.attendance_excellent_min:  # > 85%
        status = "Excellent"
        advice = "Excellent! Your attendance is very good. Keep it up!"
        color = "emerald"
        is_safe = True
        badge = "🟢 Top Tier Attendance"
    elif attendance_pct > THRESHOLDS.attendance_safe_threshold and attendance_pct <= THRESHOLDS.attendance_excellent_min:  # 75.1% - 85%
        status = "Good"
        advice = "Good! Your attendance is satisfactory and above the minimum requirement (75%), but strive to reach above 85% for distinction and honors eligibility."
        color = "green"
        is_safe = True
        badge = "🟢 Satisfactory Attendance"
    elif attendance_pct == THRESHOLDS.attendance_safe_threshold:  # == 75%
        status = "Borderline Safe"
        advice = "You are currently safe, but you are at the minimum attendance threshold. You must attend all upcoming classes regularly."
        color = "yellow"
        is_safe = True
        badge = "🟡 Minimum Threshold Warning"
    elif attendance_pct >= THRESHOLDS.attendance_warning_min and attendance_pct < THRESHOLDS.attendance_safe_threshold:  # 65% - 74.9%
        status = "Warning"
        advice = "Warning! Your attendance is below the required level. You may receive an I Grade. Attend all classes regularly and contact your class advisor regarding your attendance."
        color = "amber"
        is_safe = False
        badge = "🟠 Attendance Warning (I Grade Risk)"
    else:  # < 65%
        status = "Critical Warning"
        advice = "Critical Warning! You are at high risk of receiving an I Grade. Contact your class advisor immediately. Submit all pending OD forms and medical certificates before the I Grade processing."
        color = "rose"
        is_safe = False
        badge = "🔴 Critical Attendance Alert"

    # Formatted chat text response
    chat_text = (
        f"📋 *ATTENDANCE REPORT*\n\n"
        f"• *Recorded Attendance:* {attendance_pct:.1f}%\n"
        f"• *Status:* {badge}\n"
        f"• *Safe Threshold:* {THRESHOLDS.attendance_safe_threshold:.0f}%\n\n"
        f"💬 *Personalized Advice:*\n{advice}"
    )

    return {
        "available": True,
        "percentage": attendance_pct,
        "status": status,
        "badge": badge,
        "advice": advice,
        "color": color,
        "is_safe": is_safe,
        "safe_threshold": THRESHOLDS.attendance_safe_threshold,
        "excellent_threshold": THRESHOLDS.attendance_excellent_min,
        "chat_text": chat_text,
    }

