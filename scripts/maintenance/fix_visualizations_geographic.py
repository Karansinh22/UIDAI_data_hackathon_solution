import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

os.makedirs('visualizations', exist_ok=True)

# Load data
data = pd.read_csv('processed_data/geographic_data.csv')

# 1. Top 10 States (IMPROVED - better sizing and labels)
plt.figure(figsize=(12, 6))
state_data = data.groupby('state')['total_enrollments'].sum().sort_values(ascending=False).head(10)
state_data.plot(kind='bar', color='skyblue')
plt.title('Top 10 States by Total Enrollments', fontsize=14, fontweight='bold')
plt.ylabel('Enrollments', fontsize=12)
plt.xlabel('State', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('visualizations/01_top_10_states_enrollment.png', dpi=150, bbox_inches='tight')
plt.close()

# 2. Enrollments vs Updates (no changes needed)
plt.figure(figsize=(12, 6))
sns.scatterplot(data=data, x='total_enrollments', y='total_updates', alpha=0.5)
plt.title('Enrollments vs Total Updates by Pincode', fontsize=14, fontweight='bold')
plt.xlabel('Total Enrollments', fontsize=12)
plt.ylabel('Total Updates', fontsize=12)
plt.tight_layout()
plt.savefig('visualizations/01_enrollments_vs_updates_correlation.png', dpi=150, bbox_inches='tight')
plt.close()

print("✅ Geographic visualizations updated!")
