import numpy as np
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
from scikit_posthocs import posthoc_dunn
from scipy.stats import shapiro

# Read the data from the file
data = pd.read_csv('data5.csv', header=None)

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

# Define your sources of variation
sources_of_variation = ['Group']

# Convert the dependent variables to float
data_without_group = data.drop('Group', axis=1)
dependent_variables = data_without_group.columns
data[dependent_variables] = data_without_group.astype(float)

# Perform Shapiro-Wilk normality test
shapiro_results = []
for var in dependent_variables:
    shapiro_results.append(shapiro(data[var]))

# Perform Dunn's test and print the results for each dependent variable
for var in dependent_variables:
    dunn_results = posthoc_dunn(data, val_col=var, group_col='Group')
    print(f"Post-hoc Dunn's test for {var}:")
    print(dunn_results)

    # Calculate and print p-values
    p_values = [stats.ranksums(data[data['Group'] == 'Control'][var],
                               data[data['Group'] == 'Experimental 1'][var])[1],
                stats.ranksums(data[data['Group'] == 'Control'][var],
                               data[data['Group'] == 'Experimental 2'][var])[1],
                stats.ranksums(data[data['Group'] == 'Experimental 1'][var],
                               data[data['Group'] == 'Experimental 2'][var])[1]]
    print("p-values:")
    print(p_values)

    # Calculate and print effect sizes (Cohen's d)
    effect_sizes = [(np.mean(data[data['Group'] == 'Control'][var]) - np.mean(data[data['Group'] == 'Experimental 1'][var])) /
                    np.sqrt((np.std(data[data['Group'] == 'Control'][var]) ** 2 + np.std(data[data['Group'] == 'Experimental 1'][var]) ** 2) / 2),
                    (np.mean(data[data['Group'] == 'Control'][var]) - np.mean(data[data['Group'] == 'Experimental 2'][var])) /
                    np.sqrt((np.std(data[data['Group'] == 'Control'][var]) ** 2 + np.std(data[data['Group'] == 'Experimental 2'][var]) ** 2) / 2),
                    (np.mean(data[data['Group'] == 'Experimental 1'][var]) - np.mean(data[data['Group'] == 'Experimental 2'][var])) /
                    np.sqrt((np.std(data[data['Group'] == 'Experimental 1'][var]) ** 2 + np.std(data[data['Group'] == 'Experimental 2'][var]) ** 2) / 2)]
    print("Effect sizes (Cohen's d):")
    print(effect_sizes)
