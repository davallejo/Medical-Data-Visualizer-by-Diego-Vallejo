#medical_data_visualizer.py
#Autor: Diego Armando Vallejo Vinueza

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("medical_examination.csv")

# Add overweight column
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

# Normalize data
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# Convert data into long format
df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

# Group and reformat the data
df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

# Draw catplot
def draw_cat_plot():
    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat, kind='bar').fig
    return fig

# Clean the data
df_heat = df[(df['ap_lo'] <= df['ap_hi'])
             & (df['height'] >= df['height'].quantile(0.025))
             & (df['height'] <= df['height'].quantile(0.975))
             & (df['weight'] >= df['weight'].quantile(0.025))
             & (df['weight'] <= df['weight'].quantile(0.975))]

# Calculate the correlation matrix
corr = df_heat.corr()

# Generate a mask for the upper triangle
mask = np.triu(corr)

# Draw the heatmap
def draw_heat_map():
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt='.1f', linewidths=.5, cmap='coolwarm', mask=mask, square=True, ax=ax)
    return fig

# Save catplot and heatmap figures
fig_cat_plot = draw_cat_plot()
fig_cat_plot.savefig('catplot.png')

fig_heat_map = draw_heat_map()
fig_heat_map.savefig('heatmap.png')
