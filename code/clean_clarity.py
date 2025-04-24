import pandas as pd

# Load Clarity data
clarity = pd.read_csv("risesouthcity_april_hourly.csv", parse_dates=["startOfPeriod"])

# Convert to Pacific and strip tz info
clarity["startOfPeriod"] = pd.to_datetime(clarity["startOfPeriod"], utc=True)
clarity["startOfPeriod"] = clarity["startOfPeriod"].dt.tz_convert("US/Pacific").dt.tz_localize(None)

# Rename and select columns
clarity = clarity.rename(columns={
    "startOfPeriod": "time",
    "Name": "location_name",
    "datasourceId": "location_id",
    "locationLatitude": "latitude",
    "locationLongitude": "longitude",
    "pm2_5ConcMass1HourMean.value": "pm2_5_1h_mean",
    "relHumidInternal1HourMean.value": "rh",
    "temperatureInternal1HourMean.value": "temp"
})

clarity = clarity[["time", "location_name", "location_id", "latitude", "longitude", "pm2_5_1h_mean", "rh", "temp"]]

# Clamp PM2.5 to non-negative values
clarity["pm2_5_1h_mean"] = clarity["pm2_5_1h_mean"].clip(lower=0)

# Add date column for 24h grouping
clarity["date_only"] = clarity["time"].dt.date

# Calculate 24h mean per sensor per day
daily_avg = (
    clarity.groupby(["location_id", "date_only"])["pm2_5_1h_mean"]
    .mean()
    .reset_index()
    .rename(columns={"pm2_5_1h_mean": "pm2_5_24h_mean"})
)

# Clamp to non-negative
daily_avg["pm2_5_24h_mean"] = daily_avg["pm2_5_24h_mean"].clip(lower=0)

# Merge 24h average back into hourly data
clarity = pd.merge(clarity, daily_avg, on=["location_id", "date_only"], how="left")

# AQI calculation function
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

# Calculate AQI values
clarity["pm2_5_1h_mean_aqi"] = clarity["pm2_5_1h_mean"].apply(calculate_pm2_5_aqi)
clarity["pm2_5_24h_mean_aqi"] = clarity["pm2_5_24h_mean"].apply(calculate_pm2_5_aqi)

# Sort and organize columns
clarity = clarity.sort_values("time")
clarity = clarity[["time", "location_name", "location_id", "latitude", "longitude",
                   "pm2_5_1h_mean", "pm2_5_1h_mean_aqi",
                   "pm2_5_24h_mean", "pm2_5_24h_mean_aqi",
                   "temp", "rh"]]

# Export
clarity.to_csv("clean_clarity.csv", index=False)