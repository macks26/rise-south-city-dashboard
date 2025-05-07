import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# --- Page Config ---
st.set_page_config(page_title="Rise South City Community Dashboard", layout="wide")

# --- Tabs ---
tab1, tab2 = st.tabs(["Risk Analysis", "Additional Information"])

# --- Risk Analysis Tab ---
with tab1:
    st.title("Risk Analysis")
    st.write("This dashboard provides insights into air pollution risk in South San Francisco and San Bruno.")

    # Slider (no functionality yet!)
    st.subheader("Composite Risk Score Weights")
    # air_weight = st.slider("Adjust air quality risk weight (%)", 0, 100, 50) # Default is at 50%
    # st.write(f"Air Quality: {air_weight}%, Health Risk: {100 - air_weight}%")

    # Short explanation for users
    st.markdown("""
    Use the slider below to choose how much weight to give to air quality risk versus health risk 
    when calculating the overall neighborhood risk score. Slide right for more air quality emphasis, 
    left for more health emphasis.
    """)

    # Preset buttons (makes it easier for non-tech users)
    preset = st.radio(
        "Quick presets:",
        ["50% Air / 50% Health", "70% Air / 30% Health", "30% Air / 70% Health", "Custom"],
        index=0
    )

    # Set slider value based on preset or allow custom
    if preset == "50% Air / 50% Health":
        air_weight = 50
    elif preset == "70% Air / 30% Health":
        air_weight = 70
    elif preset == "30% Air / 70% Health":
        air_weight = 30
    else:
        air_weight = st.slider(
            "Adjust air quality risk weight (%)", 0, 100, 50, 
            help="Slide to adjust how much weight to give to air quality versus health risk."
        )

    health_weight = 100 - air_weight

    # Display selected weights with icons
    st.write(f"🌫️ **Air Quality Weight:** {air_weight}%")
    st.write(f"❤️ **Health Risk Weight:** {health_weight}%")

    # Map (to be updated later to a Composite Risk Score map!)
    st.subheader("Overall PM2.5 Exposure by Census Tract")
    st.write(
        "This map shows the combined long-term average PM2.5 AQI for each census tract, using data from 14 Clarity sensors and 27 PurpleAir sensors collected between March 30, 2024 and March 31, 2025."
    )

    # Load precomputed GeoJSON with AQRI data
    geojson_path = "../data/tracts_with_combined_aqi.geojson"

    # Load the GeoDataFrame
    tracts_with_data = gpd.read_file(geojson_path)

    # Set map center (based on actual data)
    center = tracts_with_data.geometry.centroid.unary_union.centroid
    map_center = [center.y, center.x]

    # Search bar
    st.subheader("Search by Address")
    search_query = st.text_input("Enter a street address (e.g., 123 Main St):")
    marker_coords = None
    zoom_level = 12

    if search_query:
        geolocator = Nominatim(user_agent="rise-south-city")
        location = (geolocator.geocode(f"{search_query}, South San Francisco, CA") or
                    geolocator.geocode(f"{search_query}, San Bruno, CA"))
        if location:
            marker_coords = [location.latitude, location.longitude]
            map_center = marker_coords
            zoom_level = 14
        else:
            st.warning("Address not found. Please try again.")

    # Folium map
    m = folium.Map(location=map_center, zoom_start=zoom_level, tiles="cartodbpositron")

    if tracts_with_data is not None and not tracts_with_data.empty:
        # Choropleth layer
        folium.Choropleth(
            geo_data=tracts_with_data,
            data=tracts_with_data,
            columns=["geoid", "combined_aqi"],
            key_on="feature.properties.geoid",
            fill_color="YlOrRd",
            fill_opacity=0.8,
            line_opacity=0.5
        ).add_to(m)

        # Tooltip layer
        folium.GeoJson(
            tracts_with_data,
            tooltip=folium.GeoJsonTooltip(
                fields=["geoid", "combined_aqi"],
                aliases=["Census Tract", "AQI"],
                localize=True,
                sticky=True
            )
        ).add_to(m)

    # Add Clarity monitor locations (blue markers)
    # for _, row in clarity_locations.iterrows():
    #     folium.CircleMarker(
    #         location=[row['latitude'], row['longitude']],
    #         radius=5,
    #         color="blue",
    #         fill=True,
    #         fill_color="blue",
    #         fill_opacity=0.7,
    #         tooltip="Clarity Monitor"
    #     ).add_to(m)
    #
    # Add PurpleAir monitor locations (purple markers)
    # for _, row in purpleair_locations.iterrows():
    #     folium.CircleMarker(
    #         location=[row['latitude'], row['longitude']],
    #         radius=5,
    #         color="purple",
    #         fill=True,
    #         fill_color="purple",
    #         fill_opacity=0.7,
    #         tooltip="PurpleAir Monitor"
    #     ).add_to(m)

    if marker_coords:
        folium.Marker(
            location=marker_coords,
            tooltip=search_query,
            icon=folium.Icon(color="red", icon="map-pin", prefix="fa")
        ).add_to(m)

    st_folium(m, use_container_width=True, height=700)

    # Insights & Interpretation
    st.title("Insights & Interpretation")

    st.info("""
    - This map shows combined PM2.5 Air Quality Index (AQI) scores by census tract in South San Francisco and San Bruno.
    - Census tracts are shaded from light to dark to represent increasing levels of long-term PM2.5 exposure.
    - The AQI for each census tract is based on measurements from two types of air monitors: Clarity and PurpleAir.
    - Each monitor reports daily PM2.5 concentrations, which we converted to AQI scores using EPA standards. For each census tract, we computed the median AQI from all available Clarity and PurpleAir data within the period from March 30, 2024, to March 31, 2025.
    - We then combined the Clarity and PurpleAir AQI scores using fixed weights (~76% Clarity and ~24% PurpleAir) to reflect the higher accuracy of Clarity monitors. If only one source had data for a tract, that data was used as-is.
    - The result is a weighted, median-based AQI score for each tract, helping identify areas with higher long-term air pollution exposure.
    """)

