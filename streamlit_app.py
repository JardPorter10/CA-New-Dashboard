import streamlit as st
import pandas as pd
import plotly.express as px  # ✅ Using Plotly instead of Matplotlib

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Container Atlas", layout="wide")

# --- DROPDOWN MENU (Now visible, not in sidebar) ---
st.title("📊 My Data Dashboard")

trade_lanes = [
    "All of my Lanes",
    "China to North America West Coast",
    "China to North America East Coast",
    "Europe to North America East Coast",
    "China to Mediterranean",
    "North America East Coast to China",
    "North America West Coast to China",
]
selected_lane = st.selectbox("Select a Trade Lane:", trade_lanes)

# --- LAYOUT: CHART ON LEFT, DATA CARDS ON RIGHT ---
col1, col2 = st.columns([3, 1])  # Chart takes 3x more space than cards

# --- CHART SECTION ---
with col1:
    st.subheader("📈 FEU Spot Rate Change Over Time")

    # Fake data for now
    dates = pd.date_range(start="2024-01-01", periods=12, freq="M")
    values = [2500, 2600, 2450, 2700, 2900, 2800, 2750, 2950, 3100, 3000, 3200, 3300]
    df = pd.DataFrame({"Date": dates, "Rate": values})

    # ✅ PLOTTING WITH PLOTLY
    fig = px.line(df, x="Date", y="Rate", markers=True, title=f"Spot Rate Change for {selected_lane}")
    fig.update_layout(xaxis_title="Date", yaxis_title="Rate (USD per FEU)", template="plotly_dark")
    
    st.plotly_chart(fig, use_container_width=True)

# --- DATA CARDS SECTION ---
with col2:
    st.subheader("📌 Key Metrics")

    # ✅ Transit Time Card
    st.markdown("**⏳ Transit Time:**")
    st.info("35 Days")

    # ✅ Rate Pressure Card
    st.markdown("**📉 Rate Pressure:**")
    st.success("Slight Decrease")  # Use st.warning() or st.error() for increase
    st.caption("Measures rate pressure over the next 14 days.")

    # ✅ Rollover Index
    st.markdown("**🚢 Rollover Index:**")
    st.warning("22% of containers arrived on a different ship.")
    st.caption("Percentage of containers arriving on a different ship than booked.")
