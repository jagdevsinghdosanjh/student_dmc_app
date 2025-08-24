import pdfplumber
import pandas as pd

def extract_table_from_pdf(pdf_file):
    import pdfplumber
    import pandas as pd

    with pdfplumber.open(pdf_file) as pdf:
        all_rows = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:  # Skip header
                    all_rows.append(row)

        # Extract header and sanitize
        raw_header = table[0]
        clean_header = []
        seen = set()
        for i, col in enumerate(raw_header):
            col_name = col.strip() if col else f"Column_{i}"
            if col_name in seen:
                col_name += f"_{i}"
            seen.add(col_name)
            clean_header.append(col_name)

        df = pd.DataFrame(all_rows, columns=clean_header)
    return df