# --- Additional Information Tab ---
with tab2:
    st.title("Additional Information")
    st.write("This section provides additional figures and context for environmental and health analysis.")

    st.image('../figures/air_traffic.png')
    st.info('PM2.5 and Airport Traffic Timeline: This visualization displays monthly passenger traffic at San Francisco International Airport (bottom, January 2018 to December 2024). The sharp drop in air travel during the early months of the COVID-19 pandemic (2020) aligned with a noticeable decline in PM2.5 levels, suggesting that reduced airport operations may have improved local air quality. As air traffic rebounded in 2021 and beyond, PM2.5 concentrations also rose, pointing to a potential connection between flight activity and pollution levels. However, a late-2020 spike in PM2.5 was likely driven by wildfires, underscoring that airport emissions are just one piece of a larger puzzle. This natural experiment — where travel volume changed drastically while other factors held steady — offers a rare opportunity to isolate the airport’s contribution to regional air pollution. For communities near SFO, who already face multiple environmental and socioeconomic stressors, understanding this relationship is vital. These insights can inform targeted air quality interventions, regulatory strategies, and long-term planning to reduce the cumulative burden of pollution.')
    
    st.image(['../figures/clarity_predictability_risk_map.png', '../figures/clarity_predictability_risk_map.png'])
    st.info("Sensory Predictability over Percentage Uninsured: The two figures above show sensor locations (Purple and Clarity, respectively), along with a predictability index for each sensor, correlations between sensor readings, and ACS estimates of percentage uninsured for the census tracts in which the sensors were located. The 'predictability index' here is simply the maximum correlation that a sensor had with any others, intended to illustrate possible sensor redundancies. In areas where sensors are highly redundant — that is, another sensor's data can be used to accurately predict hourly readings — there may be less of a need for more nearby sensors. This is overlaid on the percentage of uninsured residents in each tract to highlight areas where people may be most vulnerable to the health effects of air pollution. Those who are uninsured cannot easily access the treatments that would help them recover from, or maintain resilience to, poor air quality. Overall, the purpose of this figure is to show where additional air sensors are most needed. If an area has low health insurance coverage and low sensor redundancy, it might benefit from the placement of new sensors so that community members can take steps to protect their health.")

# Footer
st.markdown("---")
st.caption("Rise South City · 2025")