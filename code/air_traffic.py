import pandas as pd
import matplotlib.pyplot as plt

# Load the air traffic file
file_path = '../data/air_traffic.csv'
df = pd.read_csv(file_path)

# Convert date column to datetime format
df['activity_period_start_date'] = pd.to_datetime(df['activity_period_start_date'])

# Extract year and month
df['year'] = df['activity_period_start_date'].dt.year
df['month'] = df['activity_period_start_date'].dt.to_period('M')

# Filter data for the years 2018 to 2025
filtered_df = df[(df['year'] >= 2018) & (df['year'] <= 2025)]

# Group by month and sum passenger counts
monthly_passenger_traffic = (
    filtered_df
    .groupby('month')['passenger_count']
    .sum()
    .reset_index()
)

# Convert month to datetime for plotting
monthly_passenger_traffic['month'] = monthly_passenger_traffic['month'].astype(str)
monthly_passenger_traffic['month'] = pd.to_datetime(monthly_passenger_traffic['month'])

# Plot
plt.figure(figsize=(14, 6))
plt.plot(monthly_passenger_traffic['month'], monthly_passenger_traffic['passenger_count'], marker='o')
plt.title('Monthly Passenger Traffic at SFO (2018–2025)', fontsize=16)
plt.xlabel('Month')
plt.ylabel('Passenger Count')
plt.grid(True)
plt.tight_layout()
plt.show()