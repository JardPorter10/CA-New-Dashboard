import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Container Atlas", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["My Dashboard", "Lane Dashboard", "Analytics", "Settings"])

# --- HEADER ---
st.title("📊 Container Atlas")
st.write("Welcome! This is a simple dashboard framework.")

# --- LAYOUT: SECTIONS FOR EACH PAGE ---
if page == "My Dashboard":
    st.header("🏠 My Dashboard")
    st.write("This is where items like my lanes, my network analytics, and other items will live.")
    
    # Dropdown for Lane Selection
    lanes = [
        "All of my Lanes", 
        "China to North America West Coast", 
        "China to North America East Coast", 
        "Europe to North America East Coast", 
        "China to Mediterranean", 
        "North America East Coast to China", 
        "North America West Coast to China"
    ]
    selected_lane = st.selectbox("Select a Lane:", lanes)
    
    # Placeholder Data for FEU Spot Rate
    df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=12, freq='M'),
        "FEU Spot Rate": [2500, 2700, 2600, 2800, 2900, 3100, 3000, 3200, 3100, 3300, 3400, 3500]
    })

    # Create the Matplotlib chart
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["FEU Spot Rate"], marker="o", linestyle="-")
    ax.set_title("FEU Spot Rate Change Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Rate (USD)")

    # Display chart in Streamlit
    st.pyplot(fig)
    
    # Transit Time Card
    st.metric(label="Transit Time (Days)", value="25 Days")
    
    # Rate Pressure Indicator
    st.write("### Rate Pressure")
    rate_pressure = "Slight Increase"
    st.progress(66)  # Placeholder for diffusion scale
    st.write(f"Current Rate Pressure: **{rate_pressure}**")
    
    # Rollover Index Card
    st.metric(label="Rollover Index", value="12.5%")

elif page == "Lane Dashboard":
    st.header("📂 Lane Dashboard")
    st.write("This is where users will be able to search lanes and receive back operational and analytical data.")

elif page == "Analytics":
    st.header("📈 Analytics")
    st.write("This section will have charts and insights to compare specific Ocean Data.")

elif page == "Settings":
    st.header("⚙️ Settings")
    st.write("This is where users can customize their My Dashboard settings.")

# --- FOOTER ---
st.markdown("---")
st.write("🚀 Built with Streamlit | *Prototype Version*")
