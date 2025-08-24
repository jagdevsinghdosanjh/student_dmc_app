import logging
import qrcode
from io import BytesIO
from num2words import num2words
import pandas as pd
from config.constants import (
    ROLL_NO_COLUMN,
    STUDENT_NAME_COLUMN,
    CLASS_COLUMN,
    SECTION_COLUMN,
    DEFAULT_SUBJECT_COLUMNS
)

# Setup logging
logging.basicConfig(level=logging.INFO)

REQUIRED_COLUMNS = [ROLL_NO_COLUMN, STUDENT_NAME_COLUMN, CLASS_COLUMN, SECTION_COLUMN]

# ─────────────────────────────────────────────────────────────
# ✅ Validation Helpers
# ─────────────────────────────────────────────────────────────

def check_duplicate_columns(df):
    return ["Duplicate column names found."] if df.columns.duplicated().any() else []

def check_required_columns(df):
    return [f"Missing required column: {col}" for col in REQUIRED_COLUMNS if col not in df.columns]

def check_subject_columns(df):
    missing = [subj for subj in DEFAULT_SUBJECT_COLUMNS if subj not in df.columns]
    return [f"Missing subject columns: {missing}"] if missing else []

def check_missing_roll_numbers(df):
    if ROLL_NO_COLUMN in df.columns and df[ROLL_NO_COLUMN].isnull().any():
        return ["Some rows have missing Roll No."]
    return []

def check_empty_rows(df):
    return ["All rows are empty."] if df.dropna(how="all").shape[0] == 0 else []

def check_numeric_subjects(df):
    issues = []
    for subj in DEFAULT_SUBJECT_COLUMNS:
        if subj in df.columns:
            if not pd.to_numeric(df[subj], errors='coerce').notnull().all():
                issues.append(f"Non-numeric marks found in {subj}")
    return issues

def validate_student_data(df):
    """Validates student data for structure and content."""
    issues = []
    issues += check_duplicate_columns(df)
    issues += check_required_columns(df)
    issues += check_subject_columns(df)
    issues += check_missing_roll_numbers(df)
    issues += check_empty_rows(df)
    issues += check_numeric_subjects(df)

    if issues:
        logging.warning("Validation issues found:")
        for issue in issues:
            logging.warning(f" - {issue}")
        return False, issues

    return True, []

# ─────────────────────────────────────────────────────────────
# ✅ Formatting & Conversion
# ─────────────────────────────────────────────────────────────

def format_name(name):
    return name.strip().title()

def calculate_grade(marks):
    try:
        marks = float(marks)
    except (TypeError, ValueError):
        return "Invalid"
    if marks >= 91: return "A+"
    elif marks >= 81: return "A"
    elif marks >= 71: return "B+"
    elif marks >= 61: return "B"
    elif marks >= 51: return "C"
    elif marks >= 41: return "D"
    else: return "F"

def marks_to_words(marks):
    try:
        return num2words(marks)
    except (TypeError, ValueError):
        return "Invalid"

# ─────────────────────────────────────────────────────────────
# ✅ QR Code Generator
# ─────────────────────────────────────────────────────────────

def generate_qr(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()

# ─────────────────────────────────────────────────────────────
# ✅ Column Validator
# ─────────────────────────────────────────────────────────────

def validate_columns(df, required_cols):
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        logging.warning(f"Missing columns: {missing}")
        return False
    return True

# import logging
# import qrcode
# from io import BytesIO
# from num2words import num2words
# import pandas as pd

# # Setup logging
# logging.basicConfig(level=logging.INFO)

# REQUIRED_COLUMNS = ["Roll No", "Student Name", "Class", "Section"]
# SUBJECT_COLUMNS = ["Math", "Science", "English", "Social Studies", "Punjabi"]

# # ─────────────────────────────────────────────────────────────
# # ✅ Validation Helpers
# # ─────────────────────────────────────────────────────────────

# def check_duplicate_columns(df):
#     return ["Duplicate column names found."] if df.columns.duplicated().any() else []

# def check_required_columns(df):
#     return [f"Missing required column: {col}" for col in REQUIRED_COLUMNS if col not in df.columns]

# def check_subject_columns(df):
#     missing = [subj for subj in SUBJECT_COLUMNS if subj not in df.columns]
#     return [f"Missing subject columns: {missing}"] if missing else []

# def check_missing_roll_numbers(df):
#     return ["Some rows have missing Roll No."] if "Roll No" in df.columns and df["Roll No"].isnull().any() else []

# def check_empty_rows(df):
#     return ["All rows are empty."] if df.dropna(how="all").shape[0] == 0 else []

# def check_numeric_subjects(df):
#     issues = []
#     for subj in SUBJECT_COLUMNS:
#         if subj in df.columns:
#             if not pd.to_numeric(df[subj], errors='coerce').notnull().all():
#                 issues.append(f"Non-numeric marks found in {subj}")
#     return issues

# def validate_student_data(df):
#     """Validates student data for structure and content."""
#     issues = []
#     issues += check_duplicate_columns(df)
#     issues += check_required_columns(df)
#     issues += check_subject_columns(df)
#     issues += check_missing_roll_numbers(df)
#     issues += check_empty_rows(df)
#     issues += check_numeric_subjects(df)

#     if issues:
#         logging.warning("Validation issues found:")
#         for issue in issues:
#             logging.warning(f" - {issue}")
#         return False, issues

#     return True, []

# # ─────────────────────────────────────────────────────────────
# # ✅ Formatting & Conversion
# # ─────────────────────────────────────────────────────────────

# def format_name(name):
#     return name.strip().title()

# def calculate_grade(marks):
#     try:
#         marks = float(marks)
#     except (TypeError, ValueError):
#         return "Invalid"
#     if marks >= 91: return "A+"
#     elif marks >= 81: return "A"
#     elif marks >= 71: return "B+"
#     elif marks >= 61: return "B"
#     elif marks >= 51: return "C"
#     elif marks >= 41: return "D"
#     else: return "F"

# def marks_to_words(marks):
#     try:
#         return num2words(marks)
#     except (TypeError, ValueError):
#         return "Invalid"

# # ─────────────────────────────────────────────────────────────
# # ✅ QR Code Generator
# # ─────────────────────────────────────────────────────────────

# def generate_qr(data):
#     qr = qrcode.make(data)
#     buffer = BytesIO()
#     qr.save(buffer, format="PNG")
#     return buffer.getvalue()

# # ─────────────────────────────────────────────────────────────
# # ✅ Column Validator
# # ─────────────────────────────────────────────────────────────

# def validate_columns(df, required_cols):
#     missing = [col for col in required_cols if col not in df.columns]
#     if missing:
#         logging.warning(f"Missing columns: {missing}")
#         return False
#     return True
