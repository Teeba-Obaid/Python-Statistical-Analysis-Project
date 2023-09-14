import numpy as np
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
from scikit_posthocs import posthoc_dunn
from scipy.stats import shapiro
import seaborn as sns
from scipy.stats import spearmanr
from itertools import combinations


# Read the data from the file
data = pd.read_csv('data9.csv', header=None)

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
dependent_variables = data_without_group.columns.str.replace('_', ' ')
data[dependent_variables] = data_without_group.astype(float)

# Create separate data frames for each group
control_data = data[data['Group'] == 'Control'].reset_index(drop=True).drop('Group', axis=1)
exp1_data = data[data['Group'] == 'Experimental 1'].reset_index(drop=True).drop('Group', axis=1)
exp2_data = data[data['Group'] == 'Experimental 2'].reset_index(drop=True).drop('Group', axis=1)

# Calculate Pearson and Spearman correlations between variables for each group
control_corr_matrix = control_data.corr(method='spearman')
exp1_corr_matrix = exp1_data.corr(method='spearman')
exp2_corr_matrix = exp2_data.corr(method='spearman')

# Get the lower triangle indices for each correlation matrix
control_tril_indices = np.tril_indices_from(control_corr_matrix)
exp1_tril_indices = np.tril_indices_from(exp1_corr_matrix)
exp2_tril_indices = np.tril_indices_from(exp2_corr_matrix)

# Extract the lower triangle of each correlation matrix
control_lower_triangle = np.tril(control_corr_matrix)
exp1_lower_triangle = np.tril(exp1_corr_matrix)
exp2_lower_triangle = np.tril(exp2_corr_matrix)

# Set seaborn style
sns.set_style("white")


# Create heatmaps using seaborn for each group
sns.set(font_scale=0.7)

# Control group heatmap
plt.figure(figsize=(8, 8))
sns.heatmap(control_lower_triangle, cmap='coolwarm', annot=False, vmin=-1, vmax=1, mask=np.zeros_like(control_lower_triangle, dtype=np.bool), square=True, xticklabels=dependent_variables, yticklabels=dependent_variables)
plt.title('Control')
plt.tight_layout()
plt.savefig('control_heatmap.png', dpi=400)
ax = plt.gca()  # get the current axis
ax.set_xticklabels(ax.get_xticklabels(), ha='right', fontsize=8)  # adjust x-axis labels
ax.set_yticklabels(ax.get_yticklabels(), ha='right', fontsize=8)  # adjust y-axis labels

# Experimental 1 group heatmap
plt.figure(figsize=(8, 8))
sns.heatmap(exp1_lower_triangle, cmap='coolwarm', annot=False, vmin=-1, vmax=1, mask=np.zeros_like(exp1_lower_triangle, dtype=np.bool), square=True, xticklabels=dependent_variables, yticklabels=dependent_variables)
plt.title('Experimental 1')
plt.tight_layout()
plt.savefig('exp1_heatmap.png', dpi=400)

# Adjust the tick label font sizes
ax = plt.gca()
ax.set_xticklabels(ax.get_xticklabels(), ha='right', fontsize=8)
ax.set_yticklabels(ax.get_yticklabels(), ha='right', fontsize=8)

# Experimental 2 group heatmap
plt.figure(figsize=(8, 8))
sns.heatmap(exp2_lower_triangle, cmap='coolwarm', annot=False, vmin=-1, vmax=1, mask=np.zeros_like(exp2_lower_triangle, dtype=np.bool), square=True, xticklabels=dependent_variables, yticklabels=dependent_variables)
plt.title('Experimental 2')
plt.tight_layout()
plt.savefig('exp2_heatmap.png', dpi=400)

# Adjust the tick label font sizes
ax = plt.gca()
ax.set_xticklabels(ax.get_xticklabels(), ha='right', fontsize=8)
ax.set_yticklabels(ax.get_yticklabels(), ha='right', fontsize=8)

plt.show()

# Define the significance level
alpha = 0.05

# Define empty lists to store the positive and negative correlations for each group
control_positive_correlations = []
control_negative_correlations = []
exp1_positive_correlations = []
exp1_negative_correlations = []
exp2_positive_correlations = []
exp2_negative_correlations = []

# Loop through each pairwise combination of dependent variables
for i,j in combinations(range(len(dependent_variables)),2):

    # Control group
    control_corr_coef,control_p_value = spearmanr(control_data[dependent_variables[i]],
                                                  control_data[dependent_variables[j]])
    if control_corr_coef > 0 and control_p_value < alpha:
        control_positive_correlations.append(
            f'{dependent_variables[i]} vs {dependent_variables[j]}: r={control_corr_coef:.2f}, p={control_p_value:.3f}')
    elif control_corr_coef < 0 and control_p_value < alpha:
        control_negative_correlations.append(
            f'{dependent_variables[i]} vs {dependent_variables[j]}: r={control_corr_coef:.2f}, p={control_p_value:.3f}')

    # Experimental 1 group
    exp1_corr_coef,exp1_p_value = spearmanr(exp1_data[dependent_variables[i]],exp1_data[dependent_variables[j]])
    if exp1_corr_coef > 0 and exp1_p_value < alpha:
        exp1_positive_correlations.append(
            f'{dependent_variables[i]} vs {dependent_variables[j]}: r={exp1_corr_coef:.2f}, p={exp1_p_value:.3f}')
    elif exp1_corr_coef < 0 and exp1_p_value < alpha:
        exp1_negative_correlations.append(
            f'{dependent_variables[i]} vs {dependent_variables[j]}: r={exp1_corr_coef:.2f}, p={exp1_p_value:.3f}')

    # Experimental 2 group
    exp2_corr_coef,exp2_p_value = spearmanr(exp2_data[dependent_variables[i]],exp2_data[dependent_variables[j]])
    if exp2_corr_coef > 0 and exp2_p_value < alpha:
        exp2_positive_correlations.append(
            f'{dependent_variables[i]} vs {dependent_variables[j]}: r={exp2_corr_coef:.2f}, p={exp2_p_value:.3f}')
    elif exp2_corr_coef < 0 and exp2_p_value < alpha:
        exp2_negative_correlations.append(
            f'{dependent_variables[i]} vs {dependent_variables[j]}: r={exp2_corr_coef:.2f}, p={exp2_p_value:.3f}')

# Print the positive and negative correlations for each group
print('Control group:')
print('Positive correlations:')
print('\n'.join(control_positive_correlations))
print('Negative correlations:')
print('\n'.join(control_negative_correlations))

print('\nExperimental 1 group:')
print('Positive correlations:')
print('\n'.join(exp1_positive_correlations))
print('Negative correlations:')
print('\n'.join(exp1_negative_correlations))

print('\nExperimental 2 group:')
print('Positive correlations:')
print('\n'.join(exp2_positive_correlations))
print('Negative correlations:')
print('\n'.join(exp2_negative_correlations))
