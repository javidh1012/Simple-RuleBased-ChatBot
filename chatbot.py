"""
chatbot.py - State-Driven Rule-Based Conversational Engine.
Manages states:
  - START: Initial empty state awaiting greeting
  - WAITING_FOR_STUDENT_ID: Greeting received, awaiting student ID
  - VERIFIED: Student authenticated, full menu accessible
100% Deterministic Python Conditional Statements (Zero External AI / LLMs).
"""

import string
import re
from typing import Dict, Any, Optional, List
from flask import session
from dataset import get_dataset
from attendance_rules import evaluate_attendance
from internal_rules import evaluate_internal_marks
from academic_rules import evaluate_academic_performance
from recommendations import generate_recommendations

# Conversation States
STATE_START = "START"
STATE_WAITING_FOR_ID = "WAITING_FOR_STUDENT_ID"
STATE_VERIFIED = "VERIFIED"

# Exact responses required by prompt
PROMPT_GREETING_RESPONSE = (
    "Hello! Welcome to Student Academic Assistant! I'm here to help you understand your academic performance. "
    "To continue, please enter your Student ID."
)

PROMPT_INVALID_ID_RESPONSE = (
    "Sorry! The Student ID you entered was not found. Please check your ID and try again."
)

PROMPT_VERIFIED_RESPONSE = (
    "Student verified successfully! Welcome. How can I help you today?"
)

# Verified menu options
VERIFIED_MENU = [
    {"id": "profile", "label": "1. My Profile", "command": "1"},
    {"id": "attendance", "label": "2. Attendance Report", "command": "2"},
    {"id": "internals", "label": "3. Internal Marks", "command": "3"},
    {"id": "performance", "label": "4. Academic Performance", "command": "4"},
    {"id": "recommendations", "label": "5. Study Recommendations", "command": "5"},
    {"id": "logout", "label": "6. Logout", "command": "6"},
]

RECOGNIZED_GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good evening",
}


def normalize_message(message: str) -> str:
    """
    Normalizes incoming messages:
    - Strips leading and trailing spaces.
    - Applies casefold() for Unicode-safe case insensitivity.
    - Strips edge punctuation while preserving inner characters.
    - Condenses multiple whitespace characters into single space.
    """
    if not message:
        return ""
    text = str(message).strip().casefold()
    text = text.strip(string.punctuation)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_greeting(normalized_message: str) -> bool:
    """Checks if message is a recognized greeting."""
    if normalized_message in RECOGNIZED_GREETINGS:
        return True
    # Also handle greetings with trailing punctuation or friendly prefixes
    for g in RECOGNIZED_GREETINGS:
        if normalized_message.startswith(g + " ") or normalized_message.endswith(" " + g):
            return True
    return False


def detect_menu_intent(normalized_message: str) -> Optional[str]:
    """Identifies verified menu options by number or keyword."""
    norm = normalized_message

    # 1. My Profile
    if norm in ["1", "my profile", "profile", "who am i", "student info", "details"]:
        return "PROFILE"

    # 2. Attendance Report
    if norm in ["2", "attendance report", "attendance", "show attendance", "check attendance", "show my attendance"]:
        return "ATTENDANCE"

    # 3. Internal Marks
    if norm in [
        "3",
        "internal marks",
        "internals",
        "internal marks report",
        "check internal marks",
        "check my marks",
        "what about internal marks",
        "test marks",
    ]:
        return "INTERNAL_MARKS"

    # 4. Academic Performance
    if norm in [
        "4",
        "academic performance",
        "performance",
        "overall performance",
        "final marks",
        "final exam",
        "grades",
    ]:
        return "ACADEMIC_PERFORMANCE"

    # 5. Study Recommendations
    if norm in [
        "5",
        "study recommendations",
        "recommendations",
        "recommendation",
        "tips",
        "how to improve",
        "suggestions",
        "study advice",
    ]:
        return "RECOMMENDATIONS"

    # 6. Logout
    if norm in ["6", "logout", "log out", "exit", "quit", "sign out", "reset"]:
        return "LOGOUT"

    return None


def process_chat_message(user_message: str) -> Dict[str, Any]:
    """
    State machine controller:
    - START: Waiting for initial greeting.
    - WAITING_FOR_STUDENT_ID: Waiting for user to enter valid Student ID.
    - VERIFIED: Student authenticated; executing menu actions.
    """
    raw_text = (user_message or "").strip()
    norm_text = normalize_message(raw_text)

    # Current state from Flask session (default to START)
    current_state = session.get("state", STATE_START)
    student_id = session.get("student_id")

    # ------------------------------------------------------------------------
    # STATE 1: START (Initial state: user must send a greeting)
    # ------------------------------------------------------------------------
    if current_state == STATE_START:
        if is_greeting(norm_text):
            session["state"] = STATE_WAITING_FOR_ID
            return {
                "response": PROMPT_GREETING_RESPONSE,
                "state": STATE_WAITING_FOR_ID,
                "is_authenticated": False,
                "show_menu": False,
                "menu_options": [],
                "card_type": None,
                "card_data": None,
            }
        else:
            # User sent something other than a greeting before starting
            return {
                "response": "Please say 'Hi' or 'Hello' to begin.",
                "state": STATE_START,
                "is_authenticated": False,
                "show_menu": False,
                "menu_options": [],
                "card_type": None,
                "card_data": None,
            }

    # ------------------------------------------------------------------------
    # STATE 2: WAITING_FOR_STUDENT_ID
    # ------------------------------------------------------------------------
    if current_state == STATE_WAITING_FOR_ID:
        # Check if user says another greeting
        if is_greeting(norm_text):
            return {
                "response": "Please enter your Student ID to continue (e.g., S1000).",
                "state": STATE_WAITING_FOR_ID,
                "is_authenticated": False,
                "show_menu": False,
                "menu_options": [],
                "card_type": None,
                "card_data": None,
            }

        # Candidate student ID normalization
        candidate = raw_text.strip().strip(string.punctuation)
        # Extract last token if student entered "My id is S1000"
        tokens = candidate.split()
        if len(tokens) > 1:
            candidate = tokens[-1].strip(string.punctuation)

        if candidate.isdigit():
            candidate = f"S{candidate}"

        ds = get_dataset()
        if ds.student_exists(candidate):
            # Student verified!
            record = ds.get_student_record(candidate)
            canonical_id = record["student_id"] if record else candidate.upper()

            session["state"] = STATE_VERIFIED
            session["student_id"] = canonical_id
            session.permanent = True

            return {
                "response": PROMPT_VERIFIED_RESPONSE,
                "state": STATE_VERIFIED,
                "is_authenticated": True,
                "student_id": canonical_id,
                "show_menu": True,
                "menu_options": VERIFIED_MENU,
                "card_type": "welcome_verified",
                "card_data": {"student_id": canonical_id},
            }
        else:
            # Student ID not found
            return {
                "response": PROMPT_INVALID_ID_RESPONSE,
                "state": STATE_WAITING_FOR_ID,
                "is_authenticated": False,
                "show_menu": False,
                "menu_options": [],
                "card_type": None,
                "card_data": None,
            }

    # ------------------------------------------------------------------------
    # STATE 3: VERIFIED (Student authenticated)
    # ------------------------------------------------------------------------
    if current_state == STATE_VERIFIED:
        if not student_id:
            # Session expired
            session["state"] = STATE_START
            session.pop("student_id", None)
            return {
                "response": "Session expired. Please say 'Hello' to start again.",
                "state": STATE_START,
                "is_authenticated": False,
                "show_menu": False,
                "menu_options": [],
                "card_type": None,
                "card_data": None,
            }

        ds = get_dataset()
        record = ds.get_student_record(student_id)
        if not record:
            session["state"] = STATE_START
            session.pop("student_id", None)
            return {
                "response": "Student record could not be found. Session reset.",
                "state": STATE_START,
                "is_authenticated": False,
                "show_menu": False,
                "menu_options": [],
                "card_type": None,
                "card_data": None,
            }

        intent = detect_menu_intent(norm_text)

        # 1. Logout
        if intent == "LOGOUT":
            session.clear()
            session["state"] = STATE_START
            return {
                "response": "You have been logged out. The session has been reset.",
                "state": STATE_START,
                "is_authenticated": False,
                "show_menu": False,
                "menu_options": [],
                "card_type": "logout",
                "card_data": None,
                "reset_chat": True,
            }

        # 2. My Profile
        if intent == "PROFILE":
            fields = record.get("mapped_fields", {})
            profile_lines = [
                f"👤 Student Profile ({student_id}):\n",
                f"• Student ID: {student_id}",
                f"• Attendance: {fields.get('attendance', 'N/A')}%",
                f"• Internal Test 1: {fields.get('internal_test_1', 'N/A')}/40",
                f"• Internal Test 2: {fields.get('internal_test_2', 'N/A')}/40",
                f"• Assignment Score: {fields.get('assignment', 'N/A')}/10",
                f"• Daily Study Hours: {fields.get('study_hours', 'N/A')} hrs/day",
                f"• Final Exam Marks: {fields.get('final_exam', 'N/A')}/100",
            ]
            return {
                "response": "\n".join(profile_lines),
                "state": STATE_VERIFIED,
                "is_authenticated": True,
                "student_id": student_id,
                "show_menu": True,
                "menu_options": VERIFIED_MENU,
                "card_type": "profile",
                "card_data": {"student_id": student_id, "fields": fields},
            }

        # 3. Attendance Report
        if intent == "ATTENDANCE":
            att_eval = evaluate_attendance(record)
            return {
                "response": att_eval["chat_text"],
                "state": STATE_VERIFIED,
                "is_authenticated": True,
                "student_id": student_id,
                "show_menu": True,
                "menu_options": VERIFIED_MENU,
                "card_type": "attendance",
                "card_data": att_eval,
            }

        # 4. Internal Marks
        if intent == "INTERNAL_MARKS":
            int_eval = evaluate_internal_marks(record)
            return {
                "response": int_eval["chat_text"],
                "state": STATE_VERIFIED,
                "is_authenticated": True,
                "student_id": student_id,
                "show_menu": True,
                "menu_options": VERIFIED_MENU,
                "card_type": "internals",
                "card_data": int_eval,
            }

        # 5. Academic Performance
        if intent == "ACADEMIC_PERFORMANCE":
            perf_eval = evaluate_academic_performance(record)
            return {
                "response": perf_eval["chat_text"],
                "state": STATE_VERIFIED,
                "is_authenticated": True,
                "student_id": student_id,
                "show_menu": True,
                "menu_options": VERIFIED_MENU,
                "card_type": "performance",
                "card_data": perf_eval,
            }

        # 6. Study Recommendations
        if intent == "RECOMMENDATIONS":
            rec_eval = generate_recommendations(record)
            return {
                "response": rec_eval["chat_text"],
                "state": STATE_VERIFIED,
                "is_authenticated": True,
                "student_id": student_id,
                "show_menu": True,
                "menu_options": VERIFIED_MENU,
                "card_type": "recommendations",
                "card_data": rec_eval,
            }

        # Fallback for unrecognized input in VERIFIED state
        return {
            "response": "Please choose an option from the menu (1-6) or click one of the buttons below.",
            "state": STATE_VERIFIED,
            "is_authenticated": True,
            "student_id": student_id,
            "show_menu": True,
            "menu_options": VERIFIED_MENU,
            "card_type": None,
            "card_data": None,
        }

    # Default fallback reset
    session["state"] = STATE_START
    return {
        "response": "Please say 'Hi' or 'Hello' to begin.",
        "state": STATE_START,
        "is_authenticated": False,
        "show_menu": False,
        "menu_options": [],
        "card_type": None,
        "card_data": None,
    }
