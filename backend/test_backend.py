"""
test_backend.py - Unit and integration tests for Flask backend rules and endpoints.
"""

import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from dataset import get_dataset
from verification import get_session_manager
from attendance_rules import evaluate_attendance
from internal_rules import evaluate_internal_marks
from academic_rules import evaluate_overall_performance
from recommendations import generate_recommendations
from chatbot import get_chatbot
from main import app


def test_dataset_loading():
    ds = get_dataset()
    meta = ds.get_metadata()
    assert meta["total_students"] == 2000, f"Expected 2000 students, got {meta['total_students']}"
    assert meta["student_id_column"] == "Student_ID"
    assert meta["feature_availability"]["attendance"] is True
    assert meta["feature_availability"]["internal_test_1"] is True
    assert meta["feature_availability"]["internal_test_2"] is True
    print("✅ test_dataset_loading passed")


def test_attendance_rules():
    ds = get_dataset()

    # Test > 85% (e.g. S1001 with 91%)
    s1001 = ds.get_student_record("S1001")
    eval_1001 = evaluate_attendance(s1001)
    assert eval_1001["status"] == "Excellent"
    assert "Excellent! Your attendance is very good. Keep it up!" in eval_1001["advice"]

    # Test == 75% (e.g. S1031 with 75%)
    s1031 = ds.get_student_record("S1031")
    eval_1031 = evaluate_attendance(s1031)
    assert eval_1031["status"] == "Borderline Safe"
    assert "You are currently safe, but you are at the minimum attendance threshold" in eval_1031["advice"]

    # Test 65% - 74% (e.g. S1002 with 73%)
    s1002 = ds.get_student_record("S1002")
    eval_1002 = evaluate_attendance(s1002)
    assert eval_1002["status"] == "Warning"
    assert "Warning! Your attendance is below the required level. You may receive an I Grade" in eval_1002["advice"]

    # Test < 65% (e.g. S1678 with 60%)
    s1678 = ds.get_student_record("S1678")
    eval_1678 = evaluate_attendance(s1678)
    assert eval_1678["status"] == "Critical Warning"
    assert "Critical Warning! You are at high risk of receiving an I Grade" in eval_1678["advice"]

    print("✅ test_attendance_rules passed (all 4 cases verified)")


def test_internal_rules():
    ds = get_dataset()

    # S1118 has Internal Test 1 = 18 (<20) and Test 2 = 32 (30-40)
    s1118 = ds.get_student_record("S1118")
    eval_1118 = evaluate_internal_marks(s1118)
    assert eval_1118["test_1"]["category"] == "Poor Performance"
    assert "Poor performance. Study harder and aim to pass your end-semester examination." in eval_1118["test_1"]["feedback"]
    assert eval_1118["test_2"]["category"] == "Excellent Performance"
    assert "Excellent performance. Keep up the same effort in your next internal examination." in eval_1118["test_2"]["feedback"]

    # Student with 20-29 marks (S1002 has Internal Test 1 = 29)
    s1002 = ds.get_student_record("S1002")
    eval_1002 = evaluate_internal_marks(s1002)
    assert eval_1002["test_1"]["category"] == "Needs Improvement"
    assert "Needs improvement. Prepare better and aim for 30+ marks in your next examination." in eval_1002["test_1"]["feedback"]

    print("✅ test_internal_rules passed (all 3 score brackets verified)")


def test_academic_performance():
    ds = get_dataset()
    s1000 = ds.get_student_record("S1000")
    perf = evaluate_overall_performance(s1000)
    assert "composite_score" in perf
    assert perf["metrics"]["assignment"]["display_value"] == "7 / 10"
    assert perf["metrics"]["study_hours"]["display_value"] == "3 hrs/day"
    assert perf["metrics"]["final_exam"]["display_value"] == "72 / 100"
    print("✅ test_academic_performance passed")


def test_recommendations():
    ds = get_dataset()
    s1678 = ds.get_student_record("S1678")  # Critical attendance
    rec = generate_recommendations(s1678)
    assert len(rec["action_items"]) > 0
    assert any(a["urgency"] == "High" for a in rec["action_items"])
    print("✅ test_recommendations passed")


def test_flask_endpoints():
    client = app.test_client()

    # 1. Health endpoint
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["framework"] == "Flask"

    # 2. Verify invalid student ID
    res = client.post("/verify-student", json={"student_id": "INVALID999"})
    assert res.status_code == 404
    assert res.json["success"] is False

    # 3. Verify valid student ID
    res = client.post("/verify-student", json={"student_id": "S1000"})
    assert res.status_code == 200
    data = res.json
    assert data["success"] is True
    session_token = data["session_token"]
    assert session_token is not None

    headers = {"Authorization": f"Bearer {session_token}"}

    # 4. Unauthorized request to profile (without token)
    res = client.get("/student/profile")
    assert res.status_code == 401

    # 5. Authorized profile request
    res = client.get("/student/profile", headers=headers)
    assert res.status_code == 200
    assert res.json["student_id"] == "S1000"

    # 6. Authorized attendance request
    res = client.get("/student/attendance", headers=headers)
    assert res.status_code == 200
    assert res.json["percentage"] == 84

    # 7. Authorized internal marks request
    res = client.get("/student/internal-marks", headers=headers)
    assert res.status_code == 200
    assert res.json["test_1"]["score"] == 30

    # 8. Authorized performance request
    res = client.get("/student/performance", headers=headers)
    assert res.status_code == 200
    assert "composite_score" in res.json

    # 9. Authorized recommendations request
    res = client.get("/student/recommendations", headers=headers)
    assert res.status_code == 200
    assert len(res.json["action_items"]) >= 0

    # 10. Chat endpoint with session token
    res = client.post("/chat", json={"message": "2", "session_token": session_token})
    assert res.status_code == 200
    assert "ATTENDANCE REPORT" in res.json["text"]

    # 11. Logout
    res = client.post("/logout", headers=headers)
    assert res.status_code == 200

    # 12. Confirm session is revoked
    res = client.get("/student/profile", headers=headers)
    assert res.status_code == 401

    print("✅ test_flask_endpoints passed (all Flask routes & security tested)")


if __name__ == "__main__":
    test_dataset_loading()
    test_attendance_rules()
    test_internal_rules()
    test_academic_performance()
    test_recommendations()
    test_flask_endpoints()
    print("\n🎉 ALL FLASK TESTS PASSED SUCCESSFULLY!")
