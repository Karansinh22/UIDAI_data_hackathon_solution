import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import Ridge
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Ensure directories exist
os.makedirs('models', exist_ok=True)
os.makedirs('processed_data', exist_ok=True)

print("🚀 Starting ML Model Training Pipeline...")

# 1. Load Data
geo_df = pd.read_csv('processed_data/geographic_data.csv')
anomaly_df = pd.read_csv('processed_data/anomaly_detection_data.csv')
predictive_df = pd.read_csv('processed_data/predictive_data.csv')

# Population data for normalization
pop_data = {
    'Uttar Pradesh': 241.1, 'Bihar': 136.0, 'Maharashtra': 127.1, 'West Bengal': 99.8,
    'Madhya Pradesh': 88.4, 'Rajasthan': 82.9, 'Tamil Nadu': 77.5, 'Gujarat': 74.4,
    'Karnataka': 69.5, 'Andhra Pradesh': 53.3, 'Odisha': 47.0, 'Jharkhand': 41.3,
    'Telangana': 38.4, 'Kerala': 36.0, 'Assam': 36.0, 'Punjab': 31.0, 'Haryana': 30.5,
    'Chhattisgarh': 30.5, 'Delhi': 20.4, 'Jammu and Kashmir': 13.8, 'Uttarakhand': 11.8,
    'Himachal Pradesh': 7.5, 'Tripura': 4.1, 'Meghalaya': 3.4, 'Manipur': 3.3,
    'Nagaland': 2.1, 'Goa': 1.6, 'Arunachal Pradesh': 1.5, 'Puducherry': 1.6,
    'Chandigarh': 1.2, 'Mizoram': 1.2, 'Sikkim': 0.69
}

# --- MODEL 1: Future Demand Forecaster ---
print("📦 Training Model 1: Future Demand Forecaster...")
df1 = predictive_df.copy()
df1['pop_millions'] = df1['state'].map(pop_data)
df1 = df1.dropna(subset=['pop_millions'])

# Prepare features
le = LabelEncoder()
df1['state_enc'] = le.fit_transform(df1['state'])

# Synthetic "Year" data for training (current=2024, historical=2023)
# We duplicate data to simulate growth trends
df_hist = df1.copy()
df_hist['year'] = 2023
df_hist['total_updates'] = (df1['total_demo_updates'] + df1['total_bio_updates']) * 0.9

df_curr = df1.copy()
df_curr['year'] = 2024
df_curr['total_updates'] = (df1['total_demo_updates'] + df1['total_bio_updates'])

df_ml = pd.concat([df_hist, df_curr])

X1 = df_ml[['state_enc', 'pop_millions', 'year', 'total_enrollments']]
y1 = df_ml['total_updates']

model1 = RandomForestRegressor(n_estimators=100, random_state=42)
model1.fit(X1, y1)

joblib.dump(model1, 'models/demand_forecaster.joblib', compress=3)
joblib.dump(le, 'models/state_encoder.joblib')


# --- MODEL 3: Infrastructure Optimizer ---
print("🏗️ Training Model 3: Infrastructure Optimizer...")
# Target: Optimal centers (derived: 1 center per 50k population + activity weight)
df3 = geo_df.copy()
df3['pop_millions'] = df3['state'].map(pop_data)
df3 = df3.dropna(subset=['pop_millions'])

# Features
state_agg = df3.groupby('state').agg({
    'total_enrollments': 'sum',
    'total_updates': 'sum',
    'pop_millions': 'first'
}).reset_index()

# Derive target: recommended centers
state_agg['recommended_centers'] = (state_agg['pop_millions'] * 20) + (state_agg['total_updates'] / 100000)
state_agg['state_enc'] = le.transform(state_agg['state'])

X3 = state_agg[['state_enc', 'pop_millions', 'total_updates']]
y3 = state_agg['recommended_centers']

model3 = Ridge()
model3.fit(X3, y3)

joblib.dump(model3, 'models/infra_optimizer.joblib', compress=3)


# --- MODEL 4: Anomaly Spike Warning ---
print("🚨 Training Model 4: Anomaly Spike Warning...")
# Target: Probability of a spike (synthetic: z_score > 2)
df4 = anomaly_df.copy()
df4['spike_label'] = np.where(df4['enr_z_score'] > 2, 1, 0)

# Features: Update ratios and volumes
df4['update_ratio'] = (df4['total_enrollments'] + 1) / (df4['total_enrollments'].mean() + 1)

X4 = df4[['enr_z_score', 'demo_z_score', 'total_enrollments']]
y4 = df4['spike_label']

model4 = RandomForestClassifier(n_estimators=50, random_state=42)
model4.fit(X4, y4)

joblib.dump(model4, 'models/spike_warning.joblib', compress=3)

print("✅ All Strategic ML Models Trained and Saved in /models/")
