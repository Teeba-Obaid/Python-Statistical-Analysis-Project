import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = pd.read_csv("data9.csv")

# Split the data into groups
control = data.iloc[:20, :]
exp1 = data.iloc[20:40, :]
exp2 = data.iloc[40:, :]

# Perform Dunn's test for each variable
results = []
for column in data.columns:
    control_values = control[column]
    exp1_values = exp1[column]
    exp2_values = exp2[column]
    stat, p = stats.kruskal(control_values, exp1_values, exp2_values)
    results.append({"Variable": column, "Statistic": stat, "P-value": p})

# Convert the results to a pandas dataframe
results_df = pd.DataFrame(results)

# Filter for significant results
sig_results = results_df[results_df["P-value"] < 0.05]

# Generate heatmaps for each comparison
for group1, group2, name1, name2 in [(control, exp1, "Control", "Experimental 1"), (control, exp2, "Control", "Experimental 2"), (exp1, exp2, "Experimental 1", "Experimental 2")]:
    # Compute the Spearman's correlation matrix
    corr = group1.corr(method="spearman").subtract(group2.corr(method="spearman"))

    # Create a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Generate the heatmap
    plt.figure(figsize=(8, 8))
    sns.heatmap(corr, cmap="coolwarm", annot=False, mask=mask)

    # Set the plot title
    title = f"Spearman's correlation: {name1} vs {name2}"
    plt.title(title)

    # Rotate x and y axis labels
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)

    # Set x and y axis label sizes
    plt.tick_params(axis='x', labelsize=10)
    plt.tick_params(axis='y', labelsize=10)

    # Show the plot
    plt.savefig(f"{name1}_vs_{name2}.png")
    plt.show()
