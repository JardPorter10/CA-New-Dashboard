import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Container Atlas", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["My Dashboard", "Lane Dashboard", "Lane Analyzer", "Settings"])

# --- LOOKBACK PERIOD OPTIONS ---
lookback_options = {
    "1 Month": 30,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year": 365,
    "5 Years": 1825
}

# --- TRADE LANE MAPPINGS ---
lane_options = {
    "China / Southeast Asia": "C",
    "North America West Coast": "NAW",
    "North America East Coast": "NAE",
    "North Europe": "NER",
    "Mediterranean / North Africa": "MED",
    "Europe": "E",
    "South America West": "SAW",
    "South America East": "SAE",
    "Global": "GLBL"
}

# --- LOADING EXCEL DATA ---
data_file = "Cleaned_FEU_Spot_Rate_Data.csv"
data = pd.read_csv(data_file)

# --- MY DASHBOARD PAGE ---
if page == "My Dashboard":
    st.title("📊 My Data Dashboard")
    
    # **Dropdown for Lane Selection**
    selected_lane = st.selectbox("Select a Trade Lane", ["All of my Lanes"] + list(lane_options.keys()))
    
    # **Lookback Period Selection**
    lookback = st.selectbox("Select Lookback Period", list(lookback_options.keys()))
    lookback_days = lookback_options[lookback]
    
    # **Filter Data**
    if selected_lane != "All of my Lanes":
        lane_code = lane_options[selected_lane]
        filtered_data = data[data["Qualifier"] == lane_code]
    else:
        filtered_data = data
    
    # **Plotly Chart**
    fig = px.line(filtered_data, x="Date", y="Spot_Rate", color="Qualifier_Description", title="FEU Spot Rate Trends")
    st.plotly_chart(fig, use_container_width=True)
    
    # **Additional Data Cards**
    col1, col2, col3 = st.columns(3)
    col1.metric("Transit Time", "35 Days")
    col2.metric("Rate Pressure", "Slight Increase")
    col3.metric("Rollover Index", "22% Delayed")

# --- LANE DASHBOARD PAGE ---
if page == "Lane Dashboard":
    st.title("🛳 Lane Dashboard")
    
    # **Search Fields**
    origin = st.text_input("Origin Port", "")
    destination = st.text_input("Destination Port", "")
    
    # **Autocomplete Suggestions**
    matching_origins = [port for port in lane_options.keys() if origin.lower() in port.lower()]
    matching_destinations = [port for port in lane_options.keys() if destination.lower() in port.lower()]
    
    selected_origin = st.selectbox("Matching Origins", matching_origins if matching_origins else ["No Match"], index=0)
    selected_destination = st.selectbox("Matching Destinations", matching_destinations if matching_destinations else ["No Match"], index=0)
    
    # **Search & Clear Buttons**
    col1, col2 = st.columns(2)
    if col1.button("Search"):
        origin_code = lane_options.get(selected_origin, "")
        destination_code = lane_options.get(selected_destination, "")
        filtered_data = data[(data["Qualifier"] == f"{origin_code}{destination_code}")]
    
    if col2.button("Clear"):
        st.experimental_rerun()
    
    # **Plotly Chart for Searched Lane**
    if 'filtered_data' in locals() and not filtered_data.empty:
        fig = px.line(filtered_data, x="Date", y="Spot_Rate", title=f"Spot Rate Trend: {selected_origin} to {selected_destination}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for the selected lane.")
