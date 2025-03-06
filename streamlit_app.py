import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="FEU Spot Rates Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    body, .stApp { background-color: black; color: white; }
    .metric-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        border: 1px solid #333;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    .sidebar-card {
        background-color: #2A2A2E;
        padding: 8px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"], index=1)

    st.markdown("### Global")
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.metric("Global Container Freight Index", "$3,612", delta="+1%")

    st.markdown("### My Routes")
    routes = [
        {"route": "Shanghai → Houston", "value": "$5,885", "delta": "+3%"},
        {"route": "Norfolk → Rotterdam", "value": "$299", "delta": "-1%"}
    ]
    for route in routes:
        st.markdown(f"""
        <div class="sidebar-card">{route["route"]}: {route['value']} ({route['delta']})</div>", unsafe_allow_html=True)

# Main Area
st.title("FEU Spot Rates - Global")

# Lane Search above chart
with st.form(key="lane_search"):
    col_search1, col_search2, col_search3 = st.columns([2,2,1])
    origin = col_search1.text_input("Origin Port", "Shanghai, China")
    destination = col_search2.text_input("Destination Port", "Houston, Texas, USA")
    col_search3.form_submit_button("Search")

col1, col2 = st.columns([3, 1])

# Dummy Data
import pandas as pd
import plotly.express as px

dates = pd.date_range('2024-07-07', periods=5, freq='W')
df = pd.DataFrame({
    'Date': dates,
    'FEU Spot Rate': [3600, 3550, 3480, 3500, 3612],
    'Booking Volume': [250, 270, 265, 280, 290],
    'TEU Rejections': [5, 7, 6, 8, 5],
    'TEU Capacity': [100, 110, 105, 120, 115],
    'Transit Times': [38, 37, 39, 40, 38],
    'Port Delays': [3, 2, 4, 3, 5],
    'Rollover Index': [12, 14, 13, 15, 10]
})

# Chart
with col1:
    data_option = st.selectbox("Chart Dataset", [
        "FEU Spot Rate", "Booking Volume", "TEU Rejections", 
        "TEU Capacity", "Transit Times", "Port Delays", "Rollover Index"], 
        key='chart_dataset', index=0)

    fig = px.line(df, x='Date', y=data_option, markers=True, title=f"{data_option} Over Time")
    fig.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font_color="white")

    st.plotly_chart(fig, use_container_width=True)

# Cards on right
with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("Current FEU Spot Rate", "$3,612.4", delta="+1%")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("**Rate Pressure**")
    pressure = 0.8
    color = "red" if pressure_value > 0.66 else "blue" if pressure_value > 0.33 else "green"
    st.markdown(f"<div style='color:{color};'>Sharp Increase</div>", unsafe_allow_html=True)
    st.progress(pressure_value)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("Transit Time", "38 Days")
    st.markdown("</div>", unsafe_allow_html=True)

# Bottom Table
st.subheader("Top Regional Lanes")
lanes_data = pd.DataFrame({
    'Abbreviation': ['CNSHA-USHOU', 'USORF-NLRTM'],
    'Origin Port': ['Shanghai, CHN', 'Norfolk, VA, USA'],
    'Destination Port': ['Houston, TX, USA', 'Rotterdam, NED'],
    'FEU Spot Rate': ['$5,885', '$200'],
    '% Change': ['3%', '-1%'],
    'Rate Pressure': ['Sharp Increase', 'Neutral'],
    'Transit Time': ['38 Days', '12 Days']
})
st.dataframe(lanes_data, use_container_width=True, hide_index=True)
