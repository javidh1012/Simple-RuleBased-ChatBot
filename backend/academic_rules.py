"""
academic_rules.py - Academic performance evaluation across all dataset metrics.
Evaluates Assignment Scores, Daily Study Hours, and Final Exam Marks using sensible, documented thresholds.
"""

from typing import Dict, Any, List, Optional
from config import THRESHOLDS
from attendance_rules import evaluate_attendance
from internal_rules import evaluate_internal_marks


def evaluate_assignment(score: Optional[float]) -> Dict[str, Any]:
    """Evaluates Assignment Score (out of 10)."""
    if score is None:
        return {
            "metric": "Assignment Score",
            "available": False,
            "raw_value": None,
            "display_value": "N/A",
            "scale": "out of 10",
            "status": "Unavailable",
            "explanation": "Assignment scores are not recorded in this dataset.",
            "suggestion": "Keep track of course assignments directly with your subject teacher.",
            "color": "gray",
        }

    val = float(score)
    if val >= THRESHOLDS.assignment_outstanding_min:  # 9-10
        status = "Outstanding"
        explanation = "High quality assignments submitted with thorough conceptual precision."
        suggestion = "Continue this diligence and assist peers in study groups."
        color = "emerald"
    elif val >= THRESHOLDS.assignment_good_min:  # 7-8
        status = "Good"
        explanation = "Consistent homework and assignment quality meeting course expectations."
        suggestion = "Aim for perfection by reviewing instructor feedback and edge cases."
        color = "green"
    elif val >= THRESHOLDS.assignment_average_min:  # 5-6
        status = "Average"
        explanation = "Assignments meet minimum submission standards but lack analytical depth."
        suggestion = "Review rubric guidelines before submitting and seek faculty help during office hours."
        color = "amber"
    else:  # Below 5
        status = "Needs Improvement"
        explanation = "Assignment score is substandard and adversely impacts internal assessment weighting."
        suggestion = "Complete all pending exercises immediately and attend remediation tutorials."
        color = "rose"

    return {
        "metric": "Assignment Score",
        "available": True,
        "raw_value": val,
        "display_value": f"{val:.0f} / 10",
        "scale": "out of 10",
        "status": status,
        "explanation": explanation,
        "suggestion": suggestion,
        "color": color,
    }


def evaluate_study_hours(hours: Optional[float]) -> Dict[str, Any]:
    """Evaluates Daily Study Hours (1 to 5 hours in dataset)."""
    if hours is None:
        return {
            "metric": "Daily Study Hours",
            "available": False,
            "raw_value": None,
            "display_value": "N/A",
            "scale": "hours / day",
            "status": "Unavailable",
            "explanation": "Daily study hour records are not available in this dataset.",
            "suggestion": "Maintain a personal study log to track self-study habits.",
            "color": "gray",
        }

    val = float(hours)
    if val >= THRESHOLDS.study_hours_high_min:  # 4-5 hours
        status = "Dedicated"
        explanation = "Excellent commitment to self-directed learning and revision outside classroom hours."
        suggestion = "Incorporate spaced repetition and active recall to maximize time efficiency."
        color = "emerald"
    elif val >= THRESHOLDS.study_hours_recommended_min:  # 3 hours
        status = "Balanced"
        explanation = "Healthy daily study routine supporting steady academic progression."
        suggestion = "Maintain this regular habit; increase slightly before major assessment weeks."
        color = "green"
    else:  # 1-2 hours
        status = "Insufficient"
        explanation = "Daily self-study hours are low, which significantly correlates with lower exam scores."
        suggestion = "Increase daily study time to at least 3 hours. Structure it with 45-minute focused blocks."
        color = "amber"

    return {
        "metric": "Daily Study Hours",
        "available": True,
        "raw_value": val,
        "display_value": f"{val:.0f} hrs/day",
        "scale": "hours / day",
        "status": status,
        "explanation": explanation,
        "suggestion": suggestion,
        "color": color,
    }


