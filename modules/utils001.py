import logging
import qrcode
from io import BytesIO
from num2words import num2words
import logging

REQUIRED_COLUMNS = ["Roll No", "Student Name", "Class", "Section"]
SUBJECT_COLUMNS = ["Math", "Science", "English", "Social Studies", "Punjabi"]

def validate_student_data(df):
    issues = []

    # Check for duplicate columns
    if df.columns.duplicated().any():
        issues.append("Duplicate column names found.")

    # Check for required columns
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            issues.append(f"Missing required column: {col}")

    # Check for subject columns
    missing_subjects = [subj for subj in SUBJECT_COLUMNS if subj not in df.columns]
    if missing_subjects:
        issues.append(f"Missing subject columns: {missing_subjects}")

    # Check for missing roll numbers
    if df["Roll No"].isnull().any():
        issues.append("Some rows have missing Roll No.")

    # Check for empty rows
    if df.dropna(how="all").shape[0] == 0:
        issues.append("All rows are empty.")

    # Optional: Check if marks are numeric
    for subj in SUBJECT_COLUMNS:
        if subj in df.columns:
            if not df[subj].apply(lambda x: str(x).replace('.', '', 1).isdigit()).all():
                issues.append(f"Non-numeric marks found in {subj}")

    if issues:
        logging.warning("Validation issues found:")
        for issue in issues:
            logging.warning(f" - {issue}")
        return False, issues

    return True, []


# Setup logging
logging.basicConfig(level=logging.INFO)

def format_name(name):
    return name.strip().title()

def calculate_grade(marks):
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
    except:
        return "Invalid"

def generate_qr(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()

def validate_columns(df, required_cols):
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        logging.warning(f"Missing columns: {missing}")
        return False
    return True
