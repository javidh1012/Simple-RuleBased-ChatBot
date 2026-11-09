"""
recommendations.py - Rule-based study recommendation engine.
Identifies weak and satisfactory performance areas, prioritizing actionable guidance.
"""

from typing import Dict, Any, List
from config import THRESHOLDS


def generate_recommendations(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates rule-based study recommendations prioritized by academic urgency.
    """
    fields = record.get("mapped_fields", {})
    features = record.get("features_available", {})

    att = fields.get("attendance")
    t1 = fields.get("internal_test_1")
    t2 = fields.get("internal_test_2")
    asg = fields.get("assignment")
    std = fields.get("study_hours")
    fnl = fields.get("final_exam")

    weak_areas: List[Dict[str, Any]] = []
    satisfactory_areas: List[Dict[str, Any]] = []
    action_items: List[Dict[str, Any]] = []

    # 1. Evaluate Attendance Weakness / Strength
    if att is not None:
        att_val = float(att)
        if att_val < THRESHOLDS.attendance_warning_min:  # < 65%
            weak_areas.append({
                "area": "Classroom Attendance",
                "severity": "CRITICAL",
                "detail": f"Attendance is {att_val:.1f}%, far below the mandatory 75% threshold.",
            })
            action_items.append({
                "priority": 1,
                "urgency": "High",
                "title": "Resolve Attendance Deficit",
                "action": "Meet your class advisor immediately. Submit all pending OD/medical documentation to avert I Grade processing.",
            })
        elif att_val < THRESHOLDS.attendance_safe_threshold:  # 65-74%
            weak_areas.append({
                "area": "Classroom Attendance",
                "severity": "WARNING",
                "detail": f"Attendance is {att_val:.1f}%, which is in the risk zone for an I Grade.",
            })
            action_items.append({
                "priority": 1,
                "urgency": "High",
                "title": "Mandatory Class Attendance",
                "action": "Attend 100% of remaining scheduled lectures and labs without unexcused absences.",
            })
        elif att_val >= THRESHOLDS.attendance_excellent_min:
            satisfactory_areas.append({
                "area": "Classroom Attendance",
                "detail": f"Outstanding attendance at {att_val:.1f}%.",
            })
        else:
            satisfactory_areas.append({
                "area": "Classroom Attendance",
                "detail": f"Safe attendance at {att_val:.1f}%.",
            })

    # 2. Evaluate Internal Examinations
    internals_low = False
    if t1 is not None:
        t1_val = float(t1)
        if t1_val < THRESHOLDS.internal_improvement_min:
            internals_low = True
            weak_areas.append({
                "area": "Internal Test 1",
                "severity": "HIGH",
                "detail": f"Scored {t1_val:.0f}/40 (below 20 passing mark benchmark).",
            })
        elif t1_val >= THRESHOLDS.internal_excellent_min:
            satisfactory_areas.append({
                "area": "Internal Test 1",
                "detail": f"Scored {t1_val:.0f}/40 (Excellent 30+ marks).",
            })

    if t2 is not None:
        t2_val = float(t2)
        if t2_val < THRESHOLDS.internal_improvement_min:
            internals_low = True
            weak_areas.append({
                "area": "Internal Test 2",
                "severity": "HIGH",
                "detail": f"Scored {t2_val:.0f}/40 (below 20 passing mark benchmark).",
            })
        elif t2_val >= THRESHOLDS.internal_excellent_min:
            satisfactory_areas.append({
                "area": "Internal Test 2",
                "detail": f"Scored {t2_val:.0f}/40 (Excellent 30+ marks).",
            })

    if internals_low:
        action_items.append({
            "priority": 1,
            "urgency": "High",
            "title": "Internal Examination Recovery",
            "action": "Focus on your weaker test subjects. Solve previous year internal question sets and request faculty doubt-clearing sessions.",
        })
    elif (t1 is not None and float(t1) < 30) or (t2 is not None and float(t2) < 30):
        action_items.append({
            "priority": 2,
            "urgency": "Medium",
            "title": "Target 30+ in Internals",
            "action": "Strengthen conceptual clarity in mid-level topics to raise internal scores above 30 marks.",
        })

    # 3. Evaluate Daily Study Hours
    if std is not None:
        std_val = float(std)
        if std_val < THRESHOLDS.study_hours_recommended_min:
            weak_areas.append({
                "area": "Daily Study Hours",
                "severity": "MEDIUM",
                "detail": f"Currently dedicating {std_val:.0f} hr(s)/day to self-study, which is below the 3-hour recommendation.",
            })
            action_items.append({
                "priority": 2,
                "urgency": "Medium",
                "title": "Expand Daily Study Schedule",
                "action": f"Gradually increase self-study from {std_val:.0f} to at least 3 hours daily using focused 45-minute Pomodoro intervals.",
            })
        else:
            satisfactory_areas.append({
                "area": "Daily Study Habit",
                "detail": f"Consistent daily study routine ({std_val:.0f} hrs/day).",
            })

    # 4. Evaluate Assignment Scores
    if asg is not None:
        asg_val = float(asg)
        if asg_val < THRESHOLDS.assignment_good_min:
            weak_areas.append({
                "area": "Course Assignments",
                "severity": "MEDIUM",
                "detail": f"Assignment score is {asg_val:.0f}/10.",
            })
            action_items.append({
                "priority": 3,
                "urgency": "Moderate",
                "title": "Upgrade Assignment Quality",
                "action": "Review assignment rubrics in advance and submit well ahead of deadline for preliminary feedback.",
            })
        else:
            satisfactory_areas.append({
                "area": "Course Assignments",
                "detail": f"Reliable assignment submission ({asg_val:.0f}/10).",
            })

    # 5. Evaluate Final Exam Marks
    if fnl is not None:
        fnl_val = float(fnl)
        if fnl_val < THRESHOLDS.final_second_class_min:
            weak_areas.append({
                "area": "Final Exam Performance",
                "severity": "HIGH",
                "detail": f"Final examination score is {fnl_val:.0f}/100.",
            })
            action_items.append({
                "priority": 1,
                "urgency": "High",
                "title": "Intensive End-Semester Preparation",
                "action": "Construct a systematic chapter revision calendar. Practice full-length 3-hour mock tests every weekend.",
            })
        elif fnl_val >= THRESHOLDS.final_first_class_min:
            satisfactory_areas.append({
                "area": "Final Exam Performance",
                "detail": f"Strong score of {fnl_val:.0f}/100.",
            })

    # Sort actions by priority (1 is most urgent)
    action_items.sort(key=lambda x: x["priority"])

    # Determine overall diagnostic summary
    if len(weak_areas) >= 3 or any(w.get("severity") == "CRITICAL" for w in weak_areas):
        overall_status = "Needs Urgent Intervention"
        summary = (
            "Your academic performance needs significant improvement. Focus immediately on your critical "
            "weak areas, practice regularly and maintain consistent preparation."
        )
    elif len(weak_areas) > 0:
        overall_status = "Needs Targeted Improvement"
        summary = (
            "Your academic performance shows solid potential with a few specific areas requiring attention. "
            "Focus on your weaker subjects, practice regularly and maintain consistent daily preparation."
        )
    else:
        overall_status = "Commendable Standing"
        summary = (
            "Excellent academic consistency! Maintain your dedicated study habits, continue active class participation, "
            "and explore advanced problem solving for honours distinction."
        )

    # Format WhatsApp text
    lines = [
        "🎯 *PERSONALIZED STUDY RECOMMENDATIONS*\n",
        f"📌 *Diagnostic Summary:* _{summary}_\n",
    ]

    if weak_areas:
        lines.append("⚠️ *Identified Focus Areas (Need Attention):*")
        for w in weak_areas:
            lines.append(f" • *{w['area']}* [{w.get('severity', 'Warning')}]: {w['detail']}")
        lines.append("")

    if satisfactory_areas:
        lines.append("✨ *Academic Strengths:*")
        for s in satisfactory_areas:
            lines.append(f" • *{s['area']}:* {s['detail']}")
        lines.append("")

    if action_items:
        lines.append("📋 *Prioritized Action Plan:*")
        for idx, act in enumerate(action_items, 1):
            badge = "🔴" if act["urgency"] == "High" else ("🟡" if act["urgency"] == "Medium" else "🟢")
            lines.append(f" {idx}. {badge} *{act['title']}* (Priority: {act['urgency']})")
            lines.append(f"    └ {act['action']}")

    return {
        "overall_status": overall_status,
        "summary": summary,
        "weak_areas": weak_areas,
        "satisfactory_areas": satisfactory_areas,
        "action_items": action_items,
        "chat_text": "\n".join(lines),
    }

