"""
internal_rules.py - Internal examination evaluation rules.
Section 9: Evaluates Internal Test 1 and Internal Test 2 (scale: out of 40).
"""

from typing import Dict, Any, Optional


def _evaluate_single_test(score: Optional[float], test_name: str) -> Dict[str, Any]:
    """Helper to evaluate an individual test score out of 40."""
    if score is None:
        return {
            "score": None,
            "max_score": 40.0,
            "category": "Unavailable",
            "feedback": f"{test_name} score is not available in the dataset.",
            "badge_class": "badge-secondary",
        }

    score_val = float(score)

    # Predefined rules (Section 9):
    # 30–40: Excellent performance. Keep it up in the next internal examination.
    # 20–29: Needs improvement. Prepare better and aim for 30+ marks.
    # Below 20: Poor performance. Study harder and aim to pass the end-semester examination.
    if score_val >= 30.0:
        category = "Excellent Performance"
        feedback = "Excellent performance. Keep it up in the next internal examination."
        badge_class = "badge-excellent"
    elif score_val >= 20.0:
        category = "Needs Improvement"
        feedback = "Needs improvement. Prepare better and aim for 30+ marks."
        badge_class = "badge-warning"
    else:
        category = "Poor Performance"
        feedback = "Poor performance. Study harder and aim to pass the end-semester examination."
        badge_class = "badge-danger"

    percentage = round((score_val / 40.0) * 100.0, 1)

    return {
        "score": score_val,
        "max_score": 40.0,
        "percentage": percentage,
        "category": category,
        "feedback": feedback,
        "badge_class": badge_class,
    }


def evaluate_internal_marks(record: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates internal examination performance for Test 1 and Test 2."""
    features = record.get("features_available", {})
    has_test_1 = features.get("internal_test_1", False)
    has_test_2 = features.get("internal_test_2", False)

    if not has_test_1 and not has_test_2:
        return {
            "available": False,
            "message": "Internal examination information is not available in this dataset.",
            "test_1": None,
            "test_2": None,
            "average": None,
            "chat_text": "Internal examination marks are unavailable in the dataset records.",
        }

    fields = record.get("mapped_fields", {})
    t1_score = fields.get("internal_test_1")
    t2_score = fields.get("internal_test_2")

    t1_eval = _evaluate_single_test(t1_score, "Internal Test 1") if has_test_1 else None
    t2_eval = _evaluate_single_test(t2_score, "Internal Test 2") if has_test_2 else None

    # Calculate average
    valid_scores = [s for s in [t1_score, t2_score] if s is not None]
    avg_score = round(sum(valid_scores) / len(valid_scores), 1) if valid_scores else None

    # Determine trend
    trend = "Consistent"
    if t1_score is not None and t2_score is not None:
        diff = float(t2_score) - float(t1_score)
        if diff > 0:
            trend = f"Improved by +{diff:.1f} marks in Test 2"
        elif diff < 0:
            trend = f"Declined by {abs(diff):.1f} marks in Test 2"
        else:
            trend = "Consistent performance across both tests"

    # Formatted chat text
    lines = ["📝 Internal Examination Marks (Scale: Out of 40):\n"]
    if t1_eval and t1_eval["score"] is not None:
        lines.append(f"• Internal Test 1: {t1_eval['score']:.0f}/40 ({t1_eval['category']})")
        lines.append(f"  Feedback: {t1_eval['feedback']}\n")

    if t2_eval and t2_eval["score"] is not None:
        lines.append(f"• Internal Test 2: {t2_eval['score']:.0f}/40 ({t2_eval['category']})")
        lines.append(f"  Feedback: {t2_eval['feedback']}\n")

    if avg_score is not None:
        lines.append(f"• Internal Average: {avg_score}/40 ({(avg_score/40)*100:.1f}%)")
        lines.append(f"• Progress Trend: {trend}")

    return {
        "available": True,
        "test_1": t1_eval,
        "test_2": t2_eval,
        "average": avg_score,
        "average_percentage": round((avg_score / 40.0) * 100.0, 1) if avg_score is not None else None,
        "trend": trend,
        "chat_text": "\n".join(lines),
    }

