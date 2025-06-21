import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 🌐 Page Config
st.set_page_config(page_title="Data Visualizer AI", layout="centered")

st.title("📊 AI-Powered Data Visualizer")
st.markdown("Upload your CSV/Excel file and choose a visualization type.")

# 📁 File Uploader
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])

# 🧼 Data Cleaning Function
def clean_data(df):
    df_clean = df.copy()
    df_clean.dropna(axis=1, how='all', inplace=True)
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
        else:
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
    return df_clean

# 📊 Main App Logic
if uploaded_file is not None:
    # Load data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean data
    df = clean_data(df)
    st.subheader("🔍 Cleaned Data Preview")
    st.dataframe(df.head())

    # Choose visualization
    viz_type = st.selectbox("Select visualization type", [
        "Pairplot", 
        "Correlation Heatmap", 
        "Countplot (categorical)", 
        "Boxplot (numeric vs category)", 
        "Histogram"
    ])

    # Column types
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()

    # Plot
    st.subheader("📈 Generated Visualization")
    fig = plt.figure()

    try:
        if viz_type == "Pairplot" and len(numeric_cols) >= 2:
            fig = sns.pairplot(df[numeric_cols])
            st.pyplot(fig)

        elif viz_type == "Correlation Heatmap" and len(numeric_cols) >= 2:
            plt.figure(figsize=(10, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
            st.pyplot(plt.gcf())

        elif viz_type == "Countplot (categorical)" and cat_cols:
            selected_col = st.selectbox("Choose a categorical column", cat_cols)
            sns.countplot(x=selected_col, data=df)
            plt.xticks(rotation=45)
            st.pyplot(plt.gcf())

        elif viz_type == "Boxplot (numeric vs category)" and numeric_cols and cat_cols:
            selected_num = st.selectbox("Numeric column", numeric_cols)
            selected_cat = st.selectbox("Categorical column", cat_cols)
            sns.boxplot(x=selected_cat, y=selected_num, data=df)
            plt.xticks(rotation=45)
            st.pyplot(plt.gcf())

        elif viz_type == "Histogram" and numeric_cols:
            selected_col = st.selectbox("Choose a numeric column", numeric_cols)
            sns.histplot(df[selected_col], bins=20, kde=True)
            st.pyplot(plt.gcf())

        else:
            st.warning("Insufficient data or unsupported selection.")
    except Exception as e:
        st.error(f"❌ Error generating visualization: {e}")
