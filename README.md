# Rise South City Community Dashboard

This repository contains the code and data for the **Rise South City Community Dashboard**, a Streamlit web application that visualizes air pollution and health risk in South San Francisco and San Bruno.

---

## Features

- **Interactive Map:**  
  View composite risk scores by census tract, combining air quality and health risk.
- **Sensor Locations:**  
  See air quality monitor locations with a predictability index.
- **Address Search:**  
  Enter an address to see local risk and predictability estimates.
- **Customizable Risk Balance:**  
  Adjust the weighting of air quality vs. health risk to update the map.
- **Additional Context:**  
  Explore figures and background information about environmental and health analysis.

---

## Live Demo

Explore the dashboard here:  
🌐 [https://rise-south-city-dashboard.streamlit.app/](https://rise-south-city-dashboard.streamlit.app/)

---

## Getting Started

Follow these steps to set up and run the dashboard locally:

### Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/macks26/rise-south-city-dashboard.git
   cd rise-south-city-dashboard
   ```

2. **Run Streamlit Application Locally**
   ```bash
   run streamlit code/streamlit_app.py
   ```

---

## Technologies Used

- **[Python](https://www.python.org/)** – General-purpose programming
- **[Streamlit](https://streamlit.io/)** – Interactive web dashboard framework
- **[Pandas](https://pandas.pydata.org/)** – Data manipulation and cleaning
- **[GeoPandas](https://geopandas.org/)** – Geospatial analysis and shapefiles
- **[scikit-learn](https://scikit-learn.org/)** – Machine Learning and predictability modeling
- **[Folium](https://python-visualization.github.io/folium/)** – Leaflet.js-based map visualizations
- etc.

## Repository Structure

```
.
├── code/
│   ├── air_quality/                     # Directory containing scripts for air quality analysis
│   ├── health/                          # Directory containing scripts for health analysis
│   ├── preprocessing/                   # Directory containing scripts for preprocessing data for analysis
│   ├── predictability/                  # Directory containing scripts for predictability and consistency of monitors 
│   ├── streamlit_app.py                 # Main Streamlit dashboard app
│   └── ...                              # Additional scripts and notebooks
├── data/
│   ├── clean_clarity.csv                # Cleaned Clarity sensor data
│   ├── clean_api_purpleair.csv          # Cleaned PurpleAir sensor data
│   ├── health_risk_index.csv            # Health risk index data
│   ├── census.geojson                   # Census tract boundaries
│   ├── tracts_with_combined_aqi.geojson # Tracts with AQI and health data
│   └── ...                              # Other data files
├── figures/
│   └── ...                              # Images and figures for the dashboard organized into directories
├── requirements.txt                     # Python dependencies for streamlit app
├── .devcontainer/
│   └── devcontainer.json                # VS Code Dev Container config (optional)
├── documentation/                       # Documentation/Guides for Dashboard and Code
│   ├── dashboard.pdf                    # Documentation for Interactive Dashboard
│   ├── project.pdf                      # Documentation for Project Methodology
├── README.md                            # This file
└── ...                                  # Additional files for loading data and keeping drive clean                        

``` 

---

## License

This project is for educational and community use.  
See [LICENSE](LICENSE) for details.

---

## Contact

For questions concerning deployment or any of the documentation/code provided, email macks26@stanford.edu, ikrement@stanford.edu, or enkhjin@stanford.edu.