def evaluate_final_exam(marks: Optional[float]) -> Dict[str, Any]:
    """Evaluates Final Exam Marks (out of 100)."""
    if marks is None:
        return {
            "metric": "Final Exam Marks",
            "available": False,
            "raw_value": None,
            "display_value": "N/A",
            "scale": "out of 100",
            "status": "Unavailable",
            "grade": "N/A",
            "explanation": "Final examination marks are not published in this dataset.",
            "suggestion": "Consult the examination controller portal for official grade sheets.",
            "color": "gray",
        }

    val = float(marks)
    if val >= THRESHOLDS.final_distinction_min:  # 85-100
        status = "Distinction"
        grade = "Grade S (Outstanding)"
        explanation = "Exceptional mastery of course subjects and superior examination execution."
        suggestion = "Maintain competitive edge for placement honors, research, or higher studies."
        color = "emerald"
    elif val >= THRESHOLDS.final_first_class_min:  # 70-84
        status = "First Class"
        grade = "Grade A (Very Good)"
        explanation = "Strong academic comprehension with consistent performance across syllabus topics."
        suggestion = "Practice past high-difficulty papers to push into distinction range (85%+)."
        color = "green"
    elif val >= THRESHOLDS.final_second_class_min:  # 50-69
        status = "Second Class"
        grade = "Grade B (Above Average)"
        explanation = "Satisfactory pass performance, but indicates noticeable conceptual gaps."
        suggestion = "Identify weak topics, solve textbook example problems, and clarify doubts early."
        color = "amber"
    elif val >= THRESHOLDS.final_pass_min:  # 40-49
        status = "Pass Class"
        grade = "Grade C (Borderline Pass)"
        explanation = "Cleared minimum threshold, but is in vulnerable territory near failure."
        suggestion = "Urgent academic focus needed. Form study pairs and request remedial tutoring."
        color = "orange"
    else:  # Below 40
        status = "Arrear / Critical"
        grade = "Grade U / F (Fail)"
        explanation = "Failed to secure the mandatory 40% passing mark in the end semester examination."
        suggestion = "Meet course coordinator immediately. Register for remedial classes and re-evaluation."
        color = "rose"

    return {
        "metric": "Final Exam Marks",
        "available": True,
        "raw_value": val,
        "display_value": f"{val:.0f} / 100",
        "scale": "out of 100",
        "status": status,
        "grade": grade,
        "explanation": explanation,
        "suggestion": suggestion,
        "color": color,
    }


def evaluate_overall_performance(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates all academic performance dimensions and calculates a normalized overall standing.
    """
    fields = record.get("mapped_fields", {})
    features = record.get("features_available", {})

    att_eval = evaluate_attendance(record)
    int_eval = evaluate_internal_marks(record)
    asg_eval = evaluate_assignment(fields.get("assignment") if features.get("assignment") else None)
    std_eval = evaluate_study_hours(fields.get("study_hours") if features.get("study_hours") else None)
    fnl_eval = evaluate_final_exam(fields.get("final_exam") if features.get("final_exam") else None)

    # Calculate composite academic score (weighted out of 100)
    # Final Exam: 50%, Internals: 30%, Assignments: 10%, Attendance: 10%
    score_components = []
    total_weights = 0.0
    accumulated_score = 0.0

    if fnl_eval["available"] and fnl_eval["raw_value"] is not None:
        accumulated_score += (fnl_eval["raw_value"] / 100.0) * 50.0
        total_weights += 50.0

    if int_eval["available"] and int_eval["average"] is not None:
        accumulated_score += (int_eval["average"] / 40.0) * 30.0
        total_weights += 30.0

    if asg_eval["available"] and asg_eval["raw_value"] is not None:
        accumulated_score += (asg_eval["raw_value"] / 10.0) * 10.0
        total_weights += 10.0

    if att_eval["available"] and att_eval["percentage"] is not None:
        accumulated_score += (att_eval["percentage"] / 100.0) * 10.0
        total_weights += 10.0

    composite_score = round((accumulated_score / total_weights) * 100.0, 1) if total_weights > 0 else None

    # Overall standing label
    if composite_score is not None:
        if composite_score >= 80:
            overall_standing = "Distinguished Scholar"
            overall_color = "emerald"
        elif composite_score >= 65:
            overall_standing = "Good Academic Standing"
            overall_color = "green"
        elif composite_score >= 50:
            overall_standing = "Satisfactory (Room for Growth)"
            overall_color = "amber"
        else:
            overall_standing = "Academic Warning (Support Required)"
            overall_color = "rose"
    else:
        overall_standing = "Record Incomplete"
        overall_color = "gray"

    # Chat summary text
    lines = [
        "📊 *COMPREHENSIVE ACADEMIC PERFORMANCE*\n",
        f"• *Overall Composite Rating:* {composite_score}% ({overall_standing})" if composite_score else "",
        f"• *Attendance:* {att_eval.get('percentage', 'N/A')}% ({att_eval.get('status', 'N/A')})",
        f"• *Internal Test 1:* {fields.get('internal_test_1', 'N/A')}/40",
        f"• *Internal Test 2:* {fields.get('internal_test_2', 'N/A')}/40",
        f"• *Assignment Score:* {asg_eval.get('display_value', 'N/A')} ({asg_eval.get('status', 'N/A')})",
        f"• *Daily Study Hours:* {std_eval.get('display_value', 'N/A')} ({std_eval.get('status', 'N/A')})",
        f"• *Final Exam Marks:* {fnl_eval.get('display_value', 'N/A')} ({fnl_eval.get('grade', 'N/A')})",
        "\n💡 _Select 'Study Recommendations' from the menu for targeted improvement steps._",
    ]

    return {
        "student_id": record["student_id"],
        "composite_score": composite_score,
        "overall_standing": overall_standing,
        "overall_color": overall_color,
        "metrics": {
            "attendance": att_eval,
            "internals": int_eval,
            "assignment": asg_eval,
            "study_hours": std_eval,
            "final_exam": fnl_eval,
        },
        "chat_text": "\n".join([line for line in lines if line]),
    }

