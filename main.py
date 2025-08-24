import streamlit as st
import pandas as pd
from modules.data_loader import load_excel
from modules.ui_components import sidebar_controls
from data_interface import load_student_data
from modules.utils import validate_student_data
from modules.dmc_viewer import render_dmc_html, generate_dmc_pdf

# ─────────────────────────────────────────────────────────────
# 📥 File Upload & Validation
# ─────────────────────────────────────────────────────────────

st.title("📄 PDF Table Extraction and Validation")

file_type = st.sidebar.selectbox("Select input type", ["xlsx", "pdf"])
uploaded_input_file = st.sidebar.file_uploader("Upload file", type=[file_type])

df = pd.DataFrame()

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

# ─────────────────────────────────────────────────────────────
# 🧾 DMC Generator & Viewer
# ─────────────────────────────────────────────────────────────

st.title("🎓 Student DMC Generator")

uploaded_dmc_file = sidebar_controls()
if uploaded_dmc_file:
    df_dmc = load_excel(uploaded_dmc_file)
    st.dataframe(df_dmc)

    selected_roll = st.selectbox("Select Roll No", df_dmc["Roll No"].dropna().unique())
    selected_row = df_dmc[df_dmc["Roll No"] == selected_roll].iloc[0]

    # Preview DMC
    if st.button("Preview DMC"):
        html_preview = render_dmc_html(selected_row.to_dict())
        st.components.v1.html(html_preview, height=600, scrolling=True)

        with st.expander("Show Raw HTML"):
            st.code(html_preview, language="html")

    # Download DMC PDF
    if st.button("Download DMC PDF"):
        pdf_path = generate_dmc_pdf(selected_row.to_dict())
        if pdf_path:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Click to Download",
                    data=f.read(),
                    file_name=pdf_path.split("/")[-1],
                    mime="application/pdf"
                )
        else:
            st.error("PDF generation failed. Check logs for details.")

    # Bulk DMC Generation
    if st.button("Generate All DMCs"):
        for _, row in df_dmc.iterrows():
            generate_dmc_pdf(row.to_dict())
        st.success("✅ All DMCs generated successfully!")
