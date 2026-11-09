"""
main.py - Flask Application for Student Academic Assistant.
Exposes clean REST APIs protected by backend session authentication.
Pure Python conditional statements and rule-based logic (Zero LLMs).
Also serves React frontend in production for single-command launch.
"""

from pathlib import Path
import logging
from flask import Flask, request, jsonify, g, send_from_directory
from flask_cors import CORS

from config import CORS_ORIGINS
from dataset import get_dataset
from verification import get_session_manager, require_student_session
from attendance_rules import evaluate_attendance
from internal_rules import evaluate_internal_marks
from academic_rules import evaluate_overall_performance
from recommendations import generate_recommendations
from chatbot import get_chatbot

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("academic_assistant_flask")

app = Flask(__name__)

# Enable CORS for React frontend development
CORS(
    app,
    resources={r"/*": {"origins": CORS_ORIGINS}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization", "X-Session-Token"],
    methods=["GET", "POST", "OPTIONS"]
)

# Path to built React frontend
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"


# -------------------------------------------------------------
# Public & Utility Endpoints
# -------------------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    ds = get_dataset()
    return jsonify({
        "status": "healthy",
        "framework": "Flask",
        "total_students": ds.total_records,
        "dataset_columns": ds.get_metadata()["detected_columns"],
    })


@app.route("/dataset/info", methods=["GET"])
def dataset_info():
    """Returns dataset columns and summary information without leaking student data."""
    ds = get_dataset()
    return jsonify(ds.get_metadata())


# -------------------------------------------------------------
# Section 12: API Endpoints (Flask Implementation)
# -------------------------------------------------------------

@app.route("/verify-student", methods=["POST"])
def verify_student():
    """
    Verifies student ID against CSV dataset.
    Establishes secure server-side session token upon success.
    """
    data = request.get_json(silent=True) or {}
    student_id = data.get("student_id", "")

    cleaned_id = str(student_id).strip().upper()
    if cleaned_id.isdigit():
        cleaned_id = f"S{cleaned_id}"

    manager = get_session_manager()
    success, token, message = manager.verify_student(cleaned_id)

    if not success:
        return jsonify({
            "success": False,
            "session_token": None,
            "student_id": None,
            "message": message,
            "welcome_text": ""
        }), 404

    welcome_text = (
        f"✅ *Verification Successful!*\n\n"
        f"Welcome, *Student {cleaned_id}* 🎓\n"
        f"Your academic records have been securely loaded from the database.\n\n"
        f"Please choose an option from the menu below or type a number (1-6):"
    )

    return jsonify({
        "success": True,
        "session_token": token,
        "student_id": cleaned_id,
        "message": message,
        "welcome_text": welcome_text,
    }), 200


@app.route("/logout", methods=["POST"])
def logout():
    """Revokes the current student session."""
    token = request.headers.get("Authorization") or request.headers.get("X-Session-Token")
    data = request.get_json(silent=True) or {}
    if not token and "session_token" in data:
        token = data["session_token"]

    manager = get_session_manager()
    revoked = manager.revoke_session(token)
    return jsonify({"success": revoked, "message": "Logged out successfully."}), 200


@app.route("/student/profile", methods=["GET"])
@require_student_session
def get_student_profile():
    """
    Protected endpoint: returns student profile metrics.
    Only accessible with valid session token (in g.student_id).
    """
    student_id = g.student_id
    ds = get_dataset()
    record = ds.get_student_record(student_id)
    if not record:
        return jsonify({"error": "Not Found", "detail": "Student record not found."}), 404

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
        "raw_data": record.get("raw_data", {}),
    }), 200


@app.route("/student/attendance", methods=["GET"])
@require_student_session
def get_student_attendance():
    """
    Protected endpoint: returns detailed attendance evaluation.
    Evaluates attendance strictly via predefined Python rules.
    """
    student_id = g.student_id
    ds = get_dataset()
    record = ds.get_student_record(student_id)
    if not record:
        return jsonify({"error": "Not Found", "detail": "Student record not found."}), 404

    return jsonify(evaluate_attendance(record)), 200


@app.route("/student/internal-marks", methods=["GET"])
@require_student_session
def get_student_internal_marks():
    """
    Protected endpoint: returns internal examination marks evaluation.
    Evaluates internal test 1 and internal test 2 (out of 40) via predefined rules.
    """
    student_id = g.student_id
    ds = get_dataset()
    record = ds.get_student_record(student_id)
    if not record:
        return jsonify({"error": "Not Found", "detail": "Student record not found."}), 404

    return jsonify(evaluate_internal_marks(record)), 200


@app.route("/student/performance", methods=["GET"])
@require_student_session
def get_student_performance():
    """
    Protected endpoint: returns comprehensive academic performance across all metrics.
    """
    student_id = g.student_id
    ds = get_dataset()
    record = ds.get_student_record(student_id)
    if not record:
        return jsonify({"error": "Not Found", "detail": "Student record not found."}), 404

    return jsonify(evaluate_overall_performance(record)), 200


@app.route("/student/recommendations", methods=["GET"])
@require_student_session
def get_student_recommendations():
    """
    Protected endpoint: returns rule-based study recommendations.
    Identifies weak and satisfactory areas and prioritizes actions.
    """
    student_id = g.student_id
    ds = get_dataset()
    record = ds.get_student_record(student_id)
    if not record:
        return jsonify({"error": "Not Found", "detail": "Student record not found."}), 404

    return jsonify(generate_recommendations(record)), 200


@app.route("/chat", methods=["POST"])
def chat():
    """
    Main conversational endpoint:
    - Handles greetings and unauthenticated ID entries
    - Verifies student IDs and generates session tokens
    - Dispatches rule-based responses for verified students
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    session_token = data.get("session_token") or request.headers.get("Authorization") or request.headers.get("X-Session-Token")

    bot = get_chatbot()
    response = bot.process_message(message, session_token)

    return jsonify({
        "text": response["text"],
        "session_token": response.get("session_token"),
        "student_id": response.get("student_id"),
        "is_authenticated": response.get("is_authenticated", False),
        "buttons": response.get("buttons", []),
        "card_type": response.get("card_type"),
        "card_data": response.get("card_data"),
    }), 200


# -------------------------------------------------------------
# Static Frontend Serving for Single-Command Deployment
# -------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    if FRONTEND_DIST.exists() and (FRONTEND_DIST / "index.html").exists():
        return send_from_directory(FRONTEND_DIST, "index.html")
    return jsonify({
        "service": "Student Academic Assistant API (Flask)",
        "type": "Rule-Based Engine (No LLMs)",
        "status": "online",
        "framework": "Flask",
        "frontend_status": "Build frontend with 'npm run build' inside /frontend directory.",
    })


@app.route("/<path:path>", methods=["GET"])
def static_proxy(path):
    if FRONTEND_DIST.exists() and (FRONTEND_DIST / path).exists():
        return send_from_directory(FRONTEND_DIST, path)
    if FRONTEND_DIST.exists() and (FRONTEND_DIST / "index.html").exists():
        return send_from_directory(FRONTEND_DIST, "index.html")
    return jsonify({"error": "Not Found"}), 404


if __name__ == "__main__":
    print("=" * 65)
    print("🎓 Student Academic Assistant (Flask + React) is starting...")
    print("🌐 Access Web App at: http://127.0.0.1:5000")
    print("⚙️  Zero LLMs: Powered strictly by Python rules and Kaggle dataset")
    print("=" * 65)
    app.run(host="127.0.0.1", port=5000, debug=True)
