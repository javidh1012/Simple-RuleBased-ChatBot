"""
recommendations.py - Rule-based study recommendation engine.
Section 11: Identifies weak & strong areas, generating prioritized study advice.
"""

from typing import Dict, Any, List


def generate_recommendations(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates rule-based study recommendations prioritized by academic necessity.
    """
    fields = record.get("mapped_fields", {})

    att = fields.get("attendance")
    t1 = fields.get("internal_test_1")
    t2 = fields.get("internal_test_2")
    asg = fields.get("assignment")
    std = fields.get("study_hours")
    fnl = fields.get("final_exam")

    weak_areas: List[str] = []
    strong_areas: List[str] = []
    prioritized_actions: List[Dict[str, Any]] = []

    # 1. Attendance evaluation
    if att is not None:
        att_val = float(att)
        if att_val < 65.0:
            weak_areas.append(f"Attendance ({att_val:.1f}%) - Danger of I Grade")
            prioritized_actions.append({
                "priority": "High (Immediate)",
                "title": "Resolve Attendance Deficit",
                "action": "Contact your class advisor immediately. Submit all pending OD forms and medical certificates before I Grade processing.",
            })
        elif att_val < 75.0:
            weak_areas.append(f"Attendance ({att_val:.1f}%) - Below required 75%")
            prioritized_actions.append({
                "priority": "High",
                "title": "Attend All Upcoming Classes",
                "action": "Attend all lectures regularly to cross the mandatory 75% threshold and avert an I Grade.",
            })
        elif att_val >= 85.0:
            strong_areas.append(f"Attendance ({att_val:.1f}%) - Excellent discipline")
        else:
            strong_areas.append(f"Attendance ({att_val:.1f}%) - Safe threshold maintained")

    # 2. Internal marks evaluation
    internals_low = False
    if t1 is not None:
        t1_val = float(t1)
        if t1_val < 20.0:
            weak_areas.append(f"Internal Test 1 ({t1_val:.0f}/40) - Poor score")
            internals_low = True
        elif t1_val >= 30.0:
            strong_areas.append(f"Internal Test 1 ({t1_val:.0f}/40) - Excellent score")

    if t2 is not None:
        t2_val = float(t2)
        if t2_val < 20.0:
            weak_areas.append(f"Internal Test 2 ({t2_val:.0f}/40) - Poor score")
            internals_low = True
        elif t2_val >= 30.0:
            strong_areas.append(f"Internal Test 2 ({t2_val:.0f}/40) - Excellent score")

    if internals_low:
        prioritized_actions.append({
            "priority": "High",
            "title": "Internal Examination Recovery",
            "action": "Prepare better and aim for 30+ marks in your next examination. Seek doubts clarification with professors.",
        })

    # 3. Daily study hours evaluation
    if std is not None:
        std_val = float(std)
        if std_val < 3.0:
            weak_areas.append(f"Daily Study Hours ({std_val:.0f} hrs) - Below 3 hours standard")
            prioritized_actions.append({
                "priority": "Medium",
                "title": "Increase Daily Study Time",
                "action": "Increase your daily self-study to at least 3 hours daily. Divide revision into focused 45-minute sessions.",
            })
        else:
            strong_areas.append(f"Daily Study Hours ({std_val:.0f} hrs) - Solid self-study habit")

    # 4. Assignment score evaluation
    if asg is not None:
        asg_val = float(asg)
        if asg_val < 7.0:
            weak_areas.append(f"Assignment Score ({asg_val:.0f}/10) - Needs improvement")
            prioritized_actions.append({
                "priority": "Medium",
                "title": "Elevate Assignment Quality",
                "action": "Review assignment instructions early and seek feedback before final submission to maximize internal marks.",
            })
        else:
            strong_areas.append(f"Assignment Score ({asg_val:.0f}/10) - Consistent submissions")

    # 5. Final Exam evaluation
    if fnl is not None:
        fnl_val = float(fnl)
        if fnl_val < 40.0:
            weak_areas.append(f"Final Exam Marks ({fnl_val:.0f}/100) - Arrear / Fail status")
            prioritized_actions.append({
                "priority": "High (Immediate)",
                "title": "End-Semester Examination Remediation",
                "action": "Study harder and register for remedial classes to pass upcoming end-semester examinations.",
            })
        elif fnl_val < 50.0:
            weak_areas.append(f"Final Exam Marks ({fnl_val:.0f}/100) - Borderline pass")
            prioritized_actions.append({
                "priority": "Medium",
                "title": "Target Comprehensive Revision",
                "action": "Solve past semester examination papers to raise your score above 60%.",
            })
        elif fnl_val >= 70.0:
            strong_areas.append(f"Final Exam Marks ({fnl_val:.0f}/100) - First class performance")

    # Overall advice summary
    if len(weak_areas) >= 3 or any("Danger" in w for w in weak_areas):
        overall_advice = (
            "Your academic performance needs significant improvement. "
            "Focus on your weaker subjects, practice regularly and maintain consistent preparation."
        )
    elif len(weak_areas) > 0:
        overall_advice = (
            "Your academic performance is on track, but specific areas need attention. "
            "Prioritize your weaker areas while maintaining your strong study habits."
        )
    else:
        overall_advice = (
            "Outstanding academic discipline! Keep up the same effort across all subjects "
            "and continue consistent preparation for your upcoming examinations."
        )

    # Format chat text
    lines = [
        "🎯 Study Recommendations:\n",
        f"Advice: {overall_advice}\n",
    ]

    if weak_areas:
        lines.append("⚠️ Areas Requiring Attention:")
        for w in weak_areas:
            lines.append(f" • {w}")
        lines.append("")

    if strong_areas:
        lines.append("✨ Strong Academic Areas:")
        for s in strong_areas:
            lines.append(f" • {s}")
        lines.append("")

    if prioritized_actions:
        lines.append("📋 Prioritized Action Plan:")
        for idx, act in enumerate(prioritized_actions, 1):
            lines.append(f" {idx}. [{act['priority']}] {act['title']}: {act['action']}")

    return {
        "overall_advice": overall_advice,
        "weak_areas": weak_areas,
        "strong_areas": strong_areas,
        "prioritized_actions": prioritized_actions,
        "chat_text": "\n".join(lines),
    }

