import pandas as pd
import numpy as np
import re
import streamlit as st
from io import BytesIO
from sklearn.ensemble import IsolationForest
import seaborn as sns
import matplotlib.pyplot as plt

# ----------- Streamlit UI Customization -----------
st.set_page_config(page_title="Ultra Data Cleaner", layout="wide")

st.markdown("""
    <style>
        .title {text-align: center; color: #FF4B4B; font-size: 32px; font-weight: bold;}
        .stButton>button {background-color: #FF4B4B; color: white; font-size: 16px; border-radius: 10px; padding: 8px 16px;}
        .stDownloadButton>button {background-color: #4CAF50; color: white; font-size: 16px; border-radius: 10px; padding: 8px 16px;}
        .stSidebar {background-color: #1E1E1E; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("🧹 Ultra Data Cleaner: Excel & CSV")

st.markdown('<p class="title">AI-assisted Data Cleaning Tool</p>', unsafe_allow_html=True)

st.sidebar.header("⚙️ Cleaning Settings")

# ----------- Utility Functions -----------
def clean_column_names(df, case_type="snake_case"):
    def to_snake_case(name):
        return re.sub(r'\s+', '_', name.strip()).lower()

    def to_camel_case(name):
        words = re.sub(r'\s+', ' ', name.strip()).split()
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

    if case_type == "snake_case":
        df.columns = [to_snake_case(col) for col in df.columns]
    elif case_type == "camelCase":
        df.columns = [to_camel_case(col) for col in df.columns]
    return df

def clean_data(df, transformations):
    cleaning_log = []
    for col, action in transformations.items():
        original = df[col].copy()
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
        elif action == "Remove Duplicates":
            before = len(df)
            df.drop_duplicates(subset=[col], inplace=True)
            after = len(df)
            cleaning_log.append(f"Removed {before - after} duplicate rows based on `{col}`.")
        elif action == "Fill Missing (Mean)":
            mean_val = df[col].mean(numeric_only=True)
            df[col] = df[col].fillna(mean_val)
            cleaning_log.append(f"Filled missing values in `{col}` with mean: {mean_val:.2f}")
        elif action == "Fill Missing (Median)":
            median_val = df[col].median(numeric_only=True)
            df[col] = df[col].fillna(median_val)
            cleaning_log.append(f"Filled missing values in `{col}` with median: {median_val:.2f}")
        elif action == "Remove Special Characters":
            df[col] = df[col].astype(str).str.replace(r"[^\w\s]", "", regex=True)
        elif action == "Drop Column":
            df.drop(columns=[col], inplace=True)
            cleaning_log.append(f"Dropped column `{col}`.")
        elif action == "Regex Clean":
            pattern = st.sidebar.text_input(f"Enter regex pattern for `{col}`", value=r"[^a-zA-Z0-9\s]", key=f"regex_{col}")
            df[col] = df[col].astype(str).str.replace(pattern, "", regex=True)
            cleaning_log.append(f"Applied regex cleaning to `{col}` with pattern: `{pattern}`")
    return df, cleaning_log

# ----------- File Upload -----------
uploaded_file = st.file_uploader("📂 Upload Excel or CSV file", type=["csv", "xlsx", "xlsm", "xls", "xlsb"])
st.info("Upload your data and see the wonders I can do")

if uploaded_file:
    try:
        file_ext = uploaded_file.name.split(".")[-1].lower()

        if file_ext == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        if df.empty:
            st.warning("The uploaded file is empty.")
            st.stop()

        st.subheader("🔍 Dataset Overview")
        st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        st.write("**Missing Values:**")
        st.dataframe(df.isnull().sum().reset_index().rename(columns={0: "Missing Count"}))
        st.write("**Column Data Types:**")
        st.dataframe(df.dtypes.reset_index().rename(columns={0: "Data Type"}))

        st.subheader("📜 Data Preview")
        preview_size = st.slider("Rows to preview:", 5, min(100, df.shape[0]), 10)
        st.dataframe(df.head(preview_size))

        st.sidebar.subheader("🖋 Rename Columns")
        case_type = st.sidebar.radio("Column case format:", ["snake_case", "camelCase", "No Change"])
        if case_type != "No Change":
            df = clean_column_names(df, case_type)

        st.subheader("🛠 Column Transformations")
        transformations = {}
        for col in df.columns:
            action = st.selectbox(
                f"🔧 Action for `{col}`:",
                ["No Change", "Title Case", "Upper Case", "Lower Case", "Date Format", "Remove Spaces",
                 "Remove Duplicates", "Fill Missing (Mean)", "Fill Missing (Median)",
                 "Remove Special Characters", "Drop Column", "Regex Clean"],
                key=col
            )
            if action != "No Change":
                transformations[col] = action

        st.sidebar.subheader("🗑 Drop Rows")
        drop_na_option = st.sidebar.checkbox("Drop rows with missing values")

        st.sidebar.subheader("🔎 Conditional Row Filter")
        conditional_filter = st.sidebar.text_input("Enter condition (e.g. Age > 30 and Gender == 'Male')")

        if st.button("✨ Clean Data"):
            cleaned_df, log = clean_data(df.copy(), transformations)
            if drop_na_option:
                cleaned_df.dropna(inplace=True)
                log.append("Dropped rows with missing values.")

            if conditional_filter:
                try:
                    cleaned_df = cleaned_df.query(conditional_filter)
                    log.append(f"Applied row filter: `{conditional_filter}`")
                except Exception as e:
                    st.warning(f"⚠️ Error in filter expression: {e}")

            st.success("✅ Data cleaning complete!")

            st.subheader("📈 Cleaned Data Preview")
            st.dataframe(cleaned_df.head(preview_size))

            st.subheader("📊 Summary Statistics")
            if not cleaned_df.select_dtypes(include=np.number).empty:
                st.dataframe(cleaned_df.describe())

                st.subheader("📉 Correlation Heatmap")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(cleaned_df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)

            st.subheader("🚨 Anomaly Detection (Isolation Forest)")
            numeric_df = cleaned_df.select_dtypes(include=np.number)
            if not numeric_df.empty:
                iso = IsolationForest(contamination=0.05, random_state=42)
                cleaned_df['anomaly'] = iso.fit_predict(numeric_df)
                st.write("-1 = Anomaly, 1 = Normal")
                st.dataframe(cleaned_df[['anomaly'] + list(numeric_df.columns)].head(preview_size))

            st.subheader("📝 Cleaning Log")
            for entry in log:
                st.markdown(f"- {entry}")

            st.subheader("📥 Download Cleaned Data")
            output = BytesIO()
            if file_ext == "csv":
                cleaned_df.to_csv(output, index=False)
                mime = "text/csv"
                filename = "cleaned_data.csv"
            else:
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    cleaned_df.to_excel(writer, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                filename = "cleaned_data.xlsx"

            output.seek(0)
            st.download_button("⬇️ Download", output, file_name=filename, mime=mime)

    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")

# Footer
st.markdown("---")
st.markdown("# About the Developer")

st.image("My image4.jpg", width=250)
st.markdown("## **Kajola Gbenga**")

st.markdown(
    """
\U0001F4C7 Certified Data Analyst | Certified Data Scientist | Certified SQL Programmer | Mobile App Developer | AI/ML Engineer

\U0001F517 [LinkedIn](https://www.linkedin.com/in/kajolagbenga)  
\U0001F4DC [View My Certifications & Licences](https://www.datacamp.com/portfolio/kgbenga234)  
\U0001F4BB [GitHub](https://github.com/prodigy234)  
\U0001F310 [Portfolio](https://kajolagbenga.netlify.app/)  
\U0001F4E7 k.gbenga234@gmail.com
"""
)

st.markdown("✅ Created using Python and Streamlit")