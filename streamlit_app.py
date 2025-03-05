import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Container Atlas", layout="wide")

# --- DROPDOWN MENU ---
st.sidebar.title("My Lanes")
trade_lanes = [
    "All of my Lanes",
    "China to North America West Coast",
    "China to North America East Coast",
    "Europe to North America East Coast",
    "China to Mediterranean",
    "North America East Coast to China",
    "North America West Coast to China",
]
selected_lane = st.sidebar.selectbox("Select a Trade Lane:", trade_lanes)

# --- LAYOUT: SPLIT INTO TWO COLUMNS ---
col1, col2 = st.columns([3, 1])  # Column 1 (chart) takes 3x more space than column 2 (cards)

# --- CHART SECTION ---
with col1:
    st.subheader("📊 FEU Spot Rate Change Over Time")
    
    # Fake data for now
    dates = pd.date_range(start="2024-01-01", periods=12, freq="M")
    values = [2500, 2600, 2450, 2700, 2900, 2800, 2750, 2950, 3100, 3000, 3200, 3300]
    df = pd.DataFrame({"Date": dates, "Rate": values})
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["Date"], df["Rate"], marker="o", linestyle="-", color="blue")
    ax.set_title(f"Spot Rate Change for {selected_lane}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Rate (USD per FEU)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- DATA CARDS SECTION ---
with col2:
    st.subheader("📌 Key Metrics")
    
    # Transit Time Card
    st.markdown("**⏳ Transit Time:**")
    st.info("35 Days")

    # Rate Pressure Card
    st.markdown("**📉 Rate Pressure:**")
    st.success("Slight Decrease")  # Change success to danger for increase
    st.caption("Measures rate pressure over the next 14 days.")

    # Rollover Index
    st.markdown("**🚢 Rollover Index:**")
    st.warning("22% of containers arrived on a different ship.")
    st.caption("Percentage of containers arriving on a different ship than booked.")
