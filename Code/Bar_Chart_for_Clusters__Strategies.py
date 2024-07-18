import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Data for clusters
data = {
    "Variables": ["Confirming Redundancy", "Simultaneous scanning", "Successive scanning",
                  "Conservative Focusing", "Focus gambling", "Fill up gaps", "Same rule",
                  "Verify prediction", "Falsify prediction", "Identify problem", "Posttest: Current", "Posttest: Voltage Drop"],
    "1 (Reinforced Confirmers)": [2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2],
    "2 (Dual-mode Strategy Diversifiers)": [0, 2, 2, 0, 0, 1, 3, 3, 1, 0, 3, 3],
    "3 (Multi-strategy Jugglers)": [4, 3, 1, 0, 1, 2, 8, 9, 1, 0, 4, 3],
    "4 (Self-regulated Revisers)": [2, 1, 3, 1, 0, 3, 5, 4, 1, 1, 5, 3],
    "5 (Methodical Integrators)": [0, 1, 2, 2, 0, 3, 3, 4, 2, 1, 5, 5]
}

# Create DataFrame
df = pd.DataFrame(data)

# Set the Variables as index
df.set_index("Variables", inplace=True)

# Define chart height and width
chart_height = 10
chart_width = 16

# Plotting
fig, ax = plt.subplots(figsize=(chart_width, chart_height))

# Define cluster colors
cluster_colors = ['b', 'g', 'c', 'y', 'r']

# Set the width of each bar group
bar_width = 0.12
index = np.arange(len(df.index))

# Plot each bar group with cluster color codes
for i, cluster in enumerate(df.columns):
    ax.bar(index + i * bar_width, df[cluster], bar_width, color=cluster_colors[i], label=cluster)

# Set the title and labels
ax.set_title('Comparison of Variables Among Clusters', fontsize=16)
ax.set_xlabel('Variables', fontsize=12)
ax.set_ylabel('Count / Score', fontsize=12)

# Rotate the x-axis labels for better visibility
plt.xticks(index + bar_width * (len(df.columns) - 1) / 2, df.index, rotation=45, ha="right")

# Set y-axis ticks
plt.yticks(np.arange(0, 10, 1))  # This sets the y-axis ticks at intervals of 1

# Display the legend outside the plot
plt.legend(title='Clusters', bbox_to_anchor=(1.05, 1), loc='upper left')

# Add horizontal grid lines for better readability
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

# Add some margin to the right for the legend and to the bottom for the labels
plt.subplots_adjust(right=0.75, bottom=0.35)

# Save chart as a PNG image with higher resolution
plt.savefig('chart.png', dpi=200, bbox_inches='tight')

# Show the plot
plt.show()
