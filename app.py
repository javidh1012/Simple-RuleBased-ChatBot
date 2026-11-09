"""
app.py - Flask Application for Student Academic Assistant.
Simple, clean, normal chatbot interface (Zero WhatsApp styling, Zero Voice/Audio, Zero LLMs).
Powered strictly by Python conditional logic, Flask Sessions, and Pandas dataset.
"""

import os
from datetime import timedelta
from flask import Flask, render_template, request, jsonify, session, g

from dataset import get_dataset
from verification import (
    verify_student,
    establish_student_session,
    get_current_student_id,
    clear_student_session,
    require_session,
)
from attendance_rules import evaluate_attendance
from internal_rules import evaluate_internal_marks
from academic_rules import evaluate_academic_performance
from recommendations import generate_recommendations
from chatbot import process_chat_message, VERIFIED_MENU

app = Flask(__name__)

# Secret key for secure Flask session management
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "student_academic_assistant_flask_session_key_secret_2026_secure"
)

# Session configurations
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)


# ----------------------------------------------------------------------------
# Flask Routes
# ----------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    """
    GET / : Renders the clean, empty chatbot interface.
    Initial state: START (Empty conversation area, no welcome message, no menus).
    """
    if "state" not in session:
        session["state"] = "START"
    return render_template("index.html")


@app.route("/verify-student", methods=["POST"])
def verify_student_route():
    """
    POST /verify-student : Verifies Student ID and establishes Flask session.
    """
    data = request.get_json(silent=True) or {}
    raw_id = data.get("student_id", "")

    is_valid, verified_id, message = verify_student(raw_id)
    if not is_valid:
        return jsonify({
            "success": False,
            "student_id": None,
            "message": message,
        }), 404

    establish_student_session(verified_id)

    return jsonify({
        "success": True,
        "student_id": verified_id,
        "message": message,
        "menu_options": VERIFIED_MENU,
    }), 200


@app.route("/chat", methods=["POST"])
def chat():
    """
    POST /chat : Main conversational endpoint.
    Maintains session state (START -> WAITING_FOR_STUDENT_ID -> VERIFIED)
    and returns rule-based responses.
    """
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")

    result = process_chat_message(user_message)
    return jsonify(result), 200


@app.route("/student/profile", methods=["GET"])
@require_session
def student_profile():
    """
    GET /student/profile : Retrieve verified student's profile.
    Protected by Flask session.
    """
    student_id = g.student_id
    ds = get_dataset()
    record = ds.get_student_record(student_id)
    if not record:
        return jsonify({"error": "Not Found", "message": "Student record not found."}), 404

    fields = record.get("mapped_fields", {})
    return jsonify({
        "student_id": student_id,
        "features_available": record.get("features_available", {}),
        "profile": {
            "student_id": student_id,
            "attendance_percentage": fields.get("attendance"),
            "internal_test_1": fields.get("internal_test_1"),
            "internal_test_2": fields.get("internal_test_2"),
            "assignment_score": fields.get("assignment"),
            "daily_study_hours": fields.get("study_hours"),
            "final_exam_marks": fields.get("final_exam"),
        },
    }), 200


@app.route("/student/attendance", methods=["GET"])
@require_session
def student_attendance():
    """
    GET /student/attendance : Retrieve attendance report.
    Protected by Flask session.
    """
    student_id = g.student_id
    ds = get_dataset()
    record = ds.get_student_record(student_id)
    if not record:
        return jsonify({"error": "Not Found", "message": "Student record not found."}), 404

    return jsonify(evaluate_attendance(record)), 200


@app.route("/student/internal-marks", methods=["GET"])
@require_session
def student_internal_marks():
    """
    GET /student/internal-marks : Retrieve internal examination marks.
    Protected by Flask session.
    """
    student_id = g.student_id
    ds = get_dataset()
    record = ds.get_student_record(student_id)
    if not record:
        return jsonify({"error": "Not Found", "message": "Student record not found."}), 404

    return jsonify(evaluate_internal_marks(record)), 200


@app.route("/student/performance", methods=["GET"])
@require_session
def student_performance():
    """
    GET /student/performance : Retrieve comprehensive academic performance.
    Protected by Flask session.
    """
    student_id = g.student_id
    ds = get_dataset()
    record = ds.get_student_record(student_id)
    if not record:
        return jsonify({"error": "Not Found", "message": "Student record not found."}), 404

    return jsonify(evaluate_academic_performance(record)), 200


@app.route("/student/recommendations", methods=["GET"])
@require_session
def student_recommendations():
    """
    GET /student/recommendations : Retrieve rule-based study recommendations.
    Protected by Flask session.
    """
    student_id = g.student_id
    ds = get_dataset()
    record = ds.get_student_record(student_id)
    if not record:
        return jsonify({"error": "Not Found", "message": "Student record not found."}), 404

    return jsonify(generate_recommendations(record)), 200


@app.route("/logout", methods=["POST"])
def logout():
    """
    POST /logout : Resets session to START state.
    """
    clear_student_session()
    return jsonify({
        "success": True,
        "state": "START",
        "message": "Logged out successfully. Session reset."
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Public health check endpoint."""
    ds = get_dataset()
    return jsonify({
        "status": "healthy",
        "service": "Student Academic Assistant (Flask)",
        "total_students": ds.total_records,
        "dataset_columns": ds.get_metadata()["detected_columns"],
    }), 200


@app.route("/dataset/info", methods=["GET"])
def dataset_info():
    """Public dataset inspection endpoint."""
    ds = get_dataset()
    return jsonify(ds.get_metadata()), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 70)
    print("🎓 STUDENT ACADEMIC ASSISTANT - FLASK CHATBOT")
    print("=" * 70)
    print("• Layout: Simple, Clean, Modern Normal Chatbot (Zero WhatsApp UI)")
    print("• Dataset: Kaggle Student Academic Performance (2,000 students)")
    print("• Rule Engine: 100% Deterministic Python Conditional Statements")
    print("• Input Mode: Pure Text (Zero Voice/Audio)")
    print(f"• Web Interface: http://127.0.0.1:{port}")
    print("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=True)
