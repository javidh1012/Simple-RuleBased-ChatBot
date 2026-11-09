"""
internal_rules.py - Internal examination evaluation rules and feedback.
Evaluates Internal Test 1 and Internal Test 2 strictly against predefined rules.
"""

from typing import Dict, Any, Optional
from config import THRESHOLDS


def _evaluate_single_test(score: Optional[float], test_name: str) -> Dict[str, Any]:
    """Helper to evaluate an individual test out of 40 according to predefined rules."""
    if score is None:
        return {
            "score": None,
            "max_score": THRESHOLDS.internal_max_marks,
            "category": "Unavailable",
            "feedback": f"{test_name} score is not recorded in the dataset.",
            "color": "gray",
        }

    score_val = float(score)

    # Predefined rules:
    # 30-40: Excellent performance.
    # 20-29: Needs improvement.
    # Below 20: Poor performance.
    if score_val >= THRESHOLDS.internal_excellent_min:  # 30-40
        category = "Excellent Performance"
        feedback = "Excellent performance. Keep up the same effort in your next internal examination."
        color = "emerald"
        badge = "🟢 High Scorer"
    elif score_val >= THRESHOLDS.internal_improvement_min:  # 20-29
        category = "Needs Improvement"
        feedback = "Needs improvement. Prepare better and aim for 30+ marks in your next examination."
        color = "amber"
        badge = "🟡 Moderate Performance"
    else:  # Below 20
        category = "Poor Performance"
        feedback = "Poor performance. Study harder and aim to pass your end-semester examination."
        color = "rose"
        badge = "🔴 Critical Academic Alert"

    percentage = (score_val / THRESHOLDS.internal_max_marks) * 100.0

    return {
        "score": score_val,
        "max_score": THRESHOLDS.internal_max_marks,
        "percentage": round(percentage, 1),
        "category": category,
        "badge": badge,
        "feedback": feedback,
        "color": color,
    }


def evaluate_internal_marks(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates both internal tests and computes composite performance metrics.
    """
    features = record.get("features_available", {})
    has_test_1 = features.get("internal_test_1", False)
    has_test_2 = features.get("internal_test_2", False)

    if not has_test_1 and not has_test_2:
        return {
            "available": False,
            "message": "The university dataset does not contain internal examination information.",
            "test_1": None,
            "test_2": None,
            "average": None,
            "chat_text": "ℹ️ *Internal Examination Marks:*\n\nThe university dataset does not contain internal examination information for this academic session.",
        }

    fields = record.get("mapped_fields", {})
    t1_score = fields.get("internal_test_1")
    t2_score = fields.get("internal_test_2")

    t1_eval = _evaluate_single_test(t1_score, "Internal Test 1") if has_test_1 else None
    t2_eval = _evaluate_single_test(t2_score, "Internal Test 2") if has_test_2 else None

    # Compute average if both tests are available
    valid_scores = [s for s in [t1_score, t2_score] if s is not None]
    avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else None

    # Trend calculation
    trend = "Neutral"
    trend_description = "Only one examination result available."
    if t1_score is not None and t2_score is not None:
        diff = float(t2_score) - float(t1_score)
        if diff > 0:
            trend = "Improving"
            trend_description = f"📈 Improved by +{diff:.1f} marks in Test 2!"
        elif diff < 0:
            trend = "Declining"
            trend_description = f"📉 Decreased by {abs(diff):.1f} marks in Test 2. Regain focus."
        else:
            trend = "Consistent"
            trend_description = "📊 Consistent performance across both internal assessments."

    # Build formatted chat text
    lines = ["📝 *INTERNAL EXAMINATION REPORT (Out of 40)*\n"]
    if t1_eval and t1_eval["score"] is not None:
        lines.append(f"• *Internal Test 1:* {t1_eval['score']:.0f}/40 ({t1_eval['category']})")
        lines.append(f"  └ _{t1_eval['feedback']}_")

    if t2_eval and t2_eval["score"] is not None:
        lines.append(f"• *Internal Test 2:* {t2_eval['score']:.0f}/40 ({t2_eval['category']})")
        lines.append(f"  └ _{t2_eval['feedback']}_")

    if avg_score is not None:
        lines.append(f"\n• *Internal Average:* {avg_score:.1f}/40 ({(avg_score/40)*100:.1f}%)")
        lines.append(f"• *Exam Trend:* {trend_description}")

    return {
        "available": True,
        "test_1": t1_eval,
        "test_2": t2_eval,
        "average": round(avg_score, 1) if avg_score is not None else None,
        "average_percentage": round((avg_score / 40.0) * 100.0, 1) if avg_score is not None else None,
        "trend": trend,
        "trend_description": trend_description,
        "chat_text": "\n".join(lines),
    }

