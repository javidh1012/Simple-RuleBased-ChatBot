"""
attendance_rules.py - Attendance evaluation rules using Python conditional statements.
Section 8: Evaluates Attendance (%) and formats feedback without external AI.
"""

from typing import Dict, Any, Optional


def evaluate_attendance(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates attendance strictly via predefined Python conditional logic.
    """
    features = record.get("features_available", {})
    if not features.get("attendance", False):
        return {
            "available": False,
            "percentage": None,
            "status": "Unavailable",
            "advice": "Attendance data is not available in the current dataset records.",
            "chat_text": "Attendance data is not recorded in the academic dataset.",
        }

    raw_attendance = record.get("mapped_fields", {}).get("attendance")
    if raw_attendance is None:
        return {
            "available": False,
            "percentage": None,
            "status": "Missing",
            "advice": "Attendance record for your student profile is missing.",
            "chat_text": "Your attendance record could not be found in the dataset.",
        }

    attendance_pct = float(raw_attendance)

    # Predefined Python conditional evaluation rules (Section 8)
    if attendance_pct > 85.0:
        status = "Excellent"
        advice = "Excellent! Your attendance is very good. Keep it up!"
        badge_class = "badge-excellent"
    elif attendance_pct > 75.0 and attendance_pct <= 85.0:
        status = "Satisfactory"
        advice = "Your attendance is satisfactory (above the 75% requirement). Strive to maintain above 85% for academic honors eligibility."
        badge_class = "badge-satisfactory"
    elif attendance_pct == 75.0:
        status = "Minimum Safe Threshold"
        advice = "You are safe, but you are at the minimum attendance threshold. You must attend all upcoming classes regularly."
        badge_class = "badge-safe"
    elif attendance_pct >= 65.0 and attendance_pct < 75.0:
        status = "Warning (I Grade Risk)"
        advice = "You may receive an I Grade. Attend all classes regularly and contact your class advisor regarding your attendance."
        badge_class = "badge-warning"
    else:  # Below 65%
        status = "Critical Danger (High I Grade Risk)"
        advice = "You are in danger of receiving an I Grade. Contact your class advisor immediately. Submit all pending OD forms and medical certificates before I Grade processing."
        badge_class = "badge-danger"

    chat_text = (
        f"📅 Attendance Report:\n\n"
        f"• Recorded Attendance: {attendance_pct:.1f}%\n"
        f"• Status: {status}\n"
        f"• Minimum Required Threshold: 75.0%\n\n"
        f"Advice: {advice}"
    )

    return {
        "available": True,
        "percentage": attendance_pct,
        "status": status,
        "advice": advice,
        "badge_class": badge_class,
        "chat_text": chat_text,
    }

