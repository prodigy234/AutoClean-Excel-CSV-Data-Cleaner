# 🧹 Ultra Data Cleaner: Excel & CSV

**Ultra Data Cleaner** is an interactive Streamlit web app that enables users to upload Excel or CSV datasets, apply various data cleaning transformations, and download the cleaned dataset. It is designed to be beginner-friendly yet robust for analysts and developers working with messy data.

---

## 📬 Author

**Gbenga Kajola**

[LinkedIn](https://www.linkedin.com/in/kajolagbenga)

[Portfolio](https://kajolagbenga.netlify.app)

[Certified_Data_Scientist](https://www.datacamp.com/certificate/DSA0012312825030)

[Certified_Data_Analyst](https://www.datacamp.com/certificate/DAA0018583322187)

[Certified_SQL_Database_Programmer](https://www.datacamp.com/certificate/SQA0019722049554)

---


## 🚀 Features

- Upload CSV or Excel datasets
- Detect and visualize missing values
- Rename columns to `snake_case` or `camelCase`
- Column-wise transformations (e.g. title case, fill missing, regex clean, etc.)
- Drop duplicates, special characters, or specific columns
- Apply regex-based cleaning per column
- Optional row-level filtering (e.g., `Age > 30 and Gender == 'Male'`)
- Anomaly detection with Isolation Forest
- Correlation heatmap
- Summary statistics
- Cleaned data preview and download

---

## 📦 Installation

Ensure you have **Python 3.8+** installed. Then, install the required libraries:

```bash
pip install pandas numpy streamlit seaborn matplotlib scikit-learn openpyxl
```

---

## 🧑‍💻 How to Run

```bash
streamlit run your_script_name.py
```

Replace `your_script_name.py` with the filename of your Python script.

---

## 📄 Supported File Types

- `.csv`
- `.xlsx`, `.xlsm`, `.xls`, `.xlsb` (Excel files)

---

## 📷 Screenshots

### 🔍 Dataset Overview
Get details about missing values, data types, and preview raw data.

### 🛠 Column Transformations
Select from a wide list of transformations to apply per column.

### 📊 Statistical Insights
Understand your data through descriptive stats and heatmaps.

### 🚨 Anomaly Detection
Identify outliers using Isolation Forest on numeric features.

---

## 📥 Download Feature

After cleaning, you can download your dataset in the same format as uploaded (CSV or Excel).

---

## ✅ Built With

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [scikit-learn](https://scikit-learn.org/)

---

## 📜 License

MIT License © Kajola Gbenga 2025
