import streamlit as st
import pandas as pd
import plotly.express as px  # ✅ Using Plotly for charts

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Container Atlas", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["My Dashboard", "Lane Dashboard", "Lane Analyzer", "Settings"])

# --- MY DASHBOARD PAGE ---
if page == "My Dashboard":
    st.title("📊 My Data Dashboard")

    # Dropdown Menu for Lanes
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

    # Layout: Chart on Left, Cards on Right
    col1, col2 = st.columns([3, 1])  # Chart takes 3x more space than cards

    # --- CHART SECTION ---
    with col1:
        st.subheader("📈 FEU Spot Rate Change Over Time")

        # Fake Data
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

# --- LANE DASHBOARD PAGE ---
elif page == "Lane Dashboard":
    st.title("📂 Lane Dashboard")
    st.write("🔍 **Search for specific trade lanes and receive operational & analytical data.**")

    # Search Function - Origin & Destination
    st.subheader("🔎 Search Trade Lanes")

    ports = [
        "North America East Coast",
        "North America West Coast",
        "South America",
        "Latin America",
        "Mediterranean / North Africa",
        "China / Southeast Asia",
        "Sub Saharan Africa",
        "North Europe",
        "Oceania"
    ]

    col1, col2, col3 = st.columns([2, 2, 1])  # Search layout: Two dropdowns + Button column

    with col1:
        origin = st.selectbox("Select Origin Port:", ports, key="origin")

    with col2:
        destination = st.selectbox("Select Destination Port:", ports, key="destination")

    with col3:
        if st.button("Search"):
            st.success(f"Showing results for {origin} → {destination}")

        if st.button("Clear"):
            st.experimental_rerun()  # Resets search fields

    # Layout: Chart on Left, Cards on Right
    col1, col2 = st.columns([3, 1])

    # --- CHART SECTION ---
    with col1:
        st.subheader(f"📈 FEU Spot Rate Change: {origin} → {destination}")

        # Fake Data for Search Results
        dates = pd.date_range(start="2024-01-01", periods=12, freq="M")
        values = [2600, 2700, 2800, 2900, 3050, 3150, 3200, 3300, 3400, 3450, 3500, 3600]
        df = pd.DataFrame({"Date": dates, "Rate": values})

        # ✅ PLOTTING WITH PLOTLY
        fig = px.line(df, x="Date", y="Rate", markers=True, title=f"Spot Rate Change for {origin} → {destination}")
        fig.update_layout(xaxis_title="Date", yaxis_title="Rate (USD per FEU)", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # --- DATA CARDS SECTION ---
    with col2:
        st.subheader("📌 Key Metrics")

        # ✅ Transit Time Card
        st.markdown("**⏳ Transit Time:**")
        st.info("40 Days")  # Example data

        # ✅ Rate Pressure Card
        st.markdown("**📉 Rate Pressure:**")
        st.warning("Increase")
        st.caption("Measures rate pressure over the next 14 days.")

        # ✅ Rollover Index
        st.markdown("**🚢 Rollover Index:**")
        st.error("30% of containers arrived on a different ship.")
        st.caption("Percentage of containers arriving on a different ship than booked.")

# --- LANE ANALYZER PAGE ---
elif page == "Lane Analyzer":
    st.title("🔬 Lane Analyzer")
    st.write("📊 **Compare lanes, visualize trends, and analyze performance.**")
    st.info("🚧 Feature under construction!")

# --- SETTINGS PAGE (ALWAYS AT BOTTOM LEFT) ---
elif page == "Settings":
    st.sidebar.markdown("---")  # Divider line
    st.sidebar.subheader("⚙️ Settings")
    st.write("🔧 **Customize your dashboard settings here.**")
    st.info("🚧 Feature under construction!")



