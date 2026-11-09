"""
verification.py - Student verification and Flask session management.
Protects academic routes and manages session authentication state.
"""

from functools import wraps
from typing import Tuple, Optional
from flask import session, jsonify, g
from dataset import get_dataset


def verify_student(student_id: str) -> Tuple[bool, Optional[str], str]:
    """
    Verifies student ID against the CSV dataset using case-insensitive matching.
    Returns: (is_valid, matched_student_id, message)
    """
    if not student_id or not str(student_id).strip():
        return (
            False,
            None,
            "Sorry! The Student ID you entered was not found. Please check your ID and try again."
        )

    cleaned_id = str(student_id).strip()
    if cleaned_id.isdigit():
        cleaned_id = f"S{cleaned_id}"

    ds = get_dataset()
    if not ds.student_exists(cleaned_id):
        return (
            False,
            None,
            "Sorry! The Student ID you entered was not found. Please check your ID and try again."
        )

    record = ds.get_student_record(cleaned_id)
    canonical_id = record["student_id"] if record else cleaned_id.upper()

    return (
        True,
        canonical_id,
        "Student verified successfully! Welcome. How can I help you today?"
    )


def establish_student_session(student_id: str) -> None:
    """Stores the verified student ID into the secure Flask session."""
    session["student_id"] = student_id
    session["state"] = "VERIFIED"
    session.permanent = True


def get_current_student_id() -> Optional[str]:
    """Retrieves authenticated student ID from Flask session."""
    return session.get("student_id")


def clear_student_session() -> None:
    """Clears the authenticated student session and resets state."""
    session.clear()
    session["state"] = "START"


def require_session(f):
    """
    Flask decorator enforcing student session authentication.
    Restricts route access to verified students only.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        student_id = get_current_student_id()
        current_state = session.get("state")

        if not student_id or current_state != "VERIFIED":
            return jsonify({
                "error": "Unauthorized",
                "message": "Authentication required. Please verify your Student ID."
            }), 401

        ds = get_dataset()
        if not ds.student_exists(student_id):
            clear_student_session()
            return jsonify({
                "error": "Unauthorized",
                "message": "Invalid session. Student record not found."
            }), 401

        g.student_id = student_id
        return f(*args, **kwargs)

    return decorated_function
