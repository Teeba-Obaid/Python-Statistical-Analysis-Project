import numpy as np
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
from scikit_posthocs import posthoc_dunn
from scipy.stats import shapiro
import seaborn as sns
from scipy.stats import spearmanr, wilcoxon, kruskal

# Read the data from the file
try:
    data = pd.read_csv('data10.csv', header=None)
except FileNotFoundError:
    print('Error: file not found')
    exit()

# Use the first row as column labels
data.columns = data.iloc[0]

# Drop the first row
data = data.drop(0)

# Convert the frequency values to integers
data.iloc[:, 1:] = data.iloc[:, 1:].astype(int)

# Set the dependent variables as integers
data.iloc[0] = data.iloc[0].astype(int)

# Create a new column called "Group"
data['Group'] = np.repeat(['Control', 'Experimental 1', 'Experimental 2'], 20)

# Define sources of variation
sources_of_variation = ['Group']

# Convert dependent variables to float
data_without_group = data.drop('Group', axis=1)
dependent_variables = data_without_group.columns
data[dependent_variables] = data_without_group.astype(float)


def rank_correlation(data):
    correlations = []
    for group_data in data:
        if len(group_data) < 2:
            correlations.append([np.nan,np.nan])
            continue
        if np.all(group_data == group_data[0]):
            correlations.append([0, np.nan])
            continue
        corr,pval = spearmanr(np.array(group_data))
        correlations.append([corr,pval])
    return correlations




def wilcoxon_test(data):
    group_1 = data[0]
    group_2 = data[1]
    group_1_corr = group_1[~np.isnan(group_1)]
    group_2_corr = group_2[~np.isnan(group_2)]

    if not (isinstance(group_1_corr[0], float) and isinstance(group_2_corr[0], float)):
        return np.nan

    if len(group_1_corr) < 2 or len(group_2_corr) < 2:
        return np.nan

    if np.isnan(group_1_corr[0]) or np.isnan(group_2_corr[0]):
        return np.nan

    if group_1_corr[-1] > 0.05 or group_2_corr[-1] > 0.05:
        return np.nan

    test_statistic, pval = wilcoxon(group_1_corr, group_2_corr)
    return pval


# Calculate Spearman's rank correlation coefficient separately for each group
group_correlation = []
for group in data['Group'].unique():
    group_data = data[data['Group'] == group].iloc[:, 1:-1]
    if len(group_data) > 1:
        correlation, p_value = spearmanr(group_data.to_numpy())
        group_correlation.append((correlation, p_value))

# Compare the coefficients between the groups
results = pd.DataFrame({
    'Group': ['Control', 'Experimental 1', 'Experimental 2'],
    "Spearman's rank correlation coefficients": [i[0] for i in group_correlation]
})

# Test for significant differences between two groups using Wilcoxon rank-sum test
if len(group_correlation) >= 2:
    print(f"Wilcoxon rank-sum test (Control vs Experimental 1):")

# Convert the dictionary to a dataframe and write it to a CSV file
results = pd.DataFrame(results)
results.to_csv('results.csv', index=False)
