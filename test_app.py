"""
test_app.py - Automated tests for the updated state-based chatbot flow.
Tests the exact sequence:
  1. Initial empty conversation area
  2. Greeting recognition (HI, hello, Good morning, etc.)
  3. WAITING_FOR_STUDENT_ID transition
  4. Invalid ID rejection
  5. Valid ID verification & VERIFIED state transition
  6. Menu options execution (Profile, Attendance, Internals, Performance, Recommendations)
  7. Logout and session reset to START
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from app import app
from chatbot import (
    normalize_message,
    is_greeting,
    PROMPT_GREETING_RESPONSE,
    PROMPT_INVALID_ID_RESPONSE,
    PROMPT_VERIFIED_RESPONSE,
)


def test_greeting_normalization():
    print("Testing greeting normalization with casefold()...")
    greetings = [
        "HI", "hi", "Hi",
        "HELLO", "hello", "Hello",
        "Hey", "hey",
        "Good morning", "GOOD MORNING", "good morning",
        "Good evening", "GOOD EVENING",
    ]
    for g in greetings:
        norm = normalize_message(g)
        assert is_greeting(norm), f"Failed greeting recognition for {g!r}"

    print("✅ All greeting variations recognized successfully.")


def test_conversation_state_flow():
    print("Testing complete conversation state machine...")
    client = app.test_client()

    # Step 1: Initial page load (GET /)
    res = client.get("/")
    assert res.status_code == 200
    # Confirm initial HTML has empty messages list (no welcome message)
    assert b"Hello! Welcome to Student Academic Assistant" not in res.data
    assert b"Student Academic Assistant" in res.data

    # Step 2: Sending a random message before greeting
    res = client.post("/chat", json={"message": "check attendance"})
    assert res.status_code == 200
    assert res.json["state"] == "START"
    assert "Please say 'Hi' or 'Hello' to begin" in res.json["response"]

    # Step 3: Sending a greeting (e.g. 'HI')
    res = client.post("/chat", json={"message": "HI"})
    assert res.status_code == 200
    data = res.json
    assert data["state"] == "WAITING_FOR_STUDENT_ID"
    assert data["response"] == PROMPT_GREETING_RESPONSE
    assert data["show_menu"] is False

    # Step 4: Entering an invalid Student ID
    res = client.post("/chat", json={"message": "INVALID_ID_999"})
    assert res.status_code == 200
    data = res.json
    assert data["state"] == "WAITING_FOR_STUDENT_ID"
    assert data["response"] == PROMPT_INVALID_ID_RESPONSE
    assert data["show_menu"] is False

    # Step 5: Entering a valid Student ID (e.g. 's1000' or 'S1000')
    res = client.post("/chat", json={"message": "S1000"})
    assert res.status_code == 200
    data = res.json
    assert data["state"] == "VERIFIED"
    assert data["response"] == PROMPT_VERIFIED_RESPONSE
    assert data["is_authenticated"] is True
    assert data["student_id"] == "S1000"
    assert data["show_menu"] is True
    assert len(data["menu_options"]) == 6

    # Step 6: Testing Menu Option 2 (Attendance Report)
    res = client.post("/chat", json={"message": "2"})
    assert res.status_code == 200
    data = res.json
    assert data["state"] == "VERIFIED"
    assert "Attendance Report" in data["response"]
    assert "84.0%" in data["response"]

    # Step 7: Testing natural language attendance in verified state
    res = client.post("/chat", json={"message": "show my attendance"})
    assert res.status_code == 200
    assert "Attendance Report" in res.json["response"]

    # Step 8: Testing Menu Option 3 (Internal Marks)
    res = client.post("/chat", json={"message": "3"})
    assert res.status_code == 200
    assert "Internal Examination Marks" in res.json["response"]

    # Step 9: Testing Menu Option 1 (My Profile)
    res = client.post("/chat", json={"message": "1"})
    assert res.status_code == 200
    assert "Student Profile (S1000)" in res.json["response"]

    # Step 10: Testing Menu Option 4 (Academic Performance)
    res = client.post("/chat", json={"message": "4"})
    assert res.status_code == 200
    assert "Academic Performance Summary" in res.json["response"]

    # Step 11: Testing Menu Option 5 (Study Recommendations)
    res = client.post("/chat", json={"message": "5"})
    assert res.status_code == 200
    assert "Study Recommendations" in res.json["response"]

    # Step 12: Testing Menu Option 6 (Logout)
    res = client.post("/chat", json={"message": "6"})
    assert res.status_code == 200
    data = res.json
    assert data["state"] == "START"
    assert data["reset_chat"] is True
    assert "logged out" in data["response"]

    # Confirm session is reset
    res = client.get("/student/profile")
    assert res.status_code == 401

    print("✅ Complete state machine and conversational flow passed perfectly.")


if __name__ == "__main__":
    test_greeting_normalization()
    test_conversation_state_flow()
    print("\n🎉 ALL UNIT AND INTEGRATION TESTS PASSED WITH 100% SUCCESS!")
