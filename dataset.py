"""
dataset.py - CSV loading, schema inspection, feature mapping, and student record lookup.
Integrates with data/student_dataset.csv dynamically and robustly.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
import pandas as pd
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

# Check data directory first, fallback to root dataset
CSV_CANDIDATES = [
    BASE_DIR / "data" / "student_dataset.csv",
    BASE_DIR / "Final_Marks_Data.csv",
    Path("data/student_dataset.csv"),
    Path("Final_Marks_Data.csv"),
]


class AcademicDataset:
    def __init__(self):
        self.csv_path: Optional[Path] = None
        self.df: Optional[pd.DataFrame] = None
        self.student_id_col: Optional[str] = None
        self.column_mapping: Dict[str, Optional[str]] = {
            "student_id": None,
            "attendance": None,
            "internal_test_1": None,
            "internal_test_2": None,
            "assignment": None,
            "study_hours": None,
            "final_exam": None,
        }
        self.feature_availability: Dict[str, bool] = {
            "attendance": False,
            "internal_test_1": False,
            "internal_test_2": False,
            "assignment": False,
            "study_hours": False,
            "final_exam": False,
        }
        self.total_records: int = 0
        self.load_dataset()

    def load_dataset(self) -> None:
        """Loads and validates the CSV dataset, mapping columns dynamically."""
        for candidate in CSV_CANDIDATES:
            if candidate.exists():
                self.csv_path = candidate
                break

        if not self.csv_path or not self.csv_path.exists():
            logger.error("Dataset file not found in candidates list.")
            raise FileNotFoundError("CSV dataset not found in data/ or root directory.")

        try:
            self.df = pd.read_csv(self.csv_path)
            # Strip whitespace from column names
            self.df.columns = [str(col).strip() for col in self.df.columns]
            self.total_records = len(self.df)
            self._detect_and_map_columns()
            self._prepare_index()
            logger.info(
                f"Successfully loaded dataset '{self.csv_path.name}' with {self.total_records} rows and {len(self.df.columns)} columns."
            )
        except Exception as e:
            logger.exception(f"Error loading CSV dataset: {e}")
            raise RuntimeError(f"Failed to load dataset: {str(e)}")

    def _detect_and_map_columns(self) -> None:
        """Dynamically inspects existing columns and maps them to standard feature keys."""
        assert self.df is not None
        cols = list(self.df.columns)

        # 1. Identify Student ID column
        for col in cols:
            col_lower = col.lower()
            if "student_id" in col_lower or "student id" in col_lower or col_lower == "id":
                self.column_mapping["student_id"] = col
                self.student_id_col = col
                break

        if not self.student_id_col:
            if len(cols) > 0 and self.df[cols[0]].nunique() == len(self.df):
                self.column_mapping["student_id"] = cols[0]
                self.student_id_col = cols[0]
            else:
                raise ValueError("Could not automatically identify a unique student identifier column in CSV.")

        # 2. Identify Attendance column
        for col in cols:
            col_lower = col.lower()
            if "attendance" in col_lower:
                self.column_mapping["attendance"] = col
                self.feature_availability["attendance"] = True
                break

        # 3. Identify Internal Examination columns
        for col in cols:
            col_lower = col.lower()
            if "internal" in col_lower and ("1" in col_lower or "test 1" in col_lower or "test_1" in col_lower):
                self.column_mapping["internal_test_1"] = col
                self.feature_availability["internal_test_1"] = True
            elif "internal" in col_lower and ("2" in col_lower or "test 2" in col_lower or "test_2" in col_lower):
                self.column_mapping["internal_test_2"] = col
                self.feature_availability["internal_test_2"] = True
            elif "internal" in col_lower and not self.column_mapping["internal_test_1"]:
                self.column_mapping["internal_test_1"] = col
                self.feature_availability["internal_test_1"] = True

        # 4. Identify Assignment Score column
        for col in cols:
            col_lower = col.lower()
            if "assignment" in col_lower:
                self.column_mapping["assignment"] = col
                self.feature_availability["assignment"] = True
                break

        # 5. Identify Daily Study Hours column
        for col in cols:
            col_lower = col.lower()
            if "study" in col_lower and "hour" in col_lower:
                self.column_mapping["study_hours"] = col
                self.feature_availability["study_hours"] = True
                break

        # 6. Identify Final Exam Marks column
        for col in cols:
            col_lower = col.lower()
            if "final" in col_lower or "end semester" in col_lower or "exam marks" in col_lower:
                self.column_mapping["final_exam"] = col
                self.feature_availability["final_exam"] = True
                break

    def _prepare_index(self) -> None:
        """Normalizes the student ID column for fast, case-insensitive lookups."""
        if self.df is not None and self.student_id_col:
            self.df[self.student_id_col] = self.df[self.student_id_col].astype(str).str.strip()
            self._lookup: Dict[str, Dict[str, Any]] = {}
            for _, row in self.df.iterrows():
                sid_norm = str(row[self.student_id_col]).strip().casefold()
                self._lookup[sid_norm] = row.to_dict()

    def student_exists(self, student_id: str) -> bool:
        """Checks if student ID exists in the dataset (case-insensitive)."""
        if not student_id or not hasattr(self, "_lookup"):
            return False
        return student_id.strip().casefold() in self._lookup

    def get_student_record(self, student_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves raw student record and standardized mapped fields without inventing data."""
        if not self.student_exists(student_id):
            return None

        raw_record = self._lookup[student_id.strip().casefold()]

        record: Dict[str, Any] = {
            "student_id": str(raw_record.get(self.student_id_col, student_id)),
            "raw_data": raw_record,
            "mapped_fields": {},
            "features_available": self.feature_availability.copy(),
        }

        for feature, col_name in self.column_mapping.items():
            if col_name and col_name in raw_record:
                val = raw_record[col_name]
                if pd.isna(val):
                    record["mapped_fields"][feature] = None
                else:
                    record["mapped_fields"][feature] = val
            else:
                record["mapped_fields"][feature] = None

        return record

    def get_metadata(self) -> Dict[str, Any]:
        """Returns metadata about the loaded dataset for transparency and inspection."""
        sample_ids: List[str] = []
        if self.df is not None and self.student_id_col:
            sample_ids = self.df[self.student_id_col].head(6).tolist()

        return {
            "csv_path": str(self.csv_path),
            "total_students": self.total_records,
            "student_id_column": self.student_id_col,
            "detected_columns": list(self.df.columns) if self.df is not None else [],
            "column_mapping": self.column_mapping,
            "feature_availability": self.feature_availability,
            "sample_ids": sample_ids,
        }


# Global singleton instance
dataset_instance = AcademicDataset()


def get_dataset() -> AcademicDataset:
    return dataset_instance

