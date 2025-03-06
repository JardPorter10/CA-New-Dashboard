import streamlit as st
import pandas as pd
import plotly.express as px

# App Config
st.set_page_config(page_title="FEU Spot Rates Dashboard", layout="wide")

# Sidebar Navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Go to", ["My Dashboard", "Lane Dashboard", "Lane Analyzer", "Settings"])

    st.markdown("---")

    st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"], index=1)

    # Lane Search Functionality
    st.markdown("### Lane Search")
    with st.form(key="lane_search"):
        origin = st.text_input("Origin Port", "Shanghai, China")
        destination = st.text_input("Destination Port", "Houston, Texas, USA")
        submitted = st.form_submit_button("Search")

# Dummy Data
dates = pd.date_range(start='2024-07-07', periods=5, freq='W')
data = {
    'Date': dates,
    'FEU Spot Rate': [5200, 5100, 5000, 4950, 4800],
    'Booking Volume': [250, 270, 265, 280, 290],
    'TEU Rejections': [5, 7, 6, 8, 5],
    'TEU Capacity': [100, 110, 105, 120, 115],
    'Transit Time': [38, 37, 39, 40, 38],
    'Port Delays': [3, 2, 4, 3, 5],
    'Rollover Index': [12, 14, 13, 15, 10]
}
df = pd.DataFrame(data)

# Main Dashboard
st.title("FEU Spot Rates - Global")

# Dropdown for Data Type Selection
data_option = st.selectbox("Chart Dataset", ["FEU Spot Rate", "Booking Volume", "TEU Rejections", "TEU Capacity", "Transit Time", "Port Delays", "Rollover Index"])

# Plot
fig = px.line(df, x='Date', y=data_option, markers=True, title=f"{data_option} Over Time")
st.plotly_chart(fig, use_container_width=True)

# Summary Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Current FEU Spot Rate", value="$3,612.4", delta="+1%")

with col2:
    st.markdown("**Rate Pressure**")
    st.progress(90)  # Sharp Increase indicator
    st.caption("Sharp Increase")

with col3:
    st.metric(label="Transit Time", value="38 Days")

# Top Regional Lanes Table
st.subheader("Top Regional Lanes")
lanes_data = pd.DataFrame({
    'Abbreviation': ['CNSHA-USHOU', 'USORF-NLRTM'],
    'Origin Port': ['Shanghai, CHN', 'Norfolk, VA, USA'],
    'Destination Port': ['Houston, TX, USA', 'Rotterdam, NED'],
    'FEU Spot Rate': ["$5,885", "$200"],
    '% Change': ["+3%", "-1%"],
    'Rate Pressure': ["Sharp Increase", "Neutral"],
    'Transit Time': ["38 Days", "12 Days"]
})
st.dataframe(lanes_data, use_container_width=True, hide_index=True)
