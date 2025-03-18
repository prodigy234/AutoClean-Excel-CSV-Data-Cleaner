import pandas as pd
import re
import streamlit as st

# ----------- Streamlit UI Customization -----------
st.set_page_config(page_title="Excel & CSV Data Cleaner", layout="wide")

st.markdown("""
    <style>
        .title {text-align: center; color: #FF4B4B; font-size: 28px; font-weight: bold;}
        .sidebar {background-color: #1E1E1E; color: white;}
        .stButton>button {background-color: #FF4B4B; color: white; font-size: 16px; border-radius: 10px;}
        .stDownloadButton>button {background-color: #4CAF50; color: white; font-size: 16px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">📊 Advanced Data Cleaner: Excel & CSV</p>', unsafe_allow_html=True)

st.sidebar.header("⚙️ Settings")

# ----------- Utility Functions -----------
def clean_column_names(df, case_type="snake_case"):
    def to_snake_case(name):
        return re.sub(r'[\s]+', '_', name.strip()).lower()

    def to_camel_case(name):
        words = re.sub(r'[\s]+', ' ', name.strip()).split()
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

    if case_type == "snake_case":
        df.columns = [to_snake_case(col) for col in df.columns]
    elif case_type == "camelCase":
        df.columns = [to_camel_case(col) for col in df.columns]
    
    return df

def clean_data(df, transformations):
    for col, action in transformations.items():
        if action == "Title Case":
            df[col] = df[col].astype(str).str.title()
        elif action == "Upper Case":
            df[col] = df[col].astype(str).str.upper()
        elif action == "Lower Case":
            df[col] = df[col].astype(str).str.lower()
        elif action == "Date Format":
            df[col] = pd.to_datetime(df[col], errors="coerce")
        elif action == "Remove Spaces":
            df[col] = df[col].astype(str).str.strip()
    
    return df

# ----------- File Upload Section -----------
uploaded_file = st.file_uploader("📂 Upload an Excel or CSV file", type=["xls", "xlsx", "xlsm", "xlsb", "csv"])

if uploaded_file:
    try:
        file_ext = uploaded_file.name.split(".")[-1].lower()

        # Select correct engine for reading files
        if file_ext == "xls":
            df = pd.read_excel(uploaded_file, engine="xlrd")
        elif file_ext in ["xlsx", "xlsm", "xlsb"]:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif file_ext == "csv":
            df = pd.read_csv(uploaded_file)

        # Show data preview
        st.subheader("📜 Data Preview")
        st.dataframe(df.head())

        # Column renaming options
        st.sidebar.subheader("🖋 Column Naming Format")
        case_type = st.sidebar.radio("Select format:", ["snake_case", "camelCase", "No Change"])

        # Clean column names based on user choice
        if case_type != "No Change":
            df = clean_column_names(df, case_type)

        # Display all columns and let user select transformations
        st.subheader("🛠 Column Transformations")
        column_actions = {}

        for col in df.columns:
            action = st.selectbox(
                f"🔹 What should be done to `{col}`?",
                ["No Change", "Title Case", "Upper Case", "Lower Case", "Date Format", "Remove Spaces"],
                key=col
            )
            column_actions[col] = action

        if st.button("✨ Clean Data"):
            cleaned_df = clean_data(df, column_actions)

            # Convert to appropriate format for download
            cleaned_file = "cleaned_dataset.xlsx" if file_ext != "csv" else "cleaned_dataset.csv"
            
            if file_ext == "csv":
                cleaned_df.to_csv(cleaned_file, index=False)
                mime_type = "text/csv"
            else:
                cleaned_df.to_excel(cleaned_file, index=False, engine="openpyxl")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            st.success("✅ Cleaning Complete! Download your cleaned file below:")
            st.download_button("📥 Download Cleaned File", open(cleaned_file, "rb"), file_name=cleaned_file, mime=mime_type)

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")