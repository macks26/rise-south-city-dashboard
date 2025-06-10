"""
Rise South City Community Dashboard

This Streamlit app visualizes air pollution and health risk in South San Francisco and San Bruno.

It provides:
- An interactive map showing composite risk scores by census tract, combining air quality and health risk.
- Locations of air quality monitors with a predictability index.
- Address search with local risk and predictability estimates.
- Additional figures and context about environmental and health analysis.

Users can adjust the weighting of air quality vs. health risk, search by address, and explore insights about local air quality and vulnerability.
"""

import pandas as pd  
import streamlit as st  
import geopandas as gpd 
import branca.colormap as cm  
import folium  
from streamlit_folium import st_folium   
from geopy.geocoders import Nominatim 
from geopy.distance import geodesic
import pickle

# Page Config
st.set_page_config(page_title="Rise South City Community Dashboard", layout="wide")

# Load predictability data for sensors
pred_df = pd.read_csv("data/combined_scores.csv")

# Tabs
tab1, tab2 = st.tabs(["Risk Analysis", "Additional Information"])

# Todo for future groups: Automate the translation process (+add more languages) using a package such as gettext (along with polib)
languages = ['English', 'Español']
language = languages[0]

translations = {
    'Español': {
        "Select Language": "Cambiar Idioma",
        "Neighborhood Risk Map": "Mapa de Riesgo Vecinal",
        "See how air quality and health risk vary across neighborhoods. Adjust the balance below to update the map.": "Ver como se varia la calidad del aire y riesgo de salud por vecinos. Ajusta el equilibrio debajo para actualizar la mapa.",
        "Adjust Map Risk Balance": "Ajustar el Equilibrio de Riesgo de la Mapa",
        "Use the options below to choose how much the map should focus on air quality or health factors.": "Usa las opciones debajo para elegir cuanto debe enfocar en calidad del aire o factores de salud la mapa.",
        "Pick a balance:": "Elige un equilibrio:",
        "Even (50% Air, 50% Health)": "Igualado (50% Aire, 50% Salud)",
        "More Air (70% Air, 30% Health)": "Más Aire (70% Aire, 30% Salud)",
        "More Health (30% Air, 70% Health)": "Más Salud (30% Aire, 70% Salud)",
        "Custom": "Personalizado",
        "Air Quality Weight (%)": "Ponderación de la calidad del aire",
        "Slide right for more air quality, left for more health.": "Desliza a la derecha para más ponderación a la calidad del aire, a la izquierda para más ponderación a la salud",
        "Air Quality": "Calidad del Aire",
        "Health": "Salud",
        "Search by Address": "Buscar por Dirección",
        "Enter a street address (e.g., 123 Main St):": "Poner un dirección (ej. 123 Main St):",
        "Geocoding error": "Error de geocodificación",
        "Address not found. Please try again.": "No se encuentra a tu dirección. Por favor intenta otra vez.",
        "Composite Risk Score": "Índice de Riesgo Compuesto",
        "Census Tract": "Tramo Censal",
        "Predictability Score": "Índice de Predictibilidad",
        "Consistency Score": "Índice de Consistencia",
        "Address": "Dirección",
        "Insights & Interpretation": "Conocimientos & Interpretación", """
    ### 🧪 Composite Risk Score

    This map displays a **composite air and health risk score** for each census tract in South San Francisco and San Bruno.  
    **Darker shading** indicates **higher overall risk** in a given tract.  

    The score combines two parts:  
    - An **air quality risk score**, calculated from daily PM2.5 concentrations reported by Clarity and PurpleAir monitors. These values are converted into **Air Quality Index (AQI)** scores using EPA standards.  
    - A **health risk score**, which integrates **health equity data** along with **general and respiratory health metrics** to identify communities more vulnerable to air pollution.  

    The final score is a **weighted combination** of the two, highlighting areas where both pollution levels and health vulnerabilities are high.
    """: """
    ### 🧪 Índice de Riesgo Compuesto

    Esta mapa se exhiba un índice compuesto de la calidad del aire y la salud por cada tramo censal en South San Francisco y San Bruno.  
    **Tono oscuro** se indica **riesgo mayor en general** en el tramo dado.  

    Este índice se mezcla dos partes:  
    - Un **índice de riesgo de la calidad del aire**, calculado por concentraciónes de PM2.5 diarias reportado por Clarity y PurpleAir monitores. Estes números se convierten al **Índice de Calidad del Aire (AQI)** con las normas de la EPA.  
    - Un **índice de riesgo a la salud**, que se incorpora **datos de justicia de salud** junto con **métricos de salud general y respiratorio** para identificar comunidades que son más vulnerables a la pollución del aire.  

    El número final es una **suma ponderada** de las dos, que destaca áreas donde las niveles de la pollución y vulnerabilidades de salud son elevados.
    """, """
    ### 📡 Monitor Predictability Index

    The map also shows the locations of **air quality monitors**, each marked with a **predictability index**.  
    This index reflects how **reliably a monitor's readings can be predicted** using historical data and nearby monitors.  

    It is calculated using a combination of:  
    - **Self-predictability** — how well a monitor's past data can forecast its future readings.  
    - **Cross-predictability** — how well nearby monitors can be used to predict a monitor's readings.  

    A **higher predictability index** suggests more stable or consistent readings, while **lower scores** may indicate irregular behavior or localized factors affecting air quality.
    """: """
    ### 📡 Índice de Predictibilidad de los Monitores

    La mapa también se muestra las ubicaciónes de las **monitores de calidad del aire**, cada marcado con un **índice de predictibildad**.  
    Este índice se refleja **qué tan bien podemos pronosticar las lecturas del monitor** usando datos históricos y monitores cercanos.  

    Se calcula usando una mezcla de:  
    - **Autopredictibilidad** — Qué tan bien le puede pronosticar a las lecturas futuros los datos históricos del monitor.  
    - **Predictibilidad Cruzada** — Que tan bien le puede pronosticar a las lecturas de un monitor los datos de los monitores cercanos.

    Un **índice de predictibilidad más alto** sugiere a más estabilidad y regularidad de las lecturas del monitor, mientras **índices más bajos** quizás indican funcionamiento irregular o factores locales que se afectan la calidad del aire.
    """,
        "Additional Information": "Información Adicional",
        "This section provides additional figures and context for environmental and health analysis.": "Esta sección se muestra figuras y contexto para analisís ambiental y de la salud.",
        "PM2.5 and Airport Traffic Timeline: This visualization displays monthly passenger traffic at San Francisco International Airport (bottom, January 2018 to December 2024). The sharp drop in air travel during the early months of the COVID-19 pandemic (2020) aligned with a noticeable decline in PM2.5 levels, suggesting that reduced airport operations may have improved local air quality. As air traffic rebounded in 2021 and beyond, PM2.5 concentrations also rose, pointing to a potential connection between flight activity and pollution levels. However, a late-2020 spike in PM2.5 was likely driven by wildfires, underscoring that airport emissions are just one piece of a larger puzzle. This natural experiment — where travel volume changed drastically while other factors held steady — offers a rare opportunity to isolate the airport’s contribution to regional air pollution. For communities near SFO, who already face multiple environmental and socioeconomic stressors, understanding this relationship is vital. These insights can inform targeted air quality interventions, regulatory strategies, and long-term planning to reduce the cumulative burden of pollution.": "",
        "Sensor Predictability over Percentage Uninsured: The two figures above show sensor locations (Purple and Clarity, respectively), along with a predictability index for each sensor, correlations between sensor readings, and ACS estimates of percentage uninsured for the census tracts in which the sensors were located. The 'predictability index' here is simply the maximum correlation that a sensor had with any others, intended to illustrate possible sensor redundancies. In areas where sensors are highly redundant — that is, another sensor's data can be used to accurately predict hourly readings — there may be less of a need for more nearby sensors. This is overlaid on the percentage of uninsured residents in each tract to highlight areas where people may be most vulnerable to the health effects of air pollution. Those who are uninsured cannot easily access the treatments that would help them recover from, or maintain resilience to, poor air quality. Overall, the purpose of this figure is to show where additional air sensors are most needed. If an area has low health insurance coverage and low sensor redundancy, it might benefit from the placement of new sensors so that community members can take steps to protect their health.": "Predictibilidad de los monitores encima de Porcentaje sin coberatura: Las figuras de arriba se muestran las ubaciónes de los monitores (Purple y Clarity respectivamente), junto con un índice de predictibilidad rudimentario por cada monitor, correlaciones entre de lecturas de los monitores, y las estimaciones ACS de la porcentaje sin coberatura por los tramos en que habían monitores. El 'índice de predictibilidad' aquí es la correlación máxima que tenía un monitor con todos otros."
    }
}

