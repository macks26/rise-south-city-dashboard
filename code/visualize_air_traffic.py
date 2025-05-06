import pandas as pd
import matplotlib.pyplot as plt

# Load PurpleAir data
purpleair = pd.read_csv('../data/clean_purpleair.csv')
air_traffic = pd.read_csv('../data/air_traffic.csv')

# Preprocess PurpleAir data
purpleair['time'] = pd.to_datetime(purpleair['time'])
purpleair['year_month'] = purpleair['time'].dt.to_period('M')
monthly_pm25_purpleair = purpleair.groupby('year_month')['pm2_5_1h_mean'].mean().reset_index()

# Filter PurpleAir for Dec 2018 - Dec 2023
monthly_pm25_purpleair = monthly_pm25_purpleair[(monthly_pm25_purpleair['year_month'] >= '2018-12') & (monthly_pm25_purpleair['year_month'] <= '2023-12')]

# Preprocess Air Traffic data
air_traffic['activity_period_start_date'] = pd.to_datetime(air_traffic['activity_period_start_date'])
air_traffic['year_month'] = air_traffic['activity_period_start_date'].dt.to_period('M')
monthly_air_traffic = air_traffic.groupby('year_month')['passenger_count'].sum().reset_index()

# PurpleAir PM 2.5 and Air Traffic (Dec 2018 - Dec 2023)
merged_data_pa = pd.merge(monthly_pm25_purpleair, monthly_air_traffic, on='year_month', how='inner')
fig, ax1 = plt.subplots(figsize=(14, 7))
ax1.plot(merged_data_pa['year_month'].dt.to_timestamp(), merged_data_pa['pm2_5_1h_mean'],
         color='purple', marker='o', label='Average PM 2.5 (PurpleAir)')
ax1.set_xlabel('Date')
ax1.set_ylabel('Average PM 2.5 (PurpleAir)', color='purple')
ax1.tick_params(axis='y', labelcolor='purple')

ax2 = ax1.twinx()
ax2.plot(merged_data_pa['year_month'].dt.to_timestamp(), merged_data_pa['passenger_count'],
         color='tab:blue', marker='o', label='Total Air Traffic')
ax2.set_ylabel('Total Air Traffic (Passengers)', color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')

ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
fig.autofmt_xdate(rotation=45)
ax1.grid(True, linestyle='--', alpha=0.5)
plt.title('Monthly Avg PM 2.5 (PurpleAir) & Air Traffic (Dec 2018–Dec 2023)')
fig.tight_layout()
plt.show()