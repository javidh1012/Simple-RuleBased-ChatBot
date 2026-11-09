"""
verification.py - Student verification and secure session management for Flask backend.
Ensures student records are strictly isolated and protected by backend tokens.
"""

import secrets
import time
from functools import wraps
from typing import Dict, Any, Optional, Tuple
from flask import request, jsonify, g
from dataset import get_dataset
from config import SESSION_EXPIRY_HOURS


class SessionManager:
    def __init__(self, expiry_hours: int = SESSION_EXPIRY_HOURS):
        self.expiry_seconds = expiry_hours * 3600
        # token -> session dict
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, student_id: str) -> str:
        """Creates a cryptographically secure session token bound to the verified student_id."""
        token = secrets.token_urlsafe(32)
        now = time.time()
        self._sessions[token] = {
            "student_id": student_id.strip().upper(),
            "created_at": now,
            "last_active": now,
        }
        return token

    def validate_session(self, token: Optional[str]) -> Optional[str]:
        """Validates session token. Returns student_id if valid, None otherwise."""
        if not token:
            return None

        # Clean token (remove 'Bearer ' if present)
        token = token.strip()
        if token.lower().startswith("bearer "):
            token = token[7:].strip()

        session = self._sessions.get(token)
        if not session:
            return None

        now = time.time()
        # Check expiry
        if now - session["last_active"] > self.expiry_seconds:
            # Expired
            del self._sessions[token]
            return None

        # Update last active timestamp
        session["last_active"] = now
        return session["student_id"]

    def revoke_session(self, token: Optional[str]) -> bool:
        """Revokes an active session."""
        if not token:
            return False
        token = token.strip()
        if token.lower().startswith("bearer "):
            token = token[7:].strip()
        if token in self._sessions:
            del self._sessions[token]
            return True
        return False

    def verify_student(self, student_id: str) -> Tuple[bool, Optional[str], str]:
        """
        Verifies student ID against the CSV dataset.
        Returns: (success: bool, session_token: Optional[str], message: str)
        """
        if not student_id or not str(student_id).strip():
            return (
                False,
                None,
                "Student ID cannot be empty. Please enter your valid Student ID (e.g., S1000 to S2999).",
            )

        cleaned_id = str(student_id).strip().upper()
        dataset = get_dataset()

        if not dataset.student_exists(cleaned_id):
            return (
                False,
                None,
                f"Student ID '{student_id.strip()}' was not found in the university academic records. "
                "Please verify your credentials and try again (e.g., S1000 to S2999).",
            )

        token = self.create_session(cleaned_id)
        return (
            True,
            token,
            f"Verification successful! Welcome, Student {cleaned_id}. How can I assist your academic journey today?",
        )


# Global session manager instance
session_manager = SessionManager()


def get_session_manager() -> SessionManager:
    return session_manager


def require_student_session(f):
    """
    Flask decorator to protect student endpoints with backend session authentication.
    Extracts session token from Authorization (Bearer) or X-Session-Token header.
    Rejects requests without valid tokens.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization") or request.headers.get("X-Session-Token")
        if not token:
            return jsonify({
                "error": "Unauthorized",
                "detail": "Authentication required. Please enter your Student ID to begin."
            }), 401

        student_id = session_manager.validate_session(token)
        if not student_id:
            return jsonify({
                "error": "Unauthorized",
                "detail": "Session expired or invalid. Please re-enter your Student ID."
            }), 401

        g.student_id = student_id
        return f(*args, **kwargs)

    return decorated_function
