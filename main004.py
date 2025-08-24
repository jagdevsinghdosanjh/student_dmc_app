import streamlit as st
from modules.data_loader import load_excel
from modules.report_generator import generate_dmc
from modules.ui_components import sidebar_controls
from modules.pdf_parser import extract_table_from_pdf
from data_interface import load_student_data
from modules.utils import validate_student_data
import pandas as pd
import tabula as tb

df=pd.DataFrame()
st.title("PDF Table Extraction and Validation")
valid, issues = validate_student_data(df)
if not valid:
    st.error("Validation failed:")
    for issue in issues:
        st.write(f"❌ {issue}")
else:
    st.success("✅ Data validated successfully!")
    st.dataframe(df)


file_type = st.sidebar.selectbox("Select input type", ["pdf", "xlsx"])
uploaded_file = st.sidebar.file_uploader("Upload file", type=[file_type])

if uploaded_file:
    df = load_student_data(uploaded_file, file_type)
    st.success(f"{file_type.upper()} file loaded successfully!")
    st.dataframe(df)

st.write("Parsed columns:", df.columns.tolist())
st.title("📄 Student DMC Generator")

uploaded_file = sidebar_controls()
if uploaded_file:
    df = load_excel(uploaded_file)
    st.dataframe(df)

    if st.button("Generate DMCs"):
        for _, row in df.iterrows():
            generate_dmc(row.to_dict())
        st.success("DMCs generated successfully!")