# Translation
def t(message):
    if language == languages[0]:
        return message
    else:
        return translations[language][message]

# Risk Analysis Tab
with tab1:
    # Language selection
    language = st.selectbox(
        label=t("Select Language"),
        options=["English", "Español"]
    )

    # Map Section
    st.title(t("Neighborhood Risk Map"))
    st.write(t("See how air quality and health risk vary across neighborhoods. Adjust the balance below to update the map."))
    
    # Composite Risk Score Weights
    st.subheader(t("Adjust Map Risk Balance"))

    st.markdown(
        t("Use the options below to choose how much the map should focus on air quality or health factors.")
    )

    opts = [t("Even (50% Air, 50% Health)"), t("More Air (70% Air, 30% Health)"), t("More Health (30% Air, 70% Health)"), t("Custom")]
    preset = st.radio(
        t("Pick a balance:"),
        opts,
        index=0
    )

    if preset == opts[1]:
        air_weight = 50
    elif preset == opts[2]:
        air_weight = 70
    elif preset == opts[3]:
        air_weight = 30
    else:
        air_weight = st.slider(
            t("Air Quality Weight (%)"), 0, 100, 50,
            help=t("Slide right for more air quality, left for more health.")
        )

    health_weight = 100 - air_weight

    st.write(f"**{t('Air Quality')}:** {air_weight}%   |   **{t('Health')}:** {health_weight}%")
    
    # Load and process data for map
    clarity = pd.read_csv("data/clean_clarity.csv")
    purpleair = pd.read_csv("data/clean_purpleair.csv")
    health_risk = pd.read_csv("data/health_risk_index.csv")
    tracts = gpd.read_file("data/census.geojson")
    geojson_path = "data/tracts_with_combined_aqi.geojson"
    tracts_with_data = gpd.read_file(geojson_path)

    # Merge health risk data into tracts GeoDataFrame
    health_risk["geoid"] = "06081" + (health_risk["tract"] * 100).astype(int).astype(str)
    tracts_with_data = tracts_with_data.merge(health_risk, on="geoid")

    # Normalize air quality and compute composite risk score
    tracts_with_data["air_norm"] = tracts_with_data["combined_aqi"] / tracts_with_data["combined_aqi"].max()
    tracts_with_data["health_norm"] = tracts_with_data["Health Risk Index"]  # Already 0-1

    air_frac = air_weight / 100
    health_frac = health_weight / 100

    tracts_with_data["risk_index"] = (
        air_frac * tracts_with_data["air_norm"] +
        health_frac * tracts_with_data["health_norm"]
    )

    # Drop any rows with missing data
    tracts_with_data = tracts_with_data.dropna(subset=["risk_index"])

    # Set map center based on tract centroids
    center = tracts_with_data.geometry.centroid.unary_union.centroid
    map_center = [center.y, center.x]

    # Address Search
    st.subheader(t("Search by Address"))
    search_query = st.text_input(t("Enter a street address (e.g., 123 Main St):"))
    marker_coords = None
    zoom_level = 12

    # Geocode address using Nominatim (cached for performance)
    @st.cache_data(show_spinner=False)
    def geocode_address(address):
        geolocator = Nominatim(user_agent="rise-south-city", timeout=5)
        try:
            return geolocator.geocode(address)
        except Exception as e:
            st.error(f"{t('Geocoding error')}: {e}")
            return None
        
    if search_query:
        # Try to geocode the address in both cities
        location = (geocode_address(f"{search_query}, South San Francisco, CA") or
                    geocode_address(f"{search_query}, San Bruno, CA"))
        if location:
            marker_coords = [location.latitude, location.longitude]
            map_center = marker_coords
            zoom_level = 14
        else:
            st.warning(t("Address not found. Please try again."))

    # Folium Map Creation 
    m = folium.Map(location=map_center, zoom_start=zoom_level, tiles="cartodbpositron")

    if tracts_with_data is not None and not tracts_with_data.empty:
        # Choropleth layer using continuous color scale
        risk_colormap = cm.linear.YlOrRd_09.scale(0, 1)
        risk_colormap.caption = t("Composite Risk Score")

        def style_function(feature):
            risk = feature["properties"]["risk_index"]
            return {
                "fillOpacity": 0.8,
                "weight": 0.5,
                "color": "black",
                "fillColor": risk_colormap(risk)
            }

        folium.GeoJson(
            tracts_with_data,
            name=t("Composite Risk Score"),
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=["geoid", "risk_index"],
                aliases=[f"{t('Census Tract')}:", f"{t('Composite Risk Score')}:"],
                localize=True,
                sticky=True
            )
        ).add_to(m)

        risk_colormap.add_to(m)

    # Load model for predictability
    with open("data/rf_predictability_model.pkl", "rb") as f:
        rf_model = pickle.load(f)

    # Separate Clarity and PurpleAir monitors
    clarity_locations = pred_df[~pred_df['location_id'].str.isnumeric()][['latitude', 'longitude', 'predictability', 'consistency']]
    purpleair_locations = pred_df[pred_df['location_id'].str.isnumeric()][['latitude', 'longitude', 'predictability', 'consistency']]

    # Create color scale for predictability index
    min_val = pred_df['predictability'].min()
    max_val = pred_df['predictability'].max()
    color_scale = cm.linear.PuBuGn_09.scale(min_val, max_val).to_step(n=10)
    color_scale.caption = t("Predictability Score")

    # Function to add monitor markers to map
    def add_monitors(df, label):
        for _, row in df.iterrows():
            predictability = round(row['predictability'], 0)
            consistency = round(row['consistency'], 0) if not pd.isnull(row['consistency']) else "N/A"
            color = color_scale(predictability)
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                tooltip=f"{label} Monitor<br>{t('Predictability Score')}: {int(predictability)}%<br>{t('Consistency Score')}: {int(consistency)}%"
            ).add_to(m)

    add_monitors(clarity_locations, "Clarity")
    add_monitors(purpleair_locations, "PurpleAir")

    # Add legend to map
    color_scale.add_to(m)

    # Add Red Pin for Search Result (if used)
    if marker_coords:
        # Find 5 closest monitors
        all_monitors = pred_df[['latitude', 'longitude', 'predictability', 'consistency']].copy()
        all_monitors['distance'] = all_monitors.apply(
            lambda row: geodesic((row['latitude'], row['longitude']), marker_coords).miles, axis=1
        )
        closest_monitors = all_monitors.nsmallest(5, 'distance')

        if not closest_monitors.empty:
            # Build feature row for model
            feature_row = {}
            for i, n_row in enumerate(closest_monitors.itertuples(), start=1):
                feature_row[f'neighbor_{i}_distance'] = n_row.distance
                feature_row[f'neighbor_{i}_predictability'] = n_row.predictability
                feature_row[f'neighbor_{i}_consistency'] = n_row.consistency

            feature_df = pd.DataFrame([feature_row])

            # Predict using model
            predicted_index = rf_model.predict(feature_df)[0]
            predicted_index = round(predicted_index, 0)

            folium.Marker(
                location=marker_coords,
                tooltip=f"<b>{t('Address')}:</b> {search_query}<br><b>{t('Predicted Predictability')}:</b> {int(predicted_index)}%",
                icon=folium.Icon(color="red", icon="map-pin", prefix="fa")
            ).add_to(m)

    # Render Map in Streamlit 
    st_folium(m, use_container_width=True, height=700)

    # Insights & Interpretation 
    st.title(t("Insights & Interpretation"))

    st.info(t("""
    ### 🧪 Composite Risk Score

    This map displays a **composite air and health risk score** for each census tract in South San Francisco and San Bruno.  
    **Darker shading** indicates **higher overall risk** in a given tract.  

    The score combines two parts:  
    - An **air quality risk score**, calculated from daily PM2.5 concentrations reported by Clarity and PurpleAir monitors. These values are converted into **Air Quality Index (AQI)** scores using EPA standards.  
    - A **health risk score**, which integrates **health equity data** along with **general and respiratory health metrics** to identify communities more vulnerable to air pollution.  

    The final score is a **weighted combination** of the two, highlighting areas where both pollution levels and health vulnerabilities are high.
    """))

    st.info(t("""
    ### 📡 Monitor Predictability Index

    The map also shows the locations of **air quality monitors**, each marked with a **predictability index**.  
    This index reflects how **reliably a monitor's readings can be predicted** using historical data and nearby monitors.  

    It is calculated using a combination of:  
    - **Self-predictability** — how well a monitor's past data can forecast its future readings.  
    - **Cross-predictability** — how well nearby monitors can be used to predict a monitor's readings.  

    A **higher predictability index** suggests more stable or consistent readings, while **lower scores** may indicate irregular behavior or localized factors affecting air quality.
    """))

