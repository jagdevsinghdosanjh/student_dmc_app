import logging
import qrcode
from io import BytesIO
from num2words import num2words
import pandas as pd
from modules.validation.student_validator import validate_student_data
from modules.config.columns import DEFAULT_SUBJECT_COLUMNS
from modules.config.constants import DEFAULT_SUBJECT_COLUMNS

# Example: Load student data from a CSV file
df = pd.read_csv('students.csv')  # Make sure 'students.csv' exists and has the required columns

valid, issues = validate_student_data(df, subject_columns=DEFAULT_SUBJECT_COLUMNS)
if not valid:
    for issue in issues:
        print(f"❌ {issue}")
else:
    print("✅ Data validated successfully!")

# Setup logging with format and file output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='validation.log',
    filemode='w'
)

# Configurable column sets
ROLL_NO_COLUMN = "Roll No"
REQUIRED_COLUMNS = [ROLL_NO_COLUMN, "Student Name", "Class", "Section"]
DEFAULT_SUBJECT_COLUMNS = ["Math", "Science", "English", "Social Studies", "Punjabi"]

def _check_duplicate_columns(df):
    if df.columns.duplicated().any():
        return ["Duplicate column names found."]
    return []

def _check_required_columns(df, required_columns):
    return [f"Missing required column: {col}" for col in required_columns if col not in df.columns]

def _check_subject_columns(df, subject_columns):
    missing_subjects = [subj for subj in subject_columns if subj not in df.columns]
    if missing_subjects:
        return [f"Missing subject columns: {missing_subjects}"]
    return []

def _check_missing_roll_numbers(df):
    if ROLL_NO_COLUMN in df.columns and df[ROLL_NO_COLUMN].isnull().any():
        return ["Some rows have missing Roll No."]
    return []

def _check_empty_rows(df):
    if df.dropna(how="all").shape[0] == 0:
        return ["All rows are empty."]
    return []

def _check_marks_numeric(df, subject_columns):
    issues = []
    for subj in subject_columns:
        if subj in df.columns:
            if not pd.to_numeric(df[subj], errors='coerce').notnull().all():
                issues.append(f"Non-numeric marks found in {subj}")
    return issues

def validate_student_data(df, subject_columns=None):
    """Validates student data DataFrame for required structure and content."""
    issues = []
    subject_columns = subject_columns or DEFAULT_SUBJECT_COLUMNS

    issues.extend(_check_duplicate_columns(df))
    issues.extend(_check_required_columns(df, REQUIRED_COLUMNS))
    issues.extend(_check_subject_columns(df, subject_columns))
    issues.extend(_check_missing_roll_numbers(df))
    issues.extend(_check_empty_rows(df))
    issues.extend(_check_marks_numeric(df, subject_columns))

    if issues:
        logging.warning("Validation issues found:")
        for issue in issues:
            logging.warning(f" - {issue}")
        return False, issues

    return True, []

def format_name(name):
    """Formats student name to title case."""
    return name.strip().title()

def calculate_grade(marks):
    """Returns grade based on numeric marks."""
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
    """Converts numeric marks to words."""
    try:
        return num2words(marks)
    except (TypeError, ValueError):
        return "Invalid"

def generate_qr(data):
    """Generates QR code from input data and returns PNG bytes."""
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()

def validate_columns(df, required_cols):
    """Quick check for presence of required columns."""
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        logging.warning(f"Missing columns: {missing}")
        return False
    return True
