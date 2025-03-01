import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #FFDEE9, #B5FFFC);
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff758c, #ff7eb3);
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 12px;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff7eb3, #ff758c);
    }
    h1, h2 {
        color: #ff4081;
    }
    .chart-container, .dataframe {
        background: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align: center;'>🎨 File Converter & Cleaner 🚀</h1>", unsafe_allow_html=True)
st.write("🌟 **Upload CSV or Excel files, clean data, and convert formats in a stylish way!**")

st.sidebar.markdown("<h2>📤 Upload Your File</h2>", unsafe_allow_html=True)
files = st.sidebar.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]

       
        df = pd.read_csv(BytesIO(file.getvalue())) if ext == "csv" else pd.read_excel(BytesIO(file.getvalue()), engine="openpyxl")

        st.subheader(f"📊 {file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"🗑 Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("✅ Duplicates Removed!")
            st.dataframe(df.head())

       
        if st.checkbox(f"🔄 Fill Missing Values with Mean - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("✅ Missing Values Filled with Column Means!")
            st.dataframe(df.head())

      
        selected_columns = st.multiselect(f"🎯 Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

       
        num_df = df.select_dtypes(include="number")
        if st.checkbox(f"📈 Show Chart - {file.name}") and not num_df.empty and len(num_df.columns) >= 2:
            with st.container():
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.bar_chart(num_df.iloc[:, :2])
                st.markdown("</div>", unsafe_allow_html=True)

      
        format_choice = st.radio(f"📂 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

      
        if st.button(f"⬇ Download {file.name} as {format_choice}"):
            output = BytesIO()
            file_name, _ = os.path.splitext(file.name)
            new_name = f"{file_name}.csv" if format_choice == "CSV" else f"{file_name}.xlsx"

            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            output.seek(0)
            st.download_button(label=f"⬇ Download {new_name}", data=output, file_name=new_name, mime=mime)

            st.success("✅ Processing Complete! 🎉")
