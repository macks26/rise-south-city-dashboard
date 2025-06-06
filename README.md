# Rise South City Community Dashboard

This repository contains the code and data for the **Rise South City Community Dashboard**, a Streamlit web application that visualizes air pollution and health risk in South San Francisco and San Bruno.

---

## Features

- **Interactive Map**  
  View composite risk scores by census tract, combining air quality and health risk.

- **Sensor Locations**  
  See air quality monitor locations with a predictability index.

- **Address Search**  
  Enter an address to see local risk and predictability estimates.

- **Customizable Risk Balance**  
  Adjust the weighting of air quality vs. health risk to update the map.

- **Additional Context**  
  Explore figures and background information about environmental and health analysis.

---

## Live Demo

Explore the dashboard here: [https://rise-south-city-dashboard.streamlit.app/](https://rise-south-city-dashboard.streamlit.app/)

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
- **[Branca](https://python-visualization.github.io/branca/)** – Color maps for Folium  
- **[Geopy](https://geopy.readthedocs.io/)** – Geocoding and spatial distance analysis  
- **[OpenPyXL](https://openpyxl.readthedocs.io/)** – Excel file parsing
- etc.

## Repository Structure

```
.
├── code/                     # Scripts and notebooks for data processing and dashboard logic
│   ├── air_quality/          # Air quality analysis
│   ├── health/               # Health index calculation
│   ├── predictability/       # Predictability scoring
│   ├── preprocessing/        # Data cleaning and merging
│   ├── additional/           # Scripts for supporting figures
│   ├── streamlit_app.py      # Main dashboard application
│   └── ...                   # Other code components
│
├── data/                     # All cleaned and raw datasets used in the project
│   ├── ...                   # CSVs, GeoJSONs, and metadata
│
├── figures/                  # Visual assets for the dashboard
│   └── ...
│
├── documentation/            # Project docs and methodology guides
│   └── ...
│
├── requirements.txt          # Python dependencies
├── .devcontainer/            # Optional VS Code setup
├── README.md                 # Project overview
└── ...                       # Miscellaneous files                      

``` 

---

## License

This project is for educational and community use.  

---

## Contact

For questions concerning deployment or any of the documentation or code provided, email macks26@stanford.edu, ikrement@stanford.edu, or enkhjin@stanford.edu.
