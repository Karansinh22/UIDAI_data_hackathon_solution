import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

os.makedirs('visualizations', exist_ok=True)

# Load data
data = pd.read_csv('processed_data/update_behavior_data.csv')

# Top 15 Districts by Update Intensity (FIXED - wrap long names)
plt.figure(figsize=(14, 10))
top_districts = data.groupby('district')['update_to_enrollment_ratio'].mean().sort_values(ascending=False).head(15)
sns.barplot(x=top_districts.values, y=top_districts.index, palette='magma')
plt.title('Top 15 Districts by Update Intensity (Updates per Enrollment)', fontsize=14, fontweight='bold')
plt.xlabel('Update Ratio', fontsize=12)
plt.ylabel('District', fontsize=10)
# Wrap long labels
ax = plt.gca()
labels = ax.get_yticklabels()
ax.set_yticklabels(labels, fontsize=9)
plt.tight_layout()
plt.savefig('visualizations/03_top_update_intensity_districts.png', dpi=150, bbox_inches='tight')
plt.close()

print("✅ Update behavior visualizations updated!")
