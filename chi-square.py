# Create a new dataframe for the chi-square results
chi_square_results = pd.DataFrame(columns=['Variable','Chi-square','P-value', 'Significance'])

# Loop through each dependent variable
for var in dependent_variables:
    # Create a contingency table of the data for this variable and the "Group" column
    contingency_table = pd.crosstab(data[var],data['Group'])

    # Calculate the chi-square test statistic and associated p-value
    chi2,p,dof,expected = stats.chi2_contingency(contingency_table)

    # Append the results to the chi_square_results dataframe
    if p < 0.05:
        significance = '*'
    else:
        significance = ''
    chi_square_results = chi_square_results.append({'Variable': var,'Chi-square': chi2,'P-value': p, 'Significance': significance},ignore_index=True)

    # Print the results with asterisks for significant values
    if p < 0.05:
        print(f"{var}: Chi-square = {chi2:.3f}*, p = {p:.3f}")
    else:
        print(f"{var}: Chi-square = {chi2:.3f}, p = {p:.3f}")

    # Calculate the effect size (Cramer's V)
    n = contingency_table.sum().sum()
    phi = np.sqrt(chi2/(n*(min(contingency_table.shape)-1)))
    cramer_v = phi/np.sqrt(min(contingency_table.shape)-1)

    # Append the effect size (Cramer's V) to the chi_square_results dataframe
    chi_square_results.loc[chi_square_results['Variable'] == var, 'Cramer\'s V'] = cramer_v

# Save the results to a CSV file with asterisks for significant values
chi_square_results['Chi-square'] = chi_square_results['Chi-square'].astype(str) + chi_square_results['Significance']
chi_square_results.drop('Significance', axis=1, inplace=True)
chi_square_results.to_csv('chi_square_results.csv', index=False)

# Print the results
print(chi_square_results)