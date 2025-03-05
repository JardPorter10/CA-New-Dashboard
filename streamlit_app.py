import streamlit as st
import pandas as pd
from rapidfuzz import process  # Ensure this is installed in requirements.txt

# --- PAGE CONFIGURATION --- (Must be the first Streamlit command)
st.set_page_config(page_title="Container Atlas", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    """Load and cache the dataset."""
    df = pd.read_csv("Cleaned_FEU_Spot_Rate_Data.csv")  # Ensure this file exists in the repo
    return df

df = load_data()

# Extract unique origins and destinations
unique_origins = df["Origin"].dropna().unique().tolist()
unique_destinations = df["Destination"].dropna().unique().tolist()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["My Dashboard", "Lane Dashboard", "Lane Analyzer", "Settings"])

# --- LANE DASHBOARD ---
if page == "Lane Dashboard":
    st.title("Lane Dashboard")
    st.write("Search and analyze specific trade lanes.")

    # Search box for Origin
    origin_input = st.text_input("Search for an Origin:")
    suggested_origin, _ = process.extractOne(origin_input, unique_origins) if origin_input else (None, None)
    
    # Search box for Destination
    destination_input = st.text_input("Search for a Destination:")
    suggested_destination, _ = process.extractOne(destination_input, unique_destinations) if destination_input else (None, None)
    
    if suggested_origin and suggested_destination:
        st.write(f"Selected Lane: **{suggested_origin} → {suggested_destination}**")
        filtered_df = df[(df["Origin"] == suggested_origin) & (df["Destination"] == suggested_destination)]
        st.dataframe(filtered_df)
    else:
        st.write("Type to search for a valid Origin and Destination.")

# --- DUMMY DATA CARDS ---
    st.subheader("Additional Data Metrics (Dummy Data)")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Transit Time (Days)", value="35", delta="+2")
    col2.metric(label="Rate Pressure", value="Stable", delta="-1%")
    col3.metric(label="Rollover Index", value="12%", delta="+3%")

st.write("\n\n")  # Spacing at the bottom


