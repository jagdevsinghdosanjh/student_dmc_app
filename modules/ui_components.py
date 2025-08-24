import streamlit as st

def sidebar_controls():
    st.sidebar.title("Upload & Filter")
    uploaded_file = st.sidebar.file_uploader("Upload Excel", type=["xlsx"])
    return uploaded_file
