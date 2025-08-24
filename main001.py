import streamlit as st
from modules.data_loader import load_excel
from modules.report_generator import generate_dmc
from modules.ui_components import sidebar_controls
from modules.pdf_parser import extract_table_from_pdf

# from modules.image_processor import process_image
# from modules.text_extractor import extract_text_from_image
# from modules.utils import save_to_excel
# import os
# import pandas as pd
# import tempfile
# import fitz  # PyMuPDF
# from PIL import Image
# import io

st.title("📄 Student DMC Generator")

uploaded_file = sidebar_controls()
if uploaded_file:
    df = load_excel(uploaded_file)
    st.dataframe(df)

    if st.button("Generate DMCs"):
        for _, row in df.iterrows():
            generate_dmc(row.to_dict())
        st.success("DMCs generated successfully!")
