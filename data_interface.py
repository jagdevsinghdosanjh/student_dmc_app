import pandas as pd
from modules.pdf_parser import extract_table_from_pdf
from modules.data_loader import load_excel_data

def load_student_data(file, file_type):
    """
    Unified interface to load student data from either PDF or Excel.
    Returns a pandas DataFrame.
    """
    if file_type == "pdf":
        return extract_table_from_pdf(file)
    elif file_type == "xlsx":
        return load_excel_data(file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or Excel file.")
