import numpy as np
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
from scikit_posthocs import posthoc_dunn
from scipy.stats import shapiro
import seaborn as sns
from scipy.stats import spearmanr

# Read the data from the file
data = pd.read_csv('data9.csv',header=None)

# Use the first row as column labels
data.columns = data.iloc[0]

# Drop the first row
data = data.drop(0)

# Convert the frequency values to integers
data.iloc[:,1:] = data.iloc[:,1:].astype(int)

# Set the dependent variables as integers
data.iloc[0] = data.iloc[0].astype(int)

# Create a new column called "Group"
data['Group'] = np.repeat(['Control','Experimental 1','Experimental 2'],20)

# Define your sources of variation
sources_of_variation = ['Group']

# Convert the dependent variables to float
data_without_group = data.drop('Group',axis=1)
dependent_variables = data_without_group.columns
data[dependent_variables] = data_without_group.astype(float)


# Perform Shapiro-Wilk normality test
shapiro_results = []
for var in dependent_variables:
    shapiro_results.append(shapiro(data[var]))

# Calculate Pearson and Spearman correlations between variables
pearson_corr_matrix = data[dependent_variables].corr()
spearman_corr_matrix = data[dependent_variables].corr(method='spearman')

# Perform Dunn's test and print the results for each dependent variable
for var in dependent_variables:
    dunn_results = posthoc_dunn(data,val_col=var,group_col='Group')
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
    effect_sizes = [
        (np.mean(data[data['Group'] == 'Control'][var]) - np.mean(data[data['Group'] == 'Experimental 1'][var])) /
        np.sqrt((np.std(data[data['Group'] == 'Control'][var]) ** 2 + np.std(
            data[data['Group'] == 'Experimental 1'][var]) ** 2) / 2),
        (np.mean(data[data['Group'] == 'Control'][var]) - np.mean(data[data['Group'] == 'Experimental 2'][var])) /
        np.sqrt((np.std(data[data['Group'] == 'Control'][var]) ** 2 + np.std(
            data[data['Group'] == 'Experimental 2'][var]) ** 2) / 2),
        (np.mean(data[data['Group'] == 'Experimental 1'][var]) - np.mean(
            data[data['Group'] == 'Experimental 2'][var])) /
        np.sqrt((np.std(data[data['Group'] == 'Experimental 1'][var]) ** 2 + np.std(
            data[data['Group'] == 'Experimental 2'][var]) ** 2) / 2)]
    print("Effect sizes (Cohen's d):")
    print(effect_sizes)

    # Loop through each dependent variable
    for var in dependent_variables:

        # Calculate and print p-values
        p_values = [stats.ranksums(data[data['Group'] == 'Control'][var],
                                   data[data['Group'] == 'Experimental 1'][var])[1],
                    stats.ranksums(data[data['Group'] == 'Control'][var],
                                   data[data['Group'] == 'Experimental 2'][var])[1],
                    stats.ranksums(data[data['Group'] == 'Experimental 1'][var],
                                   data[data['Group'] == 'Experimental 2'][var])[1]]
        print(f"P-values for {var}: {p_values}")

        # Check if any of the p-values are less than alpha
        if any(p < 0.05 for p in p_values):
            print(f"The correlation for {var} is statistically significant.")
        else:
            print(f"The correlation for {var} is not statistically significant.")

    # Calculate and print correlations with other variables
    print("Pearson correlation matrix:")
    print(pearson_corr_matrix)

    print("Spearman correlation matrix:")
    print(spearman_corr_matrix)
# Calculate Pearson and Spearman correlations between variables
pearson_corr_matrix = data[dependent_variables].corr()
spearman_corr_matrix = data[dependent_variables].corr(method='spearman')

# Calculate p-values for Spearman correlations
spearman_p_values = pd.DataFrame(np.zeros_like(spearman_corr_matrix), columns=dependent_variables, index=dependent_variables)
for i in range(len(dependent_variables)):
    for j in range(len(dependent_variables)):
        corr, p = stats.spearmanr(data[dependent_variables[i]], data[dependent_variables[j]])
        spearman_p_values.iloc[i, j] = p

# Combine correlation and p-value matrices into a single matrix
corr_and_p_values = pd.concat([pearson_corr_matrix, spearman_corr_matrix, spearman_p_values], keys=['pearson', 'spearman', 'p-value'], axis=1)

# Add asterisks to significant correlation values
corr_matrix_with_asterisks = spearman_corr_matrix.copy()

for i in range(len(dependent_variables)):
    for j in range(i):  # iterate only up to i
        p = corr_and_p_values.iloc[i, j + len(dependent_variables)*2]
        if p < 0.05:
            corr_matrix_with_asterisks.iloc[i, j] = f"{corr_matrix_with_asterisks.iloc[i, j]:.2f}*"
        else:
            corr_matrix_with_asterisks.iloc[i, j] = f"{corr_matrix_with_asterisks.iloc[i, j]:.2f}"
        # set the value in the upper triangle to NaN to omit it
        corr_matrix_with_asterisks.iloc[j, i] = np.nan

# Save the correlation matrix with asterisks to a separate CSV file
corr_matrix_with_asterisks.to_csv('correlation_matrix_with_asterisks.csv')

# Read the correlation matrix with asterisks from the CSV file
corr_matrix_with_asterisks = pd.read_csv('correlation_matrix_with_asterisks.csv', index_col=0)

# Get the lower triangle indices
tril_indices = np.tril_indices_from(corr_matrix_with_asterisks)

# Extract the lower triangle of the correlation matrix with asterisks
lower_triangle = corr_matrix_with_asterisks.iloc[tril_indices]

# Print the lower triangle
print("Lower triangle of the Spearman correlation matrix with asterisks:")
print(lower_triangle)

# Print significant Spearman correlations with asterisks
print("Significant Spearman correlations with asterisks (p < 0.05):")
for i in range(len(dependent_variables)):
    for j in range(i):
        p = corr_and_p_values.iloc[i, j + len(dependent_variables)*2]
        if p < 0.05:
            corr_val = corr_matrix_with_asterisks.iloc[i, j]
            print(f"{dependent_variables[i]} - {dependent_variables[j]}: {corr_val}")

# Read the data from the file
data = pd.read_csv('correlation_matrix_with_asterisks.csv', index_col=0)

# Convert the frequency values to integers
for col in data.columns:
    data[col] = data[col].astype(float)

# Create a new column called "Group"
data['Group'] = np.repeat(['Control', 'Experimental 1', 'Experimental 2'], 1)

# Define your sources of variation
sources_of_variation = ['Group']

# Calculate Pearson and Spearman correlations between variables
corr_matrix = data.drop('Group', axis=1).corr()

for i in range(len(data)):
    for j in range(len(data.columns)):
        try:
            float(data.iloc[i, j])
        except ValueError:
            print(f"Could not convert {data.iloc[i, j]} to a float at position ({i}, {j})")

# Create a heatmap using seaborn
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)

# Show the plot
plt.show()
