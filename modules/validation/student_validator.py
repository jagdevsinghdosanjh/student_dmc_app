import logging
import pandas as pd
from config.columns import REQUIRED_COLUMNS, DEFAULT_SUBJECT_COLUMNS

def check_duplicate_columns(df):
    if df.columns.duplicated().any():
        return ["Duplicate column names found."]
    return []

def check_required_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return [f"Missing required column: {col}" for col in missing]

def check_subject_columns(df, subject_columns):
    missing = [col for col in subject_columns if col not in df.columns]
    return [f"Missing subject columns: {missing}"] if missing else []

def check_missing_roll_numbers(df):
    if "Roll No" in df.columns and df["Roll No"].isnull().any():
        return ["Some rows have missing Roll No."]
    return []

def check_empty_rows(df):
    if df.dropna(how="all").shape[0] == 0:
        return ["All rows are empty."]
    return []

def check_numeric_subjects(df, subject_columns):
    issues = []
    for subj in subject_columns:
        if subj in df.columns:
            if not pd.to_numeric(df[subj], errors='coerce').notnull().all():
                issues.append(f"Non-numeric marks found in {subj}")
    return issues

def validate_student_data(df, subject_columns=None):
    """Validates student data DataFrame for structure and content."""
    subject_columns = subject_columns or DEFAULT_SUBJECT_COLUMNS
    issues = []

    issues += check_duplicate_columns(df)
    issues += check_required_columns(df)
    issues += check_subject_columns(df, subject_columns)
    issues += check_missing_roll_numbers(df)
    issues += check_empty_rows(df)
    issues += check_numeric_subjects(df, subject_columns)

    if issues:
        logging.warning("Validation issues found:")
        for issue in issues:
            logging.warning(f" - {issue}")
        return False, issues

    return True, []
