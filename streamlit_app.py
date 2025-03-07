import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Lane Dashboard", layout="wide")

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
    .sidebar-card-global {
        background-color: #0068FF;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: white;
        font-size: 14px;
    }
    .sidebar-card {
        background-color: #2A2A2E;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: white;
        font-size: 14px;
    }
    .tag {
        border: 1px solid #3B82F6;
        padding: 2px 4px;
        border-radius: 4px;
        display: inline-block;
        font-size: 12px;
        color: #3B82F6;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    page = st.selectbox("Navigation", ["Lane Dashboard", "Supply & Demand", "US Customs Dashboard", "Settings"], index=0)

    st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"], index=1)

    with st.expander("GLOBAL", expanded=True):
        st.markdown('<div class="sidebar-card-global">'
                    '<span class="tag">GLBL</span><br>'
                    '<strong>Global Container Freight Index</strong><br>'
                    '$3,612 <span style="color: #22C55E;">+1%</span></div>', unsafe_allow_html=True)

    with st.expander("MY ROUTES", expanded=True):
        routes = [
            {"tag": "SNR 01", "route": "Shanghai, China → Houston, TX, USA", "value": "$5,885", "delta": "+3%"},
            {"tag": "SNR 03", "route": "Norfolk, VA, USA → Rotterdam, NED", "value": "$299", "delta": "-1%"},
        ]
        for r in routes:
            st.markdown(f"""
                <div class='sidebar-card'>
                <span class='tag'>{r['tag']}</span><br>
                <strong>{r['route']}</strong><br>
                {r['value']} <span style='color:{"#10B981" if '+' in r['delta'] else "#EF4444"}'>{r['delta']}</span>
            </div>""", unsafe_allow_html=True)

    with st.expander("CORRIDORS"):
        st.selectbox("Pacific", ["Option 1", "Option 2"])

# Page routing
if page == "FEU Spot Rates Dashboard":
    st.title("FEU Spot Rates - Global")

    # Dummy Data
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

    with st.form(key="lane_search"):
        col_search1, col_search2, col_search3 = st.columns([2,2,1])
        origin = col_search1.text_input("Origin Port", "Shanghai, China")
        destination = col_search2.text_input("Destination Port", "Houston, Texas, USA")
        search_btn = col_search3.form_submit_button("Search")

    col1, col2 = st.columns([3, 1])

    # Chart
    with col1:
        data_option = st.selectbox("Chart Dataset", ["FEU Spot Rate", "Booking Volume", "TEU Rejections", 
                                                     "TEU Capacity", "Transit Times", "Port Delays", "Rollover Index"], 
                                  key='chart_dataset', index=0)

        fig = px.line(df, x='Date', y=data_option, markers=True, title=f"{data_option} Over Time")
        fig.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    # Right Metrics Cards
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(label="Current FEU Spot Rate", value="$3,612.4", delta="+1%")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**Rate Pressure**")
        pressure = 0.8
        color = "red" if pressure > 0.66 else "blue" if pressure > 0.33 else "green"
        st.write("Rate Pressure Index provides directional indicator for FEU spot rates for the next 14 days.")
        st.progress(pressure)
        st.markdown("Sharp Increase")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Transit Time", "38 Days")
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Table
    st.markdown("### Top Regional Lanes")
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
else:
    st.header(page)
    st.write("Dashboard content for this section will go here.")
