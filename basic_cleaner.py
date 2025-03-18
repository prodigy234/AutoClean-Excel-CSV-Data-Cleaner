import pandas as pd
import re
import streamlit as st

# Function to clean column names
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

# Function to clean Excel and CSV files
def clean_data(df, name_column="Name", case_type="snake_case"):
    df = clean_column_names(df, case_type)

    # Convert name column to title case
    if name_column in df.columns:
        df[name_column] = df[name_column].astype(str).str.title()

    # Convert date columns to proper SQL datetime format
    for col in df.columns:
        if "date" in col.lower():  
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Strip spaces from text fields
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df

# Streamlit UI
st.title("📊 Data Cleaner: Excel & CSV")

# File uploader supporting all Excel formats and CSV
uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xls", "xlsx", "xlsm", "xlsb", "csv"])

if uploaded_file:
    try:
        file_ext = uploaded_file.name.split(".")[-1].lower()

        # Select the correct Pandas read method
        if file_ext == "xls":
            df = pd.read_excel(uploaded_file, engine="xlrd")
        elif file_ext in ["xlsx", "xlsm", "xlsb"]:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif file_ext == "csv":
            df = pd.read_csv(uploaded_file)  # Read CSV file
        else:
            st.error("❌ Unsupported file format. Please upload an Excel or CSV file.")
            st.stop()

        # User selects naming convention
        case_type = st.radio("Select column naming format:", ["snake_case", "camelCase"])
        
        # User inputs the column containing names
        name_column = st.text_input("Enter the column name for names (e.g., 'Name')", "Name")

        if st.button("Clean Data"):
            cleaned_df = clean_data(df, name_column, case_type)

            # Convert to appropriate format for download
            cleaned_file = "cleaned_dataset.xlsx" if file_ext != "csv" else "cleaned_dataset.csv"
            
            if file_ext == "csv":
                cleaned_df.to_csv(cleaned_file, index=False)  # Save as CSV
                mime_type = "text/csv"
            else:
                cleaned_df.to_excel(cleaned_file, index=False, engine="openpyxl")  # Save as Excel
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            st.success("✅ Cleaning complete! Download your cleaned file below:")
            st.download_button("Download Cleaned File", open(cleaned_file, "rb"), file_name=cleaned_file, mime=mime_type)

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")



import pandas as pd
import re
import streamlit as st

# Function to clean column names
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

# Function to clean Excel file
def clean_excel_file(df, name_column="Name", case_type="snake_case"):
    df = clean_column_names(df, case_type)

    # Convert name column to title case
    if name_column in df.columns:
        df[name_column] = df[name_column].astype(str).str.title()

    # Convert date columns to proper SQL datetime format
    for col in df.columns:
        if "date" in col.lower():  
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Strip spaces from text fields
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df

# Streamlit UI
st.title("Excel Data Cleaner")

# File uploader supporting all Excel formats
uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx", "xlsm", "xlsb"])

if uploaded_file:
    try:
        file_ext = uploaded_file.name.split(".")[-1].lower()

        # Select the correct Pandas engine based on file type
        if file_ext == "xls":
            df = pd.read_excel(uploaded_file, engine="xlrd")
        else:  # For .xlsx, .xlsm, .xlsb
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        # User selects naming convention
        case_type = st.radio("Select column naming format:", ["snake_case", "camelCase"])
        
        # User inputs the column containing names
        name_column = st.text_input("Enter the column name for names (e.g., 'Name')", "Name")

        if st.button("Clean Data"):
            cleaned_df = clean_excel_file(df, name_column, case_type)

            # Convert to Excel for download
            cleaned_file = "cleaned_dataset.xlsx"
            cleaned_df.to_excel(cleaned_file, index=False, engine="openpyxl")
            
            st.success("✅ Cleaning complete! Download your cleaned file below:")
            st.download_button("Download Cleaned File", open(cleaned_file, "rb"), file_name="cleaned_dataset.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")