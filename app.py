import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="CSV Analyser", layout="centered")

st.title("📂 CSV ANALYSER")
st.subheader("Clean Your Messy CSVs 🧹")
st.write("This app will help you upload, clean, filter, and download CSV files with ease.")

# Initialize session state
if "original_df" not in st.session_state:
    st.session_state.original_df = None
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

# Upload Section
uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

if uploaded_file is not None and st.session_state.original_df is None:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.original_df = df
    except Exception as e:
        st.error(f"⚠️ Failed to read CSV: {e}")

# Display original data
if st.session_state.original_df is not None:
    st.write("📊 Original Data Preview:")
    st.dataframe(st.session_state.original_df.head())
    st.write("📐 Shape:", st.session_state.original_df.shape)
    st.write("🧼 Null values count:", st.session_state.original_df.isnull().sum().sum())

    # Cleaning Button
    if st.button("🧹 Drop Missing Values"):
        cleaned = st.session_state.original_df.dropna()
        st.session_state.cleaned_df = cleaned
        st.success("Dropped rows with missing values.")

    # Reset Button
    if st.button("🔁 Reset to Original"):
        st.session_state.cleaned_df = st.session_state.original_df.copy()
        st.success("Data reset to original uploaded file.")

# Work with Cleaned Data
if st.session_state.cleaned_df is not None:
    df = st.session_state.cleaned_df
    st.write("✅ Cleaned Data:")
    st.dataframe(df.head())
    st.write("📐 New Shape:", df.shape)

    # Column Filter
    columns_to_keep = st.multiselect("🎯 Select columns to keep", df.columns.tolist())
    if columns_to_keep:
        filtered_df = df[columns_to_keep]
        st.write("🎯 Filtered Data:")
        st.dataframe(filtered_df)
        st.session_state.filtered_data= filtered_df

        # Download Button
        csv_buffer = io.StringIO()
        filtered_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_buffer.getvalue(),
            file_name="cleaned.csv",
            mime="text/csv"
        )
    else:
        st.info("ℹ️ Select at least one column to filter.")
