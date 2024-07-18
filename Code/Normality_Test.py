import numpy as np
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
from scikit_posthocs import posthoc_dunn
from scipy.stats import shapiro
# Define the dependent variables as the outcome variables
dependent_variables = [
    'Post-test: Voltage Drop non-normative',
    'Post-test: Current non-normative',
    'Post-test: Current partial',
    'Post-test: Voltage Drop partial',
    'Post-test: Current 1 Valid link',
    'Post-test: Voltage Drop 1 Valid link',
    'Post-test: Current 2 Valid links',
    'Post-test: Voltage Drop 2 Valid links',
    'No action',
    'No new comparative trial',
    'Prediction Current: same rule',
    'Prediction Voltage Drop: same rule',
    'Confidence Current: verify prediction',
    'Confidence Voltage Drop: verify prediction',
    'Rule Current: Confirming Redundancy',
    'Rule Voltage Drop: Confirming Redundancy',
    'New comparative trial',
    'Prediction Current: Fill up gaps',
    'Prediction Voltage Drop: Fill up gaps',
    'Confidence Current: falsify prediction',
    'Confidence Voltage Drop: falsify prediction',
    'Identify problem: goal stated',
    'Rule Current: Simultaneous scanning',
    'Rule Voltage Drop: Simultaneous scanning',
    'Rule Current: Successive scanning',
    'Rule Voltage Drop: Successive scanning',
    'Rule Current: Focus gambling',
    'Rule Voltage Drop: Focus gambling',
    'Rule Current: Conservative Focusing',
    'Rule Voltage Drop: Conservative Focusing'
]

# Load the data
data = pd.read_csv("data10.csv", header=None)

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

# Perform Shapiro-Wilk normality test and print the non-normal variables
non_normal_vars = []
for var in dependent_variables:
    statistic, p_value = shapiro(data[var])
    if p_value < 0.05:
        non_normal_vars.append(var)
        print(f"Variable {var} is likely non-normal with p-value: {p_value:.4f}")

# If no non-normal variables, print a message
if not non_normal_vars:
    print("All variables appear to be normal.")

# Perform Dunn's test and print the results for each dependent variable
for var in dependent_variables:
    dunn_results = posthoc_dunn(data, val_col=var, group_col='Group')
    print(f"Post-hoc Dunn's test for {var}:")
    print(dunn_results)