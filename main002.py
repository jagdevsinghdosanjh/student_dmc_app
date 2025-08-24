import streamlit as st
from modules.data_loader import load_excel
from modules.report_generator import generate_dmc
from modules.ui_components import sidebar_controls
from modules.pdf_parser import extract_table_from_pdf
from data_interface import load_student_data
from modules.utils import validate_student_data
import pandas as pd
import tabula as tb

# Initialize empty DataFrame
df = pd.DataFrame()

st.title("PDF Table Extraction and Validation")

# Sidebar controls for file upload
file_type = st.sidebar.selectbox("Select input type", ["pdf", "xlsx"])
uploaded_input_file = st.sidebar.file_uploader("Upload file", type=[file_type])

# Load and validate file
if uploaded_input_file:
    df = load_student_data(uploaded_input_file, file_type)
    st.success(f"{file_type.upper()} file loaded successfully!")
    st.dataframe(df)

    if df.empty:
        st.warning("Uploaded file has no data.")
    else:
        valid, issues = validate_student_data(df)
        if not valid:
            st.error("Validation failed:")
            for issue in issues:
                st.write(f"❌ {issue}")
        else:
            st.success("✅ Data validated successfully!")

    st.write("Parsed columns:", df.columns.tolist())

# Section for DMC generation
st.title("📄 Student DMC Generator")

uploaded_dmc_file = sidebar_controls()
if uploaded_dmc_file:
    df_dmc = load_excel(uploaded_dmc_file)
    st.dataframe(df_dmc)

    if st.button("Generate DMCs"):
        for _, row in df_dmc.iterrows():
            generate_dmc(row.to_dict())
        st.success("DMCs generated successfully!")
