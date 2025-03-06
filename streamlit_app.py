import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Set page configuration
st.set_page_config(page_title="FEU Spot Rates Dashboard", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #111827;
}

.stMetric {
    background-color: #151925;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

[data-testid="stMetricDelta"] svg {
    vertical-align: middle;
}

/* Hide Streamlit default header/footer */
#MainMenu, footer, header {visibility: hidden;}

""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.selectbox("Frequency", ["Weekly", "Monthly", "Daily"], index=0)

    with st.expander("**GLOBAL**", expanded=True):
        st.metric(label="Global Container Freight Index", value="$3,612", delta="+1%")

    with st.expander("MY ROUTES", expanded=True):
        st.metric("Shanghai → Houston", "$5,885", delta="+3%")
        st.metric("Norfolk → Rotterdam", "$299", delta="-1%")

    with st.expander("CORRIDORS"):
        st.selectbox("Pacific", ["Option 1", "Option 2"])

# Main dashboard
st.title("FEU Spot Rates - Global")

col1, col2 = st.columns([3, 1])

# Main Chart Area
with col1:
    data_selection = st.selectbox("Chart Dataset", [
        "Booking Volume", "TEU Rejections", "TEU Capacity",
        "Transit Times", "Port Delays", "Rollover Index"
    ])

    fig = go.Figure()
    fig_dates = pd.date_range(start='2024-07-07', periods=5, freq='W')
    fig = go.Figure()

    fig_data = [3600, 3500, 3450, 3525, 3612]  # Example data

    fig = go.Figure(data=[
        go.Scatter(x=fig_data, y=["11-Jul", "18-Jul", "25-Jul", "01-Aug", "08-Aug"],
                   mode='lines+markers', line=dict(color='#A78BFA'))
    ])

    fig.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="#FFFFFF"),
        xaxis=dict(title="Date"),
        yaxis=dict(title="FEU Spot Rate ($)")
    )

    st.plotly_chart(fig, use_container_width=True)

# Metrics Sidebar
with col2:
    st.markdown("### CURRENT FEU SPOT RATE")
    st.markdown("<div class='stMetric'>$3,612.4 <span style='color:#1eff70'>+1%</span></div>", unsafe_allow_html=True)

    st.markdown("#### Rate Pressure")
    st.write("Rate Pressure Index provides directional indicator of FEU spot rates for the next 14 days.")
    st.progress(80)
    st.markdown("**Sharp Increase**")

    st.markdown("---")

    st.metric("Transit Time", "38 Days")

# Bottom Data Table
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

st.subheader("Top Regional Lanes")
st.dataframe(fig_data, hide_index=True, use_container_width=True)
