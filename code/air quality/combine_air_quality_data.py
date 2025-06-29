"""
Census Tract-Level AQI Aggregation from Clarity and PurpleAir Data

This script calculates median air quality index (AQI) values for each census tract using PM2.5 data from Clarity and PurpleAir sensors.

It performs the following steps:
- Loads cleaned PM2.5 and census tract data.
- Filters sensor data to a defined date range.
- Assigns each sensor reading to its corresponding census tract.
- Computes median AQI per tract from each sensor network.
- Combines AQIs using inverse variance weights.
- Outputs both a GeoJSON and CSV with tract-level AQI estimates.

The result supports spatial analysis of air quality across South San Francisco and San Bruno.
"""

import pandas as pd
import geopandas as gpd
import numpy as np

# Time range for analysis
DATE_START = '2024-03-30'
DATE_END = '2025-03-31'

# Weights from calculate_sensor_weights.py
CLARITY_WEIGHT = 0.76
PURPLEAIR_WEIGHT = 0.24

# Load data
clarity = pd.read_csv("../data/clean_clarity.csv")
purpleair = pd.read_csv("../data/clean_api_purpleair.csv")
tracts = gpd.read_file("../data/census.geojson")

# Convert time columns to datetime
clarity['time'] = pd.to_datetime(clarity['time'])
purpleair['time'] = pd.to_datetime(purpleair['time'])

# Filter to desired date range
clarity = clarity[(clarity['time'] >= DATE_START) & (clarity['time'] <= DATE_END)]
purpleair = purpleair[(purpleair['time'] >= DATE_START) & (purpleair['time'] <= DATE_END)]

# Convert to GeoDataFrames
clarity_gdf = gpd.GeoDataFrame(
    clarity,
    geometry=gpd.points_from_xy(clarity.longitude, clarity.latitude),
    crs="EPSG:4326"
)
purpleair_gdf = gpd.GeoDataFrame(
    purpleair,
    geometry=gpd.points_from_xy(purpleair.longitude, purpleair.latitude),
    crs="EPSG:4326"
)

# Assign census tract to each sensor reading
clarity_joined = gpd.sjoin(clarity_gdf, tracts, how="left", predicate="within")
purpleair_joined = gpd.sjoin(purpleair_gdf, tracts, how="left", predicate="within")

# Compute median AQI per tract
clarity_tract_aqi = (
    clarity_joined.groupby("geoid")["pm2_5_24h_mean_aqi"]
    .median()
    .reset_index(name="clarity_aqi")
)
purpleair_tract_aqi = (
    purpleair_joined.groupby("geoid")["pm2_5_24h_mean_aqi"]
    .median()
    .reset_index(name="purpleair_aqi")
)

# Merge clarity + purpleair AQIs per tract
aqi_merged = pd.merge(clarity_tract_aqi, purpleair_tract_aqi, on="geoid", how="outer")

# Compute combined AQI
def combine_aqi(row):
    c_aqi = row['clarity_aqi']
    p_aqi = row['purpleair_aqi']
    if pd.notna(c_aqi) and pd.notna(p_aqi):
        return c_aqi * CLARITY_WEIGHT + p_aqi * PURPLEAIR_WEIGHT
    elif pd.notna(c_aqi):
        return c_aqi
    elif pd.notna(p_aqi):
        return p_aqi
    else:
        return np.nan

aqi_merged['combined_aqi'] = aqi_merged.apply(combine_aqi, axis=1)

# Merge back with census tract geometries
tracts_with_combined = tracts.merge(
    aqi_merged[['geoid', 'clarity_aqi', 'purpleair_aqi', 'combined_aqi']],
    on="geoid",
    how="left"
)

# Keep only tracts with data
tracts_with_combined = tracts_with_combined[
    tracts_with_combined[['clarity_aqi', 'purpleair_aqi', 'combined_aqi']].notnull().any(axis=1)
]

# Fill in AQI for tracts where there are no sensors
make_geoid = lambda t: "06081" + t
mean_aqi = lambda tracts: tracts_with_combined.loc[tracts_with_combined["geoid"].isin(list(map(make_geoid, tracts))), "combined_aqi"].mean()

fillin_df = gpd.GeoDataFrame({
    "geoid": ["06081604104", "06081604103"],
    "combined_aqi": [mean_aqi(["604200", "604102", "604000"]), mean_aqi(["604104", "603900", "604200"])],
    "geometry": [tracts.loc[tracts["geoid"] == make_geoid("604104"), "geometry"].values[0], tracts.loc[tracts["geoid"] == make_geoid("604103"), "geometry"].values[0]]
})
tracts_with_combined = pd.concat([tracts_with_combined, fillin_df])

# Save outputs
tracts_with_combined.to_file("../data/tracts_with_combined_aqi.geojson", driver="GeoJSON")
tracts_with_combined[['geoid', 'clarity_aqi', 'purpleair_aqi', 'combined_aqi']].to_csv(
    "../data/tracts_with_combined_aqi.csv", index=False
)