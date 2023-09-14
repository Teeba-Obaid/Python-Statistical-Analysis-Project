import numpy as np
import scipy.stats as stats
import pandas as pd
from scipy.stats import shapiro
import matplotlib.pyplot as plt


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
print(data['Group'].dtype)

data['Group'] = data['Group'].astype(str)


# Define the dependent variables as the outcome variables
dependent_variables = data.columns[1:]

# Loop over each dependent variable and perform Kruskal-Wallis
for dependent_variable in dependent_variables:
    print(f'\nResults for {dependent_variable}:')

    # Split the data into control and experimental groups
    control = data.loc[data['Group'] == 'Control', dependent_variable]
    exp1 = data.loc[data['Group'] == 'Experimental 1', dependent_variable]
    exp2 = data.loc[data['Group'] == 'Experimental 2', dependent_variable]

    # Calculate the Kruskal-Wallis test statistic and p-value
    kruskal_stat, p_value = stats.kruskal(control, exp1, exp2)

    # Print Kruskal-Wallis table
    print("Kruskal-Wallis Table")
    print("Source\t\tTest Statistic\tDegrees of Freedom\tP-value")
    print(f"{sources_of_variation[0]}\t\t{kruskal_stat:.4f}\t\t{len(data['Group'].unique())-1}\t\t{p_value:.4f}")

    if p_value < 0.05:
        print(f"The {dependent_variable} shows a significant difference between groups.")
    else:
        print(f"The {dependent_variable} does not show a significant difference between groups.")

    # Plot a box plot of the data
    fig, ax = plt.subplots()
    ax.boxplot([control, exp1, exp2])
    ax.set_xticklabels(['Control', 'Experimental 1', 'Experimental 2'])
    ax.set_ylabel(dependent_variable)
    ax.set_title(f'{dependent_variable} Box Plot')
    plt.show()

    # Perform Shapiro-Wilk test for normality of residuals
    shapiro_test = shapiro(data[dependent_variable])
    print(f'Shapiro-Wilk test for normality of residuals: W = {shapiro_test[0]:.4f}, p-value = {shapiro_test[1]:.4f}')

    if shapiro_test[1] < 0.05:
        print("The residuals are not normally distributed.")
    else:
        print("The residuals are normally distributed.")

# Perform Friedman test (repeated measures Kruskal-Wallis)
f_stat, p_val = stats.friedmanchisquare(data.iloc[:, 1:11], data.iloc[:, 11:21], data.iloc[:, 21:31])
print("\nFriedman Test Results")
print(f"Test Statistic: {f_stat:.4f}")
print(f"P-value: {p_val:.4f}")
if p_val < 0.05:
    print("There is a significant difference between the groups.")
else:
    print("There is not a significant difference between the groups.")