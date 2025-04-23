import folium
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium

### INSTRUCTIONS ###
# 1. Install the required libraries:
#    pip install streamlit folium pandas plotly streamlit-folium
# 2. Save this code in a file named `streamlit_app.py`.
# 3. Run the Streamlit app:
#    streamlit run streamlit_app.py
# 4. Once you've finished, push the code to the GitHub repository.

# --- Page Config ---
st.set_page_config(page_title="Rise South City Community Dashboard", layout="wide")

# --- Pages ---
tab1, tab2 = st.tabs(["Risk Analysis", "Additional Information"])

# --- Risk Analysis Tab ---
with tab1:
    # Title and Description
    st.title("Risk Analysis")
    st.write("This dashboard provides insights into the risk associated with air pollution in South San Francisco."
             "and San Bruno.")
    
    # Weights Slider for Composite Risk Score
    st.subheader("Composite Risk Score Weights")
    st.write("Adjust the weights to see how they affect the overall risk score.")
    
    # --- Enkhjin ---
    # NOTE: It's not possible to use a dual thumb slider in Streamlit, so you can either use two separate sliders 
    # between 0% and 100% or a single slider for one weight and then take the complement for the other.

    # Search Bar
    # --- Mack ---
    search_query = st.text_input("Curious about a specific location? Enter a street address (eg. 123 Main St):")
    
    # Geocoding
    # NOTE: You would typically use a geocoding API here to convert the address to coordinates.
    # Use the results to later capture information about a specific census tract.

    # Map Visualization
    # --- Enkhjin ---
    st.subheader("[INSERT MAP NAME]")
    st.write("This map shows the composite risk scores across different neighborhoods in SSF and San Bruno.")

    # Load dataset for map visualization

    # Visualize the data with map (If you could make it a heatmap, that would be great)
    # NOTE: I added a library (`st_folium`) to visualize the map you created with Folium. make sure to install it
    # with `pip install streamlit-folium`

    # Insights & Interpretation
    # --- Mack ---
    st.title("Insights & Interpretation")

    st.info("""
    - [INSERT INSIGHT 1]
    - [INSERT INSIGHT 2]
    - [INSERT INSIGHT 3]
    """)

with tab2:
    # Title and Description
    st.title("Additional Information")
    st.write("This section provides additional information and analysis that curated while developing the dashboard.")

    # --- Isaac ---
    # Load datasets for additional information
    # NOTE: You can download the datasets you used for your analysis and load them here via pandas. Then, you can use
    # plotly to visualize the data.

    # Insights & Interpretation
    # --- Isaac ---
    # NOTE: You can add insights and interpretations in the function below.
    st.info("""
    - [INSERT INSIGHT 1]
    - [INSERT INSIGHT 2]
    - [INSERT INSIGHT 3]
    """)

# --- Footer ---
st.markdown("---")
st.caption("Rise South City · 2025")