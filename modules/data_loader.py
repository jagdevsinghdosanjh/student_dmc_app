import pandas as pd

def load_excel(file):
    df = pd.read_excel(file)
    df.dropna(subset=["Roll No"], inplace=True)
    return df

def load_excel_data(excel_file):
    return pd.read_excel(excel_file)