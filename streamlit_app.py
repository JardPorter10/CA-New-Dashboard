import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Container Atlas", layout="wide")

# Load Data
def load_data():
    file_path = "Cleaned_FEU_Spot_Rate_Data.csv"  # Update this to your actual file
    df = pd.read_csv(file_path)
    return df

data = load_data()

def get_closest_match(query, choices):
    """Return the closest matching options for a given query."""
    query = query.lower()
    return [choice for choice in choices if query in choice.lower()]

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["My Dashboard", "Lane Dashboard", "Lane Analyzer", "Settings"])

if page == "Lane Analyzer":
    st.title("Lane Analyzer")
    
    # Extract unique origins and destinations from data
    unique_origins = data["Qualifier_Description"].unique().tolist()
    unique_destinations = data["Qualifier_Description"].unique().tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        origin_query = st.text_input("Enter Origin Port:")
        origin_suggestions = get_closest_match(origin_query, unique_origins) if origin_query else []
        origin = st.selectbox("Select Origin", origin_suggestions, index=0 if origin_suggestions else None)
    
    with col2:
        destination_query = st.text_input("Enter Destination Port:")
        destination_suggestions = get_closest_match(destination_query, unique_destinations) if destination_query else []
        destination = st.selectbox("Select Destination", destination_suggestions, index=0 if destination_suggestions else None)
    
    # Filter data based on selection
    if origin and destination:
        filtered_data = data[(data["Qualifier_Description"] == origin) & (data["Qualifier_Description"] == destination)]
    else:
        filtered_data = pd.DataFrame()
    
    if not filtered_data.empty:
        st.success("Data loaded successfully!")
        st.dataframe(filtered_data)
        
        # Plot spot rate data
        fig = px.line(filtered_data, x="Date", y="Spot_Rate", title=f"FEU Spot Rates: {origin} to {destination}")
        st.plotly_chart(fig)
    else:
        st.warning("No data found for the selected lane. Please refine your selection.")

