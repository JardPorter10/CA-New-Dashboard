import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Container Atlas", layout="wide")

# --- Load Data Function (with caching for efficiency) ---
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_FEU_Spot_Rate_Data.csv")
    df["Date"] = pd.to_datetime(df["Date"])  # Ensure Date column is datetime format
    return df

df = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["My Dashboard", "Lane Dashboard", "Lane Analyzer", "Settings"])

# --- MY DASHBOARD PAGE ---
if page == "My Dashboard":
    st.title("📊 My Data Dashboard")
    
    # Dropdown for Lane Selection
    trade_lanes = df["Qualifier_Description"].unique().tolist()
    selected_lane = st.selectbox("Select Trade Lane", trade_lanes)

    # Filter Data Based on Selection
    filtered_data = df[df["Qualifier_Description"] == selected_lane]

    # Plot with Plotly
    fig = px.line(
        filtered_data, 
        x="Date", 
        y="Spot_Rate", 
        title=f"Spot Rate for {selected_lane}",
        labels={"Spot_Rate": "FEU Spot Rate ($)", "Date": "Date"}
    )
    st.plotly_chart(fig)

# --- LANE DASHBOARD PAGE ---
elif page == "Lane Dashboard":
    st.title("🔍 Lane Dashboard")

    # Search Inputs
    origin = st.text_input("Enter Origin Port")
    destination = st.text_input("Enter Destination Port")
    search_button = st.button("Search")

    if search_button:
        # Generate Lane Code (Example: CNER = China to North Europe)
        lane_code = origin[:3].upper() + destination[:3].upper()

        if lane_code in df["Qualifier"].values:
            filtered_lane = df[df["Qualifier"] == lane_code]
            fig = px.line(
                filtered_lane, 
                x="Date", 
                y="Spot_Rate", 
                title=f"Spot Rate for {origin} to {destination}",
                labels={"Spot_Rate": "FEU Spot Rate ($)", "Date": "Date"}
            )
            st.plotly_chart(fig)
        else:
            st.warning("Lane not found. Please check your input.")

# --- SETTINGS PAGE ---
elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("This page will allow you to configure your dashboard settings in the future.")



