import pandas as pd

# Load cleaned Clarity and PurpleAir data
clarity = pd.read_csv("clean_clarity.csv")
purpleair = pd.read_csv("clean_api_purpleair.csv")

# Merge on time + location_name to find overlapping locations + dates
merged = pd.merge(
    clarity,
    purpleair,
    on=['time', 'location_name'],
    suffixes=('_clarity', '_purpleair')
)

# Filter to rows where both sources have data at the same time + location
overlap = merged.dropna(subset=['pm2_5_24h_mean_clarity', 'pm2_5_24h_mean_purpleair'])

# How many overlap points?
print(f"Number of overlapping rows: {len(overlap)}")

if len(overlap) == 0:
    print("No overlapping data found. Cannot compute weights.")
else:
    # Calculate variance
    clarity_var = overlap['pm2_5_24h_mean_clarity'].var()
    purpleair_var = overlap['pm2_5_24h_mean_purpleair'].var()

    # Inverse variance weighting
    clarity_weight = (1 / clarity_var) / ((1 / clarity_var) + (1 / purpleair_var))
    purpleair_weight = (1 / purpleair_var) / ((1 / clarity_var) + (1 / purpleair_var))

    print(f"Clarity weight:    {clarity_weight:.2f}")
    print(f"PurpleAir weight:  {purpleair_weight:.2f}")