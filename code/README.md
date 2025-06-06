# Code Folder

This folder contains all scripts and notebooks used to process, analyze, and visualize data for the Rise South City Community Dashboard.

## Structure & Key Files

### air_quality/
- `calculate_sensor_weights.py` – Calculates weights to combine Clarity and PurpleAir PM2.5 data based on their reliability in measuring air pollution risk.
- `clarity_midproject.ipynb` – Exploratory data analysis of Clarity sensor readings for mid-project report.

### health/
- `data_analysis_geo.ipynb` – Spatial analysis of health indicators and health risk by geography.
- `health.ipynb` – Main notebook for exploring and modeling health-related risk data for computing health-risk score.
- `health_preproc.ipynb` – Notebook to clean and reshape health risk datasets.

### predictability/
- `predictability.ipynb` – Computes and visualizes the predictability and consistency of air monitors.
- `visualize_pred_midproject.py` – Visualization tool for predictability of air monitors for the mid-project report.

### preprocessing/
- `clean_air_data.ipynb` – Notebook for cleaning and aligning raw air data sources.
- `clean_api_purpleair.ipynb` – Preprocessing PurpleAir API data in notebook form.
- `clean_clarity.py` – Script for cleaning Clarity sensor data.
- `clean_purpleair.py` – Script for cleaning PurpleAir sensor data.
- `combine_air_quality_data.py` – Merges air quality sources into a single composite dataset.
- `purpleair_wrapper.py` – Helper functions to query and process PurpleAir API data.

### Root Files
- `streamlit_app.py` – Main script for launching the Streamlit dashboard.
- `visualize_air_traffic.py` – Visualizes aircraft traffic in the area for contextual analysis.

---

All files are organized by theme: air quality, health, predictability, and preprocessing. Final dashboard functionality is tied together in `streamlit_app.py`.