# Additional Information Tab
with tab2:
    st.title(t("Additional Information"))
    st.write(t("This section provides additional figures and context for environmental and health analysis."))

    # Display air traffic and PM2.5 timeline figure
    st.image('figures/air_traffic.png')
    st.info(t('PM2.5 and Airport Traffic Timeline: This visualization displays monthly passenger traffic at San Francisco International Airport (bottom, January 2018 to December 2024). The sharp drop in air travel during the early months of the COVID-19 pandemic (2020) aligned with a noticeable decline in PM2.5 levels, suggesting that reduced airport operations may have improved local air quality. As air traffic rebounded in 2021 and beyond, PM2.5 concentrations also rose, pointing to a potential connection between flight activity and pollution levels. However, a late-2020 spike in PM2.5 was likely driven by wildfires, underscoring that airport emissions are just one piece of a larger puzzle. This natural experiment — where travel volume changed drastically while other factors held steady — offers a rare opportunity to isolate the airport’s contribution to regional air pollution. For communities near SFO, who already face multiple environmental and socioeconomic stressors, understanding this relationship is vital. These insights can inform targeted air quality interventions, regulatory strategies, and long-term planning to reduce the cumulative burden of pollution.'))
    
    # Display sensor predictability and uninsured percentage figures
    st.image(['figures/predictability/clarity_predictability.png', 'figures/predictability/clarity_corrs.png'])
    st.info(t("Sensor Predictability over Percentage Uninsured: The two figures above show sensor locations (Purple and Clarity, respectively), along with a predictability index for each sensor, correlations between sensor readings, and ACS estimates of percentage uninsured for the census tracts in which the sensors were located. The 'predictability index' here is simply the maximum correlation that a sensor had with any others, intended to illustrate possible sensor redundancies. In areas where sensors are highly redundant — that is, another sensor's data can be used to accurately predict hourly readings — there may be less of a need for more nearby sensors. This is overlaid on the percentage of uninsured residents in each tract to highlight areas where people may be most vulnerable to the health effects of air pollution. Those who are uninsured cannot easily access the treatments that would help them recover from, or maintain resilience to, poor air quality. Overall, the purpose of this figure is to show where additional air sensors are most needed. If an area has low health insurance coverage and low sensor redundancy, it might benefit from the placement of new sensors so that community members can take steps to protect their health."))

# --- Footer ---
st.markdown("---")
st.caption("Rise South City · 2025")