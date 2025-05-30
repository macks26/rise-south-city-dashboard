# Code Folder

This folder contains all scripts and notebooks used to process, analyze, and visualize data for the Rise South City Community Dashboard.

## Folder Structure & Key Files

### `air_quality/`
- `calculate_sensor_weights.py` – Computes source weights for combining Clarity and PurpleAir PM2.5 data based on co-located sensor comparisons.
- `combine_air_quality_data.py` – Merges daily PM2.5 data by census tract using spatial joins and time filtering.

### `health/`
- `health.ipynb` – Calculates the Health Risk Index (HRI) using indicators of health equity and respiratory vulnerability.

### `predictability/`
- `predictability.ipynb` – Computes consistency and predictability scores for air quality monitors using Random Forest models and neighbor-based inference.

### `preprocessing/`
- `clean_api_purpleair.ipynb` – Cleans PurpleAir API data and transforms it into daily averages.
- `clean_clarity.py` – Cleans Clarity sensor data and handles invalid values.
- `clean_purpleair.py` – Processes historical PurpleAir datasets.
- `combine_air_quality_data.py` – Aggregates and merges air quality data by tract and time period.
- `health_preproc.ipynb` – Cleans and standardizes raw health indicators before risk scoring.
- `purpleair_wrapper.py` – Automates data retrieval from the PurpleAir API.

### `additional/`
- `uninsured.ipynb` – Analyzes the relationship between air quality monitor placement and the percentage of uninsured residents.
- `uninsured_clarity.ipynb` – Focused analysis of Clarity sensors and health vulnerability based on insurance access.
- `visualize_air_traffic.py` – Visualizes trends in PM2.5 in relation to airport passenger traffic for the Additional Information tab in the dashboard.

### Root Files
- `streamlit_app.py` – Main Streamlit app for the dashboard. Located at the root level.

---

## Notes

- Files are grouped by functionality: air quality processing, health scoring, predictability modeling, visualization, and dashboard integration.
- Notebooks and scripts in `additional/` are used to generate visualizations for the dashboard’s Additional Information tab.
- See the project documentation for full methodology and the suggested execution order.