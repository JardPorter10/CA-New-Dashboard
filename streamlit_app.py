import streamlit as st
import pandas as pd

# Load Data
try:
    df = pd.read_csv("Cleaned_FEU_Spot_Rate_Data.csv")
    st.write("Dataset loaded successfully!")
except Exception as e:
    st.error(f"Error loading CSV: {e}")

# Check Column Names
st.write("Columns in dataset:", df.columns)

# Ensure Correct Column Name
expected_columns = ["Origin", "Destination", "Spot_Rate"]  # Adjust based on actual CSV
missing_columns = [col for col in expected_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing expected columns: {missing_columns}")
else:
    # Proceed with filtering & dashboard logic
    unique_origins = df["Origin"].dropna().unique().tolist()
    st.write("Unique Origins:", unique_origins)

# --- Streamlit App ---
st.set_page_config(page_title="Container Atlas", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["My Dashboard", "Lane Dashboard", "Lane Analyzer", "Settings"])

if page == "Lane Dashboard":
    st.title("Lane Dashboard")
    
    # Lane selection
    origin_input = st.text_input("Enter Origin:")
    destination_input = st.text_input("Enter Destination:")
    
    # Suggest closest matches
    filtered_df = df.copy()
    if origin_input:
        filtered_df = filtered_df[filtered_df["Origin"].str.contains(origin_input, case=False, na=False)]
    if destination_input:
        filtered_df = filtered_df[filtered_df["Destination"].str.contains(destination_input, case=False, na=False)]
    
    if not filtered_df.empty:
        st.dataframe(filtered_df)
    else:
        st.warning("No matching lanes found. Try adjusting your search.")

elif page == "My Dashboard":
    st.title("My Dashboard")
    st.write("Welcome to My Dashboard!")

elif page == "Lane Analyzer":
    st.title("Lane Analyzer")
    st.write("Analyze specific trade lanes here.")

elif page == "Settings":
    st.title("Settings")
    st.write("Adjust application settings here.")
