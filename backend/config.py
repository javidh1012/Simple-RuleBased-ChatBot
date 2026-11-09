"""
Configuration settings for the Student Academic Assistant backend.
All thresholds are centralized and configurable here.
"""

from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

# CSV Dataset path - checks project root and current folder
DEFAULT_CSV_PATH = BASE_DIR / "Final_Marks_Data.csv"
if not DEFAULT_CSV_PATH.exists():
    DEFAULT_CSV_PATH = Path("Final_Marks_Data.csv")


class ThresholdConfig(BaseModel):
    # Attendance thresholds (%)
    attendance_excellent_min: float = 85.0
    attendance_safe_threshold: float = 75.0
    attendance_warning_min: float = 65.0

    # Internal marks thresholds (out of 40)
    internal_excellent_min: float = 30.0
    internal_improvement_min: float = 20.0
    internal_max_marks: float = 40.0

    # Assignment score thresholds (out of 10)
    assignment_outstanding_min: float = 9.0
    assignment_good_min: float = 7.0
    assignment_average_min: float = 5.0
    assignment_max_score: float = 10.0

    # Daily study hours thresholds
    study_hours_high_min: float = 4.0
    study_hours_recommended_min: float = 3.0
    study_hours_low_threshold: float = 2.0

    # Final Exam thresholds (out of 100)
    final_distinction_min: float = 85.0
    final_first_class_min: float = 70.0
    final_second_class_min: float = 50.0
    final_pass_min: float = 40.0
    final_max_marks: float = 100.0


THRESHOLDS = ThresholdConfig()

# Session settings
SESSION_EXPIRY_HOURS = 24

# Allowed CORS origins
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*",
]

