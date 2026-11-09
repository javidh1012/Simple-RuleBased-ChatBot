"""
chatbot.py - Rule-based response manager and intent dispatcher.
Pure Python conditional logic with zero LLM API dependency.
"""

from typing import Dict, Any, List, Optional
import re
from dataset import get_dataset
from verification import get_session_manager
from attendance_rules import evaluate_attendance
from internal_rules import evaluate_internal_marks
from academic_rules import evaluate_overall_performance
from recommendations import generate_recommendations

WELCOME_MESSAGE = (
    "Hello! 👋 Welcome to Student Academic Assistant.\n\n"
    "I'm your personal academic assistant. I can help you understand your attendance, "
    "internal examination performance and academic progress.\n\n"
    "To get started, please enter your Student ID (e.g., *S1000* to *S2999*)."
)

HELP_MESSAGE = (
    "💡 *STUDENT ACADEMIC ASSISTANT - HELP & SUPPORT*\n\n"
    "You can interact with me by tapping the quick buttons below or simply typing:\n"
    "• Type *1* or *Profile* – View your registered student profile\n"
    "• Type *2* or *Attendance* – Detailed attendance breakdown & I Grade status\n"
    "• Type *3* or *Internals* – Internal Test 1 & 2 scores (out of 40)\n"
    "• Type *4* or *Performance* – Complete academic metrics & final marks\n"
    "• Type *5* or *Recommendations* – Actionable study improvement plan\n"
    "• Type *6* or *Help* – Display this help menu\n"
    "• Type *Logout* – Exit session and switch Student ID\n\n"
    "Need academic office assistance? Email: advisor@university.edu | Ext: 4040"
)

MAIN_MENU_BUTTONS = [
    {"id": "profile", "label": "👤 1. My Profile", "command": "1"},
    {"id": "attendance", "label": "📅 2. Attendance Report", "command": "2"},
    {"id": "internals", "label": "📝 3. Internal Marks", "command": "3"},
    {"id": "performance", "label": "📊 4. Academic Performance", "command": "4"},
    {"id": "recommendations", "label": "🎯 5. Study Recommendations", "command": "5"},
    {"id": "help", "label": "❓ 6. Help & Support", "command": "6"},
]


