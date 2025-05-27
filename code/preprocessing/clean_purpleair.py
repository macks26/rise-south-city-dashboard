"""
PurpleAir Data Integration and AQI Processing

This script merges and processes PM2.5 data from multiple PurpleAir sources for comprehensive air quality analysis.

It performs the following steps:
- Loads hourly, daily, and API-based sensor data.
- Cleans and standardizes timestamps, locations, and pollutant readings.
- Calculates 24-hour averages and corresponding AQI values.
- Merges and combines data from different formats and sources.
- Outputs a unified, time-sorted dataset for analysis or visualization.

The final result is a cleaned CSV file with PM2.5, AQI, and environmental conditions per sensor.
"""

import pandas as pd

# Load hourly, daily, and PurpleAir API data 
hourly = pd.read_csv("purpleair_hourly_data.csv")
daily = pd.read_csv("purpleair_daily_data.csv")
additional = pd.read_csv("purpleair_additional_data.csv")

# Process hourly data
hourly = hourly.rename(columns={
    'Datetime': 'time',
    'Site_Name': 'location_name',
    'Site_ID': 'location_id',
    'Latitude': 'latitude',
    'Longitude': 'longitude',
    'PM2.5_EPA': 'pm2_5_1h_mean',
    'Elevation': 'elevation',
    'Temp': 'temp',
    'RH': 'rh'
})
hourly['time'] = pd.to_datetime(hourly['time'])
hourly['date_only'] = hourly['time'].dt.date  

# Process daily data
daily = daily.rename(columns={
    'Datetime': 'daily_time',
    'Site_Name': 'location_name',
    'Site_ID': 'location_id',
    'PM2.5_EPA': 'pm2_5_24h_mean'
})
daily['daily_time'] = pd.to_datetime(daily['daily_time'])
daily['date_only'] = daily['daily_time'].dt.date
daily = daily[['location_id', 'date_only', 'pm2_5_24h_mean']]

# Merge data
merged = pd.merge(hourly, daily, on=['location_id', 'date_only'], how='left')

# Clamp negative PM2.5 values to zero
merged['pm2_5_1h_mean'] = merged['pm2_5_1h_mean'].clip(lower=0)
merged['pm2_5_24h_mean'] = merged['pm2_5_24h_mean'].clip(lower=0)

# Column arrangement
merged = merged[['time', 'location_name', 'location_id', 'latitude', 'longitude',
                 'pm2_5_1h_mean', 'pm2_5_24h_mean', 'elevation', 'temp', 'rh']]

# AQI calculation
def calculate_pm2_5_aqi(C_p):
    if pd.isna(C_p):
        return None

    C_p = float(str(C_p)[:str(C_p).find('.')+2]) if '.' in str(C_p) else float(C_p)

    breakpoints = [
        (0.0,   9.0,   0,   50),
        (9.1,   35.4,  51,  100),
        (35.5,  55.4,  101, 150),
        (55.5,  125.4, 151, 200),
        (125.5, 225.4, 201, 300),
        (225.5, 500.4, 301, 500)
    ]

    for BP_Lo, BP_Hi, I_Lo, I_Hi in breakpoints:
        if BP_Lo <= C_p <= BP_Hi:
            I_p = ((I_Hi - I_Lo) / (BP_Hi - BP_Lo)) * (C_p - BP_Lo) + I_Lo
            return round(I_p)

    return None

# Apply AQI calculations
merged['pm2_5_1h_mean_aqi'] = merged['pm2_5_1h_mean'].apply(calculate_pm2_5_aqi)
merged['pm2_5_24h_mean_aqi'] = merged['pm2_5_24h_mean'].apply(calculate_pm2_5_aqi)

# Sort
merged = merged.sort_values('time')

# Process PurpleAir API data
additional = additional.rename(columns={
    'time_stamp': 'time',
    'sensor_name': 'location_name',
    'sensor_index': 'location_id',
    'pm2.5_atm': 'pm2_5_1h_mean',
    'temperature': 'temp',
    'humidity': 'rh'
})
additional['time'] = pd.to_datetime(additional['time'], utc=True)
additional['time'] = additional['time'].dt.tz_convert('US/Pacific').dt.tz_localize(None)

# Clamp hourly PM2.5
additional['pm2_5_1h_mean'] = additional['pm2_5_1h_mean'].clip(lower=0)

# Add date column for grouping
additional['date_only'] = additional['time'].dt.date

# Calculate 24h average per sensor per day
daily_avg = (
    additional.groupby(['location_id', 'date_only'])['pm2_5_1h_mean']
    .mean()
    .reset_index()
    .rename(columns={'pm2_5_1h_mean': 'pm2_5_24h_mean'})
)

# Clamp daily average
daily_avg['pm2_5_24h_mean'] = daily_avg['pm2_5_24h_mean'].clip(lower=0)

# Merge back into original hourly-level data
additional = pd.merge(additional, daily_avg, on=['location_id', 'date_only'], how='left')

# AQI Calculations
additional['pm2_5_1h_mean_aqi'] = additional['pm2_5_1h_mean'].apply(calculate_pm2_5_aqi)
additional['pm2_5_24h_mean_aqi'] = additional['pm2_5_24h_mean'].apply(calculate_pm2_5_aqi)

# Column arrangement
additional = additional[['time', 'location_name', 'location_id', 'latitude', 'longitude',
                         'pm2_5_1h_mean', 'pm2_5_1h_mean_aqi',
                         'pm2_5_24h_mean', 'pm2_5_24h_mean_aqi',
                         'temp', 'rh', 'pressure']]

# Sort
additional = additional.sort_values('time')

# Combine both datasets
final = pd.concat([merged, additional], ignore_index=True)
final = final.sort_values('time')

# Reorder columns
final = final[['time', 'location_name', 'location_id', 'latitude', 'longitude',
               'pm2_5_1h_mean', 'pm2_5_1h_mean_aqi',
               'pm2_5_24h_mean', 'pm2_5_24h_mean_aqi',
               'temp', 'rh', 'elevation', 'pressure']]

# Save final result
final.to_csv("clean_purpleair.csv", index=False)