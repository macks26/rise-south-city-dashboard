import folium
import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
from folium.plugins import Geocoder
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from shared import purple_predictability_risk_map, clarity_predictability_risk_map

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
    st.write("This dashboard provides insights into the risk associated with air pollution in South San Francisco and San Bruno.")
    
    # --- Enkhjin ---
    # Weight Slider
    st.subheader("Composite Risk Score Weights")
    st.write("Adjust the weights to see how they affect the overall risk score.")
    air_weight = st.slider("", 0, 100, 50) # Default is at 50 as of now
    health_weight = 100 - air_weight
    st.write(f"Air Quality: {air_weight}%, Health Risk: {health_weight}%")

    # Search Bar
    # --- Mack ---
    # search_query = st.text_input("Curious about a specific location? Enter a street address (eg. 123 Main St):")
    
    # Geocoding
    # NOTE: You would typically use a geocoding API here to convert the address to coordinates.
    # Use the results to later capture information about a specific census tract.

    # --- Enkhjin ---
    # Map (NOTE: to be changed later to a Composite Risk Score map)
    st.subheader("Overall PM2.5 Exposure by Census Tract")
    st.write("This map shows long-term average PM2.5 AQI by census tract using data from 49 sensors.")

    # Visualize the data with map (If you could make it a heatmap, that would be great)
    # NOTE: I added a library (`st_folium`) to visualize the map you created with Folium

    # Load and process data
    clarity = pd.read_csv("../data/clean_clarity.csv")
    purpleair = pd.read_csv("../data/clean_purpleair.csv")
    tracts = gpd.read_file("../data/census.geojson")

    # Combine both sensor datasets into one DataFrame
    combined = pd.concat([clarity, purpleair], ignore_index=True)

    # Convert combined DataFrame into a GeoDataFrame
    combined_gdf = gpd.GeoDataFrame(
        combined,
        geometry=gpd.points_from_xy(combined.longitude, combined.latitude),
        crs="EPSG:4326"
    )

    # Assign each sensor reading to the census tract it falls within
    joined = gpd.sjoin(combined_gdf, tracts, how="left", predicate="within")
    joined["date"] = pd.to_datetime(joined["time"]).dt.date

    # Compute the daily average AQI per tract
    tract_daily_aqi = (
        joined.groupby(["geoid", "date"])["pm2_5_24h_mean_aqi"]
        .mean()
        .reset_index(name="daily_avg_aqi")
    )

    # Compute the overall average AQI per tract
    tract_aqi = (
        tract_daily_aqi.groupby("geoid")["daily_avg_aqi"]
        .mean()
        .reset_index(name="overall_tract_aqi")
    )

    tracts_with_aqi = tracts.merge(tract_aqi, on="geoid")

    # Base map center
    center = tracts_with_aqi.geometry.centroid.unary_union.centroid
    map_center = [center.y, center.x]

    # Search bar and geocoding
    st.subheader("Search by Address")
    search_query = st.text_input("Curious about a specific location? Enter a street address (eg. 123 Main St):")
    marker_coords = None

    # If a user types an address, geocode it using Nominatim
    if search_query:
        geolocator = Nominatim(user_agent="rise-south-city")
        location = geolocator.geocode(search_query)
        if location:
            marker_coords = [location.latitude, location.longitude]
            map_center = marker_coords
        else:
            st.warning("Address not found. Please try again.")

    # Build the folium map
    m = folium.Map(location=map_center, zoom_start=12, tiles=None)
    folium.TileLayer("OpenStreetMap", opacity=0.4).add_to(m)

    # Color census tracts based on their average AQI
    folium.Choropleth(
        geo_data=tracts_with_aqi,
        data=tracts_with_aqi,
        columns=["geoid", "overall_tract_aqi"],
        key_on="feature.properties.geoid",
        fill_color="YlOrRd",
        fill_opacity=0.8,
        line_opacity=0.5,
        legend_name="Mean 24h PM2.5 AQI by Census Tract (Clarity + PurpleAir)"
    ).add_to(m)

    # Add tooltip when you hover over a census tract
    folium.GeoJson(
        tracts_with_aqi,
        tooltip=folium.GeoJsonTooltip(
            fields=["geoid", "overall_tract_aqi"],
            aliases=["Census Tract", "AQI"],
            localize=True,
            sticky=True
        )
    ).add_to(m)

    # Add a marker for the searched address if any
    if marker_coords:
        folium.Marker(
            location=marker_coords,
            tooltip="Searched Location",
            icon=folium.Icon(color="blue", icon="search", prefix="fa")
        ).add_to(m)

    # Full width map
    st_folium(m, use_container_width=True, height=700)

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

    #st.pyplot(purple_predictability_risk_map)

# --- Footer ---
st.markdown("---")
st.caption("Rise South City · 2025")