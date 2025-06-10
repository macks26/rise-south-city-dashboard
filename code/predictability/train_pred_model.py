# train_pred_model.py

import pandas as pd
from geopy.distance import geodesic
from sklearn.ensemble import RandomForestRegressor
import pickle

# === Load Data ===
# print current working directory
df = pd.read_csv("data/combined_scores.csv")

# Clean coordinates
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df = df.dropna(subset=['latitude', 'longitude'])

# === Build Training Data ===
rows = []
for idx, row in df.iterrows():
    target_latlon = (row['latitude'], row['longitude'])
    target_val = row['predictability']

    # Exclude self, compute distances
    neighbors = df[df['location_id'] != row['location_id']].copy()
    neighbors['distance'] = neighbors.apply(
        lambda n: geodesic((n['latitude'], n['longitude']), target_latlon).miles, axis=1
    )
    closest = neighbors.nsmallest(5, 'distance')

    # Create feature vector
    feature_row = {}
    for i, n in enumerate(closest.itertuples(), start=1):
        feature_row[f'neighbor_{i}_distance'] = n.distance
        feature_row[f'neighbor_{i}_predictability'] = n.predictability
        feature_row[f'neighbor_{i}_consistency'] = n.consistency

    feature_row['target_predictability'] = target_val
    rows.append(feature_row)

train_df = pd.DataFrame(rows)

# === Train Model ===
X = train_df.drop(columns=["target_predictability"])
y = train_df["target_predictability"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# === Save Model with Pickle ===
with open("data/rf_predictability_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to rf_predictability_model.pkl")
