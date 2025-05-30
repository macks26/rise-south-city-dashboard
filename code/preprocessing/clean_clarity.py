"""
Clarity Data Processing for PM2.5 and AQI Analysis

This script prepares hourly PM2.5 data from Clarity monitors for use in air quality analysis.

It performs the following steps:
- Loads raw hourly data and converts timestamps to Pacific time.
- Selects and renames relevant columns for clarity.
- Computes daily 24-hour PM2.5 averages per sensor.
- Calculates AQI based on daily PM2.5 concentrations.
- Cleans and organizes the final dataset.

The result is a daily air quality dataset exported as a clean CSV.
"""

import pandas as pd

# Load Clarity data
clarity = pd.read_csv("data/risesouthcity_april_hourly.csv", parse_dates=["startOfPeriod"])

# Convert to Pacific timezone and strip tz info
clarity["startOfPeriod"] = pd.to_datetime(clarity["startOfPeriod"], utc=True)
clarity["startOfPeriod"] = clarity["startOfPeriod"].dt.tz_convert("US/Pacific").dt.tz_localize(None)

# Rename and keep needed columns
clarity = clarity.rename(columns={
    "startOfPeriod": "time",
    "Name": "location_name",
    "datasourceId": "location_id",
    "locationLatitude": "latitude",
    "locationLongitude": "longitude",
    "pm2_5ConcMass1HourMean.value": "pm2_5_1h_mean"
})
clarity = clarity[["time", "location_name", "location_id", "latitude", "longitude", "pm2_5_1h_mean"]]

# Clamp PM2.5 to non-negative values
clarity["pm2_5_1h_mean"] = clarity["pm2_5_1h_mean"].clip(lower=0)

# Add date column for grouping
clarity["date_only"] = clarity["time"].dt.date

# Calculate 24-hour mean per sensor per day
daily_avg = (
    clarity.groupby(["location_id", "date_only"])['pm2_5_1h_mean']
    .mean()
    .reset_index()
    .rename(columns={"pm2_5_1h_mean": "pm2_5_24h_mean"})
)
daily_avg["pm2_5_24h_mean"] = daily_avg["pm2_5_24h_mean"].clip(lower=0)

# Merge daily average back in
clarity = pd.merge(clarity, daily_avg, on=["location_id", "date_only"], how="left")

# AQI calculation function
def calculate_pm2_5_aqi(C_p):
    if pd.isna(C_p):
        return None
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

# Apply AQI calculation
clarity["pm2_5_24h_mean_aqi"] = clarity["pm2_5_24h_mean"].apply(calculate_pm2_5_aqi)

# Keep and sort final columns
clarity = clarity.sort_values("time")
clarity = clarity[["time", "location_name", "location_id", "latitude", "longitude", "pm2_5_24h_mean", "pm2_5_24h_mean_aqi"]]

# Export cleaned Clarity data
clarity.to_csv("clean_clarity.csv", index=False)