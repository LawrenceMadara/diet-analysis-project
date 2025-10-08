import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os

warnings.filterwarnings('ignore')

# Create output directory
os.makedirs('output', exist_ok=True)

print("="*70)
print(f"DIET ANALYSIS PROJECT - Task 1")
print(f"Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

print("\nLoading dataset...")
try:
    df = pd.read_csv('All_Diets.csv')
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: All_Diets.csv not found!")
    print("Please make sure the file is in the same directory.")
    exit()

print("\n" + "="*70)
print("DATASET INFORMATION")
print("="*70)
print(f"\nDataset shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\nFirst few rows:")
print(df.head())

numerical_columns = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
for col in numerical_columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mean(), inplace=True)
        print(f"Filled missing values in {col}")

print("\n" + "="*70)
print("TASK 1: Average Macronutrients by Diet Type")
print("="*70)
avg_macros = df.groupby('Diet_type')[numerical_columns].mean()
print(avg_macros.round(2))

print("\n" + "="*70)
print("TASK 2: Top 5 Protein-Rich Recipes by Diet Type")
print("="*70)
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
print(top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']].head(15))

print("\n" + "="*70)
print("TASK 3: Diet Type with Highest Average Protein")
print("="*70)
highest_protein_diet = avg_macros['Protein(g)'].idxmax()
highest_protein_value = avg_macros['Protein(g)'].max()
print(f"Diet with highest average protein: {highest_protein_diet}")
print(f"Average protein content: {highest_protein_value:.2f}g")

print("\n" + "="*70)
print("TASK 4: Most Common Cuisines by Diet Type")
print("="*70)
common_cuisines = df.groupby('Diet_type')['Cuisine_type'].agg(
    lambda x: x.mode()[0] if not x.mode().empty else 'N/A'
)
print(common_cuisines)

print("\n" + "="*70)
print("TASK 5: Creating New Metrics (Ratios)")
print("="*70)
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)'].replace(0, 1)
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)'].replace(0, 1)
print("New metrics created!")

df.to_csv('output\\processed_diet_data.csv', index=False)
print("\nProcessed data saved!")

print("\n" + "="*70)
print("CREATING VISUALIZATIONS")
print("="*70)

sns.set_style("whitegrid")

# Bar Chart
print("\nCreating bar chart...")
plt.figure(figsize=(12, 7))
avg_macros.plot(kind='bar', color=['#FF6B6B', '#4ECDC4', '#FFE66D'])
plt.title('Average Macronutrient Content by Diet Type', fontsize=16, fontweight='bold')
plt.xlabel('Diet Type', fontsize=12)
plt.ylabel('Amount (grams)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Nutrients')
plt.tight_layout()
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
plt.text(0.99, 0.01, f'Generated: {timestamp}', transform=plt.gca().transAxes, 
         fontsize=8, ha='right', va='bottom', alpha=0.7)
plt.savefig('output\\bar_chart_macros.png', dpi=300, bbox_inches='tight')
print(f"Bar chart saved at {timestamp}")
plt.close()

# Heatmap
print("\nCreating heatmap...")
plt.figure(figsize=(10, 8))
correlation_data = df.groupby('Diet_type')[numerical_columns].mean()
sns.heatmap(correlation_data.T, annot=True, cmap='YlOrRd', fmt='.1f')
plt.title('Heatmap: Macronutrient Content by Diet Type', fontsize=16, fontweight='bold')
plt.tight_layout()
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
plt.text(0.99, 0.01, f'Generated: {timestamp}', transform=plt.gca().transAxes, 
         fontsize=8, ha='right', va='bottom', alpha=0.7)
plt.savefig('output\\heatmap_macros.png', dpi=300, bbox_inches='tight')
print(f"Heatmap saved at {timestamp}")
plt.close()

# Scatter Plot
print("\nCreating scatter plot...")
plt.figure(figsize=(15, 9))
diet_types = df['Diet_type'].unique()
colors = plt.cm.Set3(range(len(diet_types)))
for idx, diet in enumerate(diet_types):
    diet_data = df[df['Diet_type'] == diet].nlargest(5, 'Protein(g)')
    plt.scatter(diet_data['Cuisine_type'], diet_data['Protein(g)'], 
                label=diet, s=150, alpha=0.7, color=colors[idx])
plt.title('Top 5 Protein-Rich Recipes by Cuisine and Diet Type', fontsize=16, fontweight='bold')
plt.xlabel('Cuisine Type', fontsize=12)
plt.ylabel('Protein (grams)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
plt.text(0.99, 0.01, f'Generated: {timestamp}', transform=plt.gca().transAxes, 
         fontsize=8, ha='right', va='bottom', alpha=0.7)
plt.savefig('output\\scatter_protein_recipes.png', dpi=300, bbox_inches='tight')
print(f"Scatter plot saved at {timestamp}")
plt.close()

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)
print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nAll tasks completed successfully!")
print("="*70)