class RuleBasedChatbot:
    def __init__(self):
        self.dataset = get_dataset()
        self.session_manager = get_session_manager()

    def process_message(self, message: str, session_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Pure rule-based message processor.
        Dispatches intents via Python conditional statements.
        """
        cleaned_msg = (message or "").strip()
        lower_msg = cleaned_msg.lower()

        # Check if user has an active, valid session
        student_id = self.session_manager.validate_session(session_token)

        # -------------------------------------------------------------
        # 1. UNAUTHENTICATED FLOW
        # -------------------------------------------------------------
        if not student_id:
            # Check for general greetings
            if lower_msg in ["hi", "hello", "hey", "start", "restart", "help"]:
                return {
                    "text": WELCOME_MESSAGE,
                    "session_token": None,
                    "student_id": None,
                    "is_authenticated": False,
                    "buttons": [],
                    "card_type": None,
                    "card_data": None,
                }

            # Attempt verification if user entered a string
            # Normalize potential student ID (e.g. S1000, s1000, 1000)
            candidate_id = cleaned_msg.upper()
            if candidate_id.isdigit():
                candidate_id = f"S{candidate_id}"

            success, new_token, verify_msg = self.session_manager.verify_student(candidate_id)
            if success and new_token:
                # Successfully verified!
                greeting_text = (
                    f"✅ *Verification Successful!*\n\n"
                    f"Welcome, *Student {candidate_id}* 🎓\n"
                    f"Your academic records have been securely loaded from the database.\n\n"
                    f"Please choose an option from the menu below or type a number (1-6):"
                )
                return {
                    "text": greeting_text,
                    "session_token": new_token,
                    "student_id": candidate_id,
                    "is_authenticated": True,
                    "buttons": MAIN_MENU_BUTTONS,
                    "card_type": "welcome_verified",
                    "card_data": {"student_id": candidate_id},
                }
            else:
                return {
                    "text": (
                        f"❌ *Student ID Not Found*\n\n"
                        f"Could not locate record for '{cleaned_msg}'.\n"
                        f"Please ensure you enter your valid university Student ID in the format *S1000* to *S2999*."
                    ),
                    "session_token": None,
                    "student_id": None,
                    "is_authenticated": False,
                    "buttons": [],
                    "card_type": None,
                    "card_data": None,
                }

        # -------------------------------------------------------------
        # 2. AUTHENTICATED FLOW
        # -------------------------------------------------------------
        student_record = self.dataset.get_student_record(student_id)
        if not student_record:
            return {
                "text": "⚠️ Error: Student record could not be retrieved. Please re-authenticate.",
                "session_token": None,
                "student_id": None,
                "is_authenticated": False,
                "buttons": [],
                "card_type": None,
                "card_data": None,
            }

        # Check for logout / switch intent
        if lower_msg in ["logout", "exit", "quit", "switch", "change student", "sign out"]:
            self.session_manager.revoke_session(session_token)
            return {
                "text": (
                    f"🔒 *Session Terminated*\n\n"
                    f"You have been successfully logged out of Student {student_id}'s account.\n\n"
                    f"To view another student's academic progress, please enter the new Student ID."
                ),
                "session_token": None,
                "student_id": None,
                "is_authenticated": False,
                "buttons": [],
                "card_type": "logout",
                "card_data": None,
            }

        # Menu Dispatch Logic via Python Conditional Statements:

        # 1. My Profile
        if lower_msg in ["1", "profile", "my profile", "who am i", "details", "info", "me"]:
            return self._handle_profile(student_id, student_record)

        # 2. Attendance Report
        if lower_msg in ["2", "attendance", "attendance report", "absent", "attendance percentage", "safe"]:
            return self._handle_attendance(student_id, student_record)

        # 3. Internal Examination Marks
        if lower_msg in [
            "3",
            "internals",
            "internal marks",
            "internal examination",
            "internal examination marks",
            "test 1",
            "test 2",
            "tests",
        ]:
            return self._handle_internals(student_id, student_record)

        # 4. Academic Performance
        if lower_msg in [
            "4",
            "performance",
            "academic performance",
            "overall",
            "final exam",
            "final marks",
            "assignment",
            "study hours",
            "grades",
        ]:
            return self._handle_performance(student_id, student_record)

        # 5. Study Recommendations
        if lower_msg in [
            "5",
            "recommendations",
            "study recommendations",
            "recommendation",
            "tips",
            "suggestions",
            "weak areas",
            "how to improve",
            "improve",
        ]:
            return self._handle_recommendations(student_id, student_record)

        # 6. Help & Support
        if lower_msg in ["6", "help", "support", "menu", "options", "commands"]:
            return {
                "text": HELP_MESSAGE,
                "session_token": session_token,
                "student_id": student_id,
                "is_authenticated": True,
                "buttons": MAIN_MENU_BUTTONS,
                "card_type": "help",
                "card_data": None,
            }

        # Fallback for unrecognized input
        return {
            "text": (
                f"I didn't quite catch that, *Student {student_id}*. 🤔\n\n"
                f"As a rule-based assistant, please choose one of the options below or type *1* through *6*:\n\n"
                f"1️⃣ My Profile\n"
                f"2️⃣ Attendance Report\n"
                f"3️⃣ Internal Marks\n"
                f"4️⃣ Academic Performance\n"
                f"5️⃣ Study Recommendations\n"
                f"6️⃣ Help & Support\n"
                f"*(Or type 'logout' to switch student)*"
            ),
            "session_token": session_token,
            "student_id": student_id,
            "is_authenticated": True,
            "buttons": MAIN_MENU_BUTTONS,
            "card_type": None,
            "card_data": None,
        }

    def _handle_profile(self, student_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Generates profile details response."""
        fields = record.get("mapped_fields", {})
        raw = record.get("raw_data", {})

        text = (
            f"👤 *STUDENT ACADEMIC PROFILE*\n\n"
            f"• *Student ID:* {student_id}\n"
            f"• *Dataset Status:* Verified Academic Record\n"
            f"• *Recorded Attendance:* {fields.get('attendance', 'N/A')}%\n"
            f"• *Internal Test 1:* {fields.get('internal_test_1', 'N/A')}/40\n"
            f"• *Internal Test 2:* {fields.get('internal_test_2', 'N/A')}/40\n"
            f"• *Assignment Score:* {fields.get('assignment', 'N/A')}/10\n"
            f"• *Daily Study Hours:* {fields.get('study_hours', 'N/A')} hrs\n"
            f"• *Final Exam Score:* {fields.get('final_exam', 'N/A')}/100\n\n"
            f"Select an option below to inspect specific evaluations:"
        )

        return {
            "text": text,
            "student_id": student_id,
            "is_authenticated": True,
            "buttons": MAIN_MENU_BUTTONS,
            "card_type": "profile",
            "card_data": {
                "student_id": student_id,
                "fields": fields,
            },
        }

    def _handle_attendance(self, student_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates attendance and returns formatted report."""
        att_data = evaluate_attendance(record)
        return {
            "text": att_data["chat_text"],
            "student_id": student_id,
            "is_authenticated": True,
            "buttons": [
                {"id": "internals", "label": "📝 Check Internal Marks", "command": "3"},
                {"id": "recommendations", "label": "🎯 Study Recommendations", "command": "5"},
                {"id": "menu", "label": "🏠 Main Menu", "command": "6"},
            ],
            "card_type": "attendance",
            "card_data": att_data,
        }

    def _handle_internals(self, student_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates internal examinations and returns formatted report."""
        internal_data = evaluate_internal_marks(record)
        return {
            "text": internal_data["chat_text"],
            "student_id": student_id,
            "is_authenticated": True,
            "buttons": [
                {"id": "performance", "label": "📊 Full Academic Performance", "command": "4"},
                {"id": "recommendations", "label": "🎯 Study Recommendations", "command": "5"},
                {"id": "menu", "label": "🏠 Main Menu", "command": "6"},
            ],
            "card_type": "internals",
            "card_data": internal_data,
        }

    def _handle_performance(self, student_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates overall academic performance."""
        perf_data = evaluate_overall_performance(record)
        return {
            "text": perf_data["chat_text"],
            "student_id": student_id,
            "is_authenticated": True,
            "buttons": [
                {"id": "recommendations", "label": "🎯 View Recommendations", "command": "5"},
                {"id": "attendance", "label": "📅 Attendance Report", "command": "2"},
                {"id": "menu", "label": "🏠 Main Menu", "command": "6"},
            ],
            "card_type": "performance",
            "card_data": perf_data,
        }

    def _handle_recommendations(self, student_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Generates prioritized study recommendations."""
        rec_data = generate_recommendations(record)
        return {
            "text": rec_data["chat_text"],
            "student_id": student_id,
            "is_authenticated": True,
            "buttons": [
                {"id": "profile", "label": "👤 View Profile", "command": "1"},
                {"id": "performance", "label": "📊 View Performance", "command": "4"},
                {"id": "menu", "label": "🏠 Main Menu", "command": "6"},
            ],
            "card_type": "recommendations",
            "card_data": rec_data,
        }


chatbot_instance = RuleBasedChatbot()


def get_chatbot() -> RuleBasedChatbot:
    return chatbot_instance

