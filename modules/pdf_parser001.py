import pdfplumber
import pandas as pd

def extract_table_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        all_rows = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:  # Skip header
                    all_rows.append(row)
        df = pd.DataFrame(all_rows, columns=table[0])
    return df
