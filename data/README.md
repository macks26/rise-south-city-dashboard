# Data Folder

This folder contains all data sources used for our analysis and development of the Rise South City Community Dashboard.

## Sources

### **Air Quality Data**
- Clarity sensor data (`clean_clarity.csv`, `risesouthcity_april_hourly.csv`, etc.)
- PurpleAir API data (`clean_api_purpleair.csv`, `clean_purpleair.csv`)
- ASDS datasets for South San Francisco (`ASDS 2018–2023`, `Daily/Hourly ASDS`)

### **Health Data**
- Health risk indicators (`health_risk_index.csv`)
- All indicators (`all_indicators.csv`)

### **Geospatial Data**
- Census tracts (`census.geojson`)
- Combined AQI and health scores by tract (`tracts_with_combined_aqi.geojson`, `.csv`)

### **External Sources Referenced**
- California Office of Environmental Health Hazard Assessment (CalEnviroScreen)
- San Mateo County Health
- PurpleAir API

---

## Notes

- All datasets have been cleaned and preprocessed before use in the dashboard.
- For detailed information on data cleaning, transformations, and merging logic, refer to the scripts in the `code/` directory. 