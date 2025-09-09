import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import os

st.set_page_config(page_title="Data Profiler", layout="wide")

def get_filesize_mb(uploaded_file) -> float:
    # Streamlit's UploadedFile exposes .size (bytes)
    return uploaded_file.size / (1024 ** 2)

def validate_file(uploaded_file):
    name, ext = os.path.splitext(uploaded_file.name)
    return ext.lower() if ext.lower() in (".csv", ".xlsx") else None

# Sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload .csv or .xlsx (≤ 10 MB)")
    minimal = False
    if uploaded_file is not None:
        minimal = st.checkbox("Generate minimal report?", value=False)

if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        filesize = get_filesize_mb(uploaded_file)
        if filesize <= 10:
            # Load data
            if ext == ".csv":
                df = pd.read_csv(uploaded_file)
            else:
                xl = pd.ExcelFile(uploaded_file)
                sheet = st.sidebar.selectbox("Select sheet", tuple(xl.sheet_names))
                df = xl.parse(sheet)

            # Generate profile
            with st.spinner("Generating profiling report..."):
                profile = ProfileReport(df, minimal=minimal)

            # Show report inside Streamlit
            st.components.v1.html(profile.to_html(), height=1000, scrolling=True)

            # Optional: let user download the HTML report
            html_bytes = profile.to_html().encode("utf-8")
            st.download_button(
                label="Download full report (HTML)",
                data=html_bytes,
                file_name="data_profile_report.html",
                mime="text/html",
            )
        else:
            st.error(f"Maximum allowed file size is 10 MB, but received {filesize:.2f} MB.")
    else:
        st.error("Please upload only .csv or .xlsx files.")
else:
    st.title("Data Profiler")
    st.info("Upload your data from the left sidebar to generate a profiling report.")
