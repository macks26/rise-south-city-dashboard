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

# Save outputs
tracts_with_combined.to_file("../data/tracts_with_combined_aqi.geojson", driver="GeoJSON")
tracts_with_combined[['geoid', 'clarity_aqi', 'purpleair_aqi', 'combined_aqi']].to_csv(
    "../data/tracts_with_combined_aqi.csv", index=False
)