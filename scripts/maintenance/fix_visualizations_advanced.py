import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

os.makedirs('visualizations', exist_ok=True)

# Load data
df = pd.read_csv('processed_data/pincode_data.csv')

# 1. Correlation Heatmap (IMPROVED - aesthetic names)
# Create a mapping of column names to beautiful display names
column_mapping = {
    'age_0_5': 'Children (0-5)',
    'age_5_17': 'Youth (5-17)',
    'age_18_greater': 'Adults (18+)',
    'demo_age_5_17': 'Demographic Update (Youth)',
    'demo_age_17_': 'Demographic Update (Adult)',
    'bio_age_5_17': 'Biometric Update (Youth)',
    'bio_age_17_': 'Biometric Update (Adult)'
}

# Select and rename columns
corr_df = df[list(column_mapping.keys())].rename(columns=column_mapping)
corr_matrix = corr_df.corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, 
            square=True, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix: Aadhaar Service Activities', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(rotation=0, fontsize=10)
plt.tight_layout()
plt.savefig('visualizations/07_metric_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

# 2. Demographic vs Biometric Index (IMPROVED - larger figure, clearer labels)
df['total_demo'] = df['demo_age_5_17'] + df['demo_age_17_']
df['total_bio'] = df['bio_age_5_17'] + df['bio_age_17_']
df['update_type_index'] = df['total_demo'] / (df['total_bio'] + 1)

state_index = df.groupby('state')['update_type_index'].mean().sort_values()

plt.figure(figsize=(10, 12))
state_index.plot(kind='barh', color='teal')
plt.axvline(1, color='red', linestyle='--', label='Balanced Ratio', linewidth=2)
plt.title('Demographic-to-Biometric Update Index by State', fontsize=14, fontweight='bold')
plt.xlabel('Ratio (Demographic / Biometric)', fontsize=12)
plt.ylabel('State', fontsize=12)
plt.yticks(fontsize=9)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('visualizations/07_demo_vs_bio_index_by_state.png', dpi=150, bbox_inches='tight')
plt.close()

# 3. Growth vs Saturation Bubble Plot (IMPROVED - selective labels, larger text)
df['total_updates'] = df['total_demo'] + df['total_bio']

# Aggregate to state
state_pivot = df.groupby('state').agg({
    'age_0_5': 'sum',
    'total_updates': 'sum',
    'pincode': 'count'
}).rename(columns={'pincode': 'num_pincodes'})

plt.figure(figsize=(16, 10))
sns.scatterplot(data=state_pivot, x='age_0_5', y='total_updates', 
                size='num_pincodes', hue='num_pincodes', palette='viridis', 
                sizes=(200, 2000), alpha=0.7, edgecolor='black', linewidth=0.5)

# Only label top 10 states by total activity for readability
state_pivot['total_activity'] = state_pivot['age_0_5'] + state_pivot['total_updates']
top_states = state_pivot.nlargest(10, 'total_activity').index

for i, state in enumerate(state_pivot.index):
    if state in top_states:
        plt.annotate(state, 
                    (state_pivot['age_0_5'].iloc[i], state_pivot['total_updates'].iloc[i]),
                    fontsize=11, fontweight='bold', alpha=0.9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='gray'))

plt.title('Market Maturity: New Child Enrollments vs. System Updates by State', fontsize=16, fontweight='bold')
plt.xlabel('Child Enrollments (0-5 Years)', fontsize=13)
plt.ylabel('Total Citizen Updates', fontsize=13)
plt.legend(title='Number of Pincodes', fontsize=10, title_fontsize=11)
plt.tight_layout()
plt.savefig('visualizations/07_growth_saturation_bubble_plot.png', dpi=150, bbox_inches='tight')
plt.close()

print("✅ Advanced insights visualizations updated!")
