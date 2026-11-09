"""
academic_rules.py - Academic performance evaluation across all available dataset metrics.
Section 10: Evaluates assignments, study hours, and final exam marks with sensible thresholds.
"""

from typing import Dict, Any, Optional
from attendance_rules import evaluate_attendance
from internal_rules import evaluate_internal_marks


def evaluate_assignment(score: Optional[float]) -> Dict[str, Any]:
    """Evaluates Assignment Score (out of 10). Observed range in dataset: 4 to 10."""
    if score is None:
        return {
            "metric": "Assignment Score",
            "available": False,
            "value": "N/A",
            "category": "Unavailable",
            "feedback": "Assignment marks are not recorded in this dataset.",
            "suggestion": "Keep track of course assignments directly with your professor.",
        }

    val = float(score)
    if val >= 9.0:
        category = "Outstanding"
        feedback = "High quality assignments submitted with clear conceptual accuracy."
        suggestion = "Continue this excellent standard throughout upcoming coursework."
    elif val >= 7.0:
        category = "Good"
        feedback = "Consistent assignment submissions meeting university criteria."
        suggestion = "Review assignment rubrics and aim for perfection in future submissions."
    elif val >= 5.0:
        category = "Average"
        feedback = "Satisfactory submissions, but lacks depth and detailed explanations."
        suggestion = "Spend more time reviewing instructor feedback before submitting."
    else:
        category = "Needs Improvement"
        feedback = "Substandard assignment marks affecting continuous assessment."
        suggestion = "Consult teaching assistants and complete all homework on schedule."

    return {
        "metric": "Assignment Score",
        "available": True,
        "value": f"{val:.0f}/10",
        "raw_value": val,
        "category": category,
        "feedback": feedback,
        "suggestion": suggestion,
    }


def evaluate_study_hours(hours: Optional[float]) -> Dict[str, Any]:
    """Evaluates Daily Study Hours. Observed range in dataset: 1 to 5 hours/day."""
    if hours is None:
        return {
            "metric": "Daily Study Hours",
            "available": False,
            "value": "N/A",
            "category": "Unavailable",
            "feedback": "Daily study hours are not available in this dataset.",
            "suggestion": "Maintain a daily personal study journal.",
        }

    val = float(hours)
    if val >= 4.0:
        category = "Dedicated"
        feedback = "Strong commitment to independent revision outside classroom lectures."
        suggestion = "Maintain this regular habit; avoid fatigue through balanced breaks."
    elif val >= 3.0:
        category = "Balanced"
        feedback = "Healthy daily study schedule supporting steady academic progress."
        suggestion = "Increase to 4 hours during examination preparation periods."
    else:
        category = "Low"
        feedback = "Daily study time is below the recommended 3-hour academic guideline."
        suggestion = "Gradually expand your daily study schedule to at least 3 hours."

    return {
        "metric": "Daily Study Hours",
        "available": True,
        "value": f"{val:.0f} hrs/day",
        "raw_value": val,
        "category": category,
        "feedback": feedback,
        "suggestion": suggestion,
    }


def evaluate_final_exam(marks: Optional[float]) -> Dict[str, Any]:
    """Evaluates Final Exam Marks (out of 100). Observed range in dataset: 25 to 100."""
    if marks is None:
        return {
            "metric": "Final Exam Marks",
            "available": False,
            "value": "N/A",
            "grade": "N/A",
            "category": "Unavailable",
            "feedback": "Final examination marks are not published in this dataset.",
            "suggestion": "Check with the university examination portal for official grade cards.",
        }

    val = float(marks)
    if val >= 85.0:
        grade = "Grade S (Distinction)"
        category = "Distinction"
        feedback = "Exceptional performance demonstrating mastery of all syllabus units."
        suggestion = "Keep up this high caliber for academic honors and placement."
    elif val >= 70.0:
        grade = "Grade A (First Class)"
        category = "First Class"
        feedback = "Strong academic comprehension with consistent examination scores."
        suggestion = "Target the top distinction bracket (85%+) by solving advanced problem sets."
    elif val >= 50.0:
        grade = "Grade B (Second Class)"
        category = "Second Class"
        feedback = "Pass performance, but there is significant room for concept consolidation."
        suggestion = "Identify weaker units and create summary study sheets."
    elif val >= 40.0:
        grade = "Grade C (Pass)"
        category = "Borderline Pass"
        feedback = "Met minimum passing criteria, but vulnerable to falling behind."
        suggestion = "Urgent revision required. Join peer study circles and review past papers."
    else:
        grade = "Grade F / U (Fail / Arrear)"
        category = "Fail / Arrear Risk"
        feedback = "Below the mandatory 40% passing score in end-semester exams."
        suggestion = "Meet course coordinator immediately. Register for remedial classes."

    return {
        "metric": "Final Exam Marks",
        "available": True,
        "value": f"{val:.0f}/100",
        "raw_value": val,
        "grade": grade,
        "category": category,
        "feedback": feedback,
        "suggestion": suggestion,
    }


def evaluate_academic_performance(record: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates all academic dimensions available in the dataset."""
    fields = record.get("mapped_fields", {})
    features = record.get("features_available", {})

    att = evaluate_attendance(record)
    internals = evaluate_internal_marks(record)
    assignment = evaluate_assignment(fields.get("assignment") if features.get("assignment") else None)
    study_hours = evaluate_study_hours(fields.get("study_hours") if features.get("study_hours") else None)
    final_exam = evaluate_final_exam(fields.get("final_exam") if features.get("final_exam") else None)

    # Calculate overall standing
    scores = []
    if final_exam["available"] and final_exam["raw_value"] is not None:
        scores.append(final_exam["raw_value"])
    if internals["available"] and internals["average_percentage"] is not None:
        scores.append(internals["average_percentage"])
    if att["available"] and att["percentage"] is not None:
        scores.append(att["percentage"])

    avg_performance = round(sum(scores) / len(scores), 1) if scores else None

    if avg_performance is not None:
        if avg_performance >= 80.0:
            overall_status = "Distinguished Academic Standing"
        elif avg_performance >= 65.0:
            overall_status = "Good Academic Standing"
        elif avg_performance >= 50.0:
            overall_status = "Satisfactory (Requires Improvement)"
        else:
            overall_status = "Academic Warning (Support Required)"
    else:
        overall_status = "Information Incomplete"

    lines = [
        "📊 Academic Performance Summary:\n",
        f"• Overall Status: {overall_status}",
        f"• Attendance: {att.get('percentage', 'N/A')}% ({att.get('status', 'N/A')})",
        f"• Internal Test 1: {fields.get('internal_test_1', 'N/A')}/40",
        f"• Internal Test 2: {fields.get('internal_test_2', 'N/A')}/40",
        f"• Assignment Score: {assignment.get('value', 'N/A')} ({assignment.get('category', 'N/A')})",
        f"• Daily Study Hours: {study_hours.get('value', 'N/A')} ({study_hours.get('category', 'N/A')})",
        f"• Final Exam Marks: {final_exam.get('value', 'N/A')} ({final_exam.get('grade', 'N/A')})",
    ]

    return {
        "student_id": record["student_id"],
        "overall_status": overall_status,
        "average_performance": avg_performance,
        "metrics": {
            "attendance": att,
            "internals": internals,
            "assignment": assignment,
            "study_hours": study_hours,
            "final_exam": final_exam,
        },
        "chat_text": "\n".join(lines),
    }

