import streamlit as st
import pandas as pd
from pandas_profiling import ProfilesReport
from streamlit_pandas_profiling import st_profile
import sys
import os
st.set_page_config(page_title='Data Profiler',layout='wide')


def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb

def validate_file(file):
    filename = file.name
    name, ext = os.path.splittext(filename)
    if ext in ('.csv', '.xlsx'):
        return ext
    else:
        return False

# Sidebar
# Minimal report will only work in Primary Mode
with st.sidebar:
    uploaded_file = st.file_uploader('Upload .csv, .xlsx files not exceeding 10 MB')
    if uploaded_file is not None:
        st.write('Modes of Operation')
        minimal = st.checkbox('Do you want minimal report?')
        display_mode = st.radio('Display mode',
                                options=('Primary','Dark','Orange'))
        if display_mode == 'Dark':
            dark_mode = True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False

if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        filesize = get_filesize(uploaded_file)
        if filesize <= 10:
            if ext == '.csv':
                # Let load csv
                df = pd.read_csv(uploaded_file)
                # st.dataframe(df.head())
            else:
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox('Select the sheet',sheet_tuple)
                df = xl_file.parse(sheet_name)

            # Generate report
            with st.spinner('Generating report'):
                pr = ProfileReport(df,minimal=minimal,
                                dark_mode=dark_mode,
                                orange_mode=orange_mode
                                )
                
            st_profile_report(pr)
        else:
            st.error('Maximum allowed file size is 10 MB, but received {filesize} MB')
    else:
        st.error('Kindly upload only .csv or .xlsx files')

else:
    st.title('Data Profiler')
    st.info('Upload your data in the left sidebar to generate profiling')