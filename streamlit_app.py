import streamlit as st
import pandas as pd
import plotly.express as px
from fuzzywuzzy import process

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Container Atlas", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["My Dashboard", "Lane Dashboard", "Lane Analyzer", "Settings"])

# --- LOAD DATA ---
data_path = "Cleaned_FEU_Spot_Rate_Data.csv"
df = pd.read_csv(data_path)

def get_closest_match(query, choices):
    """Returns the best match for a query from a list of choices."""
    match, score = process.extractOne(query, choices)
    return match if score > 70 else None  # Only return matches above 70% confidence

# --- LANE DASHBOARD ---
if page == "Lane Dashboard":
    st.title("🚢 Lane Dashboard")
    
    # Get unique origin and destination options from the dataset
    origins = df['Qualifier_Description'].unique().tolist()
    destinations = df['Qualifier_Description'].unique().tolist()
    
    # Search fields for Origin and Destination
    origin_input = st.text_input("Enter Origin Port", "")
    destination_input = st.text_input("Enter Destination Port", "")
    
    # Suggest closest matches
    origin_match = get_closest_match(origin_input, origins) if origin_input else None
    destination_match = get_closest_match(destination_input, destinations) if destination_input else None
    
    # Display match suggestions
    if origin_match:
        st.write(f"Suggested Origin: **{origin_match}**")
    if destination_match:
        st.write(f"Suggested Destination: **{destination_match}**")
    
    # Search button
    if st.button("Search"):
        if origin_match and destination_match:
            lane_data = df[(df['Qualifier_Description'] == origin_match) & (df['Qualifier_Description'] == destination_match)]
            if not lane_data.empty:
                st.success("✅ Data loaded successfully!")
                st.write(lane_data)
            else:
                st.error("No data found for the selected lane.")
        else:
            st.error("Please enter valid Origin and Destination.")
    
    # Clear button
    if st.button("Clear"):
        st.experimental_rerun()

# --- DUMMY DATA CARDS (TO BE REPLACED LATER) ---
if page in ["My Dashboard", "Lane Dashboard"]:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="📦 Transit Time (Days)", value="25")
    with col2:
        st.metric(label="📈 Rate Pressure", value="Neutral")
    with col3:
        st.metric(label="🚢 Rollover Index", value="12%")


