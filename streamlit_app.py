import pandas as pd
import streamlit as st

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv("Cleaned_FEU_Spot_Rate_Data.csv")

# Read data
df = load_data()

# Display DataFrame (for testing)
st.subheader("FEU Spot Rate Data Preview")
st.dataframe(df.head())
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

# --- MY DASHBOARD PAGE ---
if page == "My Dashboard":
    st.title("📊 My Data Dashboard")

    # **Dropdown for Lane Selection**
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

    # **Lookback Period & Custom Date Selection**
    col1, col2 = st.columns([1, 2])
    with col1:
        lookback = st.selectbox("Lookback Period:", list(lookback_options.keys()))

    with col2:
        date_range = st.date_input("Select Date Range:", [])

    # Layout: Chart Left, Cards Right
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("📈 FEU Spot Rate Change Over Time")

        # **Fake Data Generation**
        num_days = lookback_options[lookback]
        dates = pd.date_range(end=pd.Timestamp.today(), periods=num_days, freq="D")
        values = pd.Series(range(num_days)) + 2500  # Simulated data

        df = pd.DataFrame({"Date": dates, "Rate": values})

        # **Plotly Chart**
        fig = px.line(df, x="Date", y="Rate", markers=True, title=f"Spot Rate Change for {selected_lane}")
        fig.update_traces(line=dict(color="blue", width=3))  # Primary lane always blue
        fig.update_layout(xaxis_title="Date", yaxis_title="Rate (USD per FEU)", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📌 Key Metrics")
        st.markdown("**⏳ Transit Time:**")
        st.info("35 Days")
        st.markdown("**📉 Rate Pressure:**")
        st.success("Slight Decrease")
        st.markdown("**🚢 Rollover Index:**")
        st.warning("22% of containers arrived on a different ship.")

# --- LANE DASHBOARD PAGE ---
elif page == "Lane Dashboard":
    st.title("📂 Lane Dashboard")
    st.write("🔍 **Search for specific trade lanes and receive operational & analytical data.**")

    # **Search Function - Origin & Destination**
    st.subheader("🔎 Search Trade Lanes")
    ports = [
        "North America East Coast", "North America West Coast", "South America",
        "Latin America", "Mediterranean / North Africa", "China / Southeast Asia",
        "Sub Saharan Africa", "North Europe", "Oceania"
    ]
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        origin = st.selectbox("Select Origin Port:", ports, key="origin")
    with col2:
        destination = st.selectbox("Select Destination Port:", ports, key="destination")
    with col3:
        if st.button("Search"):
            st.success(f"Showing results for {origin} → {destination}")
        if st.button("Clear"):
            st.experimental_rerun()

    # **Lookback Period & Custom Date Selection**
    col1, col2 = st.columns([1, 2])
    with col1:
        lookback = st.selectbox("Lookback Period:", list(lookback_options.keys()), key="lane_lookback")
    with col2:
        date_range = st.date_input("Select Date Range:", [], key="lane_date_range")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"📈 FEU Spot Rate Change: {origin} → {destination}")
        num_days = lookback_options[lookback]
        dates = pd.date_range(end=pd.Timestamp.today(), periods=num_days, freq="D")
        values = pd.Series(range(num_days)) + 2600
        df = pd.DataFrame({"Date": dates, "Rate": values})

        fig = px.line(df, x="Date", y="Rate", markers=True, title=f"Spot Rate Change for {origin} → {destination}")
        fig.update_layout(xaxis_title="Date", yaxis_title="Rate (USD per FEU)", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📌 Key Metrics")
        st.markdown("**⏳ Transit Time:**")
        st.info("40 Days")
        st.markdown("**📉 Rate Pressure:**")
        st.warning("Increase")
        st.markdown("**🚢 Rollover Index:**")
        st.error("30% of containers arrived on a different ship.")

# --- LANE ANALYZER PAGE ---
elif page == "Lane Analyzer":
    st.title("🔬 Lane Analyzer")
    st.write("📊 **Compare lanes, visualize trends, and analyze performance.**")

    # **Lane Selection for Comparison**
    st.subheader("📊 Compare Multiple Lanes")

    all_lanes = [
        "China to North America West Coast",
        "China to North America East Coast",
        "Europe to North America East Coast",
        "China to Mediterranean",
        "North America East Coast to China",
        "North America West Coast to China",
    ]
    primary_lane = st.selectbox("Primary Lane (🔵 Blue):", all_lanes, index=0)
    compare_lanes = st.multiselect("Compare Additional Lanes:", all_lanes, default=[])

    # **Lookback Period Selection**
    lookback = st.selectbox("Lookback Period:", list(lookback_options.keys()), key="analyzer_lookback")

    # Generate Fake Data
    num_days = lookback_options[lookback]
    dates = pd.date_range(end=pd.Timestamp.today(), periods=num_days, freq="D")
    primary_values = pd.Series(range(num_days)) + 2500  # Simulated data

    df_primary = pd.DataFrame({"Date": dates, "Rate": primary_values, "Lane": primary_lane})

    # Create data for comparison lanes
    comparison_data = []
    colors = px.colors.qualitative.Set1  # Different colors for comparison lanes
    for i, lane in enumerate(compare_lanes):
        comp_values = pd.Series(range(num_days)) + 2700 + (i * 100)  # Simulated variance
        temp_df = pd.DataFrame({"Date": dates, "Rate": comp_values, "Lane": lane})
        comparison_data.append(temp_df)

    # Combine Data
    df_all = pd.concat([df_primary] + comparison_data)

    # **Plot Multiple Lanes**
    fig = px.line(df_all, x="Date", y="Rate", color="Lane", markers=True,
                  title="Lane Rate Comparison", color_discrete_sequence=["blue"] + colors)
    fig.update_layout(xaxis_title="Date", yaxis_title="Rate (USD per FEU)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- SETTINGS PAGE ---
elif page == "Settings":
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Settings")
    st.write("🔧 **Customize your dashboard settings here.**")
    st.info("🚧 Feature under construction!")


