import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Simple Geospatial Map")

st.title("🌍 Geospatial Map Visualization with Plotly")

# Sample data: locations of a few cities
data = pd.DataFrame({
    'City': ['San Francisco', 'New York', 'Chicago', 'Austin', 'Seattle'],
    'Latitude': [37.7749, 40.7128, 41.8781, 30.2672, 47.6062],
    'Longitude': [-122.4194, -74.0060, -87.6298, -97.7431, -122.3321]
})

# Mapbox token (optional for custom styling)
# px.set_mapbox_access_token("your_mapbox_token_here")

# Create the plot
fig = px.scatter_mapbox(
    data,
    lat="Latitude",
    lon="Longitude",
    hover_name="City",
    zoom=3,
    height=600,
    width=900,
    color_discrete_sequence=["blue"]
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_traces(marker=dict(size=12))

st.plotly_chart(fig, use_container_width=True)