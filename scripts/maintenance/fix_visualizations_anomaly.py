import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

os.makedirs('visualizations', exist_ok=True)

# Load data
data = pd.read_csv('processed_data/anomaly_detection_data.csv')

# Enrollment Outliers by State (FIXED - reduce states shown, rotate labels)
plt.figure(figsize=(16, 8))
# Only show top 15 states by volume to avoid overcrowding
top_states = data.groupby('state')['total_enrollments'].sum().nlargest(15).index
filtered_data = data[data['state'].isin(top_states)]

sns.boxplot(x='state', y='total_enrollments', data=filtered_data)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.title('Distribution of Enrollments by State (Top 15 States)', fontsize=14, fontweight='bold')
plt.xlabel('State', fontsize=12)
plt.ylabel('Total Enrollments', fontsize=12)
plt.tight_layout()
plt.savefig('visualizations/04_enrollment_outliers_by_state.png', dpi=150, bbox_inches='tight')
plt.close()

print("✅ Anomaly detection visualizations updated!")
