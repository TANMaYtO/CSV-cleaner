import streamlit as st
import pandas as pd
import io
from sklearn.preprocessing import LabelEncoder,OneHotEncoder

st.set_page_config(page_title="CSV Analyser", layout="centered")

st.title("📂 CSV ANALYSER")
st.subheader("Clean Your Messy CSVs 🧹")
st.write("This app will help you upload, clean, filter, and download CSV files with ease.")

# Initialize session state
if "original_df" not in st.session_state:
    st.session_state.original_df = None
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
if 'dropped_data' not in st.session_state:
    st.session_state.droppped_data = None
if 'cat_col' not in st.session_state:
    st.session_state.cat_col = None
if 'num_col' not in st.session_state:
    st.session_state.num_col = None
if 'one_hot' not in st.session_state:
    st.session_state.one_hot = None

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
        st.write("📐 New Shape:", filtered_df.shape)
        st.write('The number of duplicated values are - ',filtered_df.duplicated().sum())
        st.session_state.filtered_data= filtered_df


    else:
        st.info("ℹ️ Select at least one column to filter.")

if st.session_state.filtered_data is not None:
    if st.button('Drop duplicates'):
        dropped_df = st.session_state.filtered_data
        dropped_df = df.drop_duplicates()
        st.write("📐 New Shape:", dropped_df.shape)
        st.session_state.dropped_data = dropped_df



        # Download Button
        csv_buffer = io.StringIO()
        dropped_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Cleaned CSV(till dropped duplicates)",
            data=csv_buffer.getvalue(),
            file_name="cleaned.csv",
            mime="text/csv"
        )

if st.session_state.dropped_data is not None:
    if st.button('Divide in numerical and catagorical colomns'):
        cat_col = dropped_df.select_dtypes("object")
        num_col = dropped_df.select_dtypes(exclude="O")
        st.session_state.cat_col = cat_col
        st.session_state.num_col = num_col
        st.write('catagorical colomn:')
        st.dataframe(cat_col)
        st.wrtie('numerical colomn:')
        st.dataframe(num_col)
        if st.session_state.cat_col is not None:
            if st.button('Encode catagorical colomns'):
                OHE = OneHotEncoder(drop= "if_binary")
                cat_col_encoded = OHE.fit_transform(cat_col).toarray()
                column_name = list(OHE.get_feature_names_out())
                one_hot = pd.DataFrame(cat_col_encoded,columns=column_name)
                st.write('encoded catagotical colomns:')
                st.dataframe(one_hot)
                st.session_state.one_hot = one_hot

                if st.session_state.one_hot is not None:
                    if st.button()


