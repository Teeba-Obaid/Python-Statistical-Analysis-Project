import numpy as np
import scipy.stats as stats
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import shapiro
import matplotlib.pyplot as plt


# Read the data from the file
data = pd.read_csv('data9.csv', dtype=int)

print(data.columns)

# Create a new column called "Group"
data['Group'] = np.repeat(['Control', 'Experimental 1', 'Experimental 2'], 20)

# Define your sources of variation
sources_of_variation = ['Group']

# Define the dependent variables as the outcome variables
dependent_variables = data.columns[:-1]

# Loop over each dependent variable and perform ANOVA
for dependent_variable in dependent_variables:
    print(f'\nResults for {dependent_variable}:')

    # Split the data into control and experimental groups
    control = data.loc[data['Group'] == 'Control', dependent_variable]
    exp1 = data.loc[data['Group'] == 'Experimental 1', dependent_variable]
    exp2 = data.loc[data['Group'] == 'Experimental 2', dependent_variable]

    # Calculate the sum of squares for each source of variation
    grand_mean = data[dependent_variable].mean()
    group_means = data.groupby('Group')[dependent_variable].mean()
    ss_group = np.sum((group_means - grand_mean) ** 2 * data.groupby('Group').size())
    df_group = len(group_means) - 1
    ms_group = ss_group / df_group

    # Calculate sum of squares for error (within groups)
    ss_total = np.sum((data[dependent_variable] - grand_mean) ** 2)
    df_total = len(data) - 1
    df_error = df_total - df_group
    ss_error = ss_total - ss_group
    ms_error = ss_error / df_error
    ms_group = ss_group / df_group

    # Calculate F statistics and p-values for each source of variation
    f_stats = ms_group / ms_error
    p_values = 1 - stats.f.cdf(f_stats, df_group, df_error)

    # Print ANOVA table
    print("ANOVA Table")
    print("Source\t\tSum of Squares\tDegrees of Freedom\tMean Squares\tF\t\tP-value")
    print(f"{sources_of_variation[0]}\t\t{ss_group}\t\t{df_group}\t\t{ms_group}\t{f_stats}\t{p_values}")
    print(f"Error\t\t{ss_error}\t\t{df_error}\t\t{ms_error}")

    # Perform Tukey's HSD test for pairwise comparisons
    mc = pairwise_tukeyhsd(endog=data[dependent_variable], groups=data['Group'], alpha=0.05)
    print(mc)

    # Perform OLS regression to obtain model summary and diagnostics
    model = ols(f'{dependent_variable} ~ C(Group)',data=data).fit()
    print(model.summary())

    # Plot the residuals against the fitted values
    residuals = model.resid
    fitted_values = model.fittedvalues
    fig, ax = plt.subplots()
    ax.scatter(fitted_values, residuals)
    ax.set_xlabel('Fitted Values')
    ax.set_ylabel('Residuals')
    ax.set_title(f'{dependent_variable} Residuals vs Fitted Values')
    plt.show()

    # Perform Shapiro-Wilk
    shapiro_test = shapiro(residuals)
    print(f'Shapiro-Wilk test for normality of residuals: W = {shapiro_test[0]:.4f}, p-value = {shapiro_test[1]:.4f}')

    if shapiro_test[1] < 0.05:
        print("The residuals are not normally distributed.")
    else:
        print("The residuals are normally distributed.")

    # Plot a histogram of the residuals
    fig,ax = plt.subplots()
    ax.hist(residuals,bins=20)
    ax.set_xlabel('Residuals')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{dependent_variable} Residuals Histogram')
    plt.show()
