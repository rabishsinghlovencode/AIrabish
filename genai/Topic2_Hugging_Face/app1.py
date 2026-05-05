import streamlit as st
import pandas as pd

st.title("📄 Excel File Uploader and Viewer")

# Upload Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)
        
        # Show dataframe
        st.success("File uploaded successfully!")
        st.subheader("Preview of the uploaded Excel file:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
else:
    st.info("Please upload an Excel file to proceed.")
