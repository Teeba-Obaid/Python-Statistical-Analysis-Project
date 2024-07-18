import os

# Suppress the OutdatedPackageWarning
os.environ['OUTDATED_IGNORE'] = '1'

import pandas as pd
import numpy as np
import altair as alt
from scipy.stats import spearmanr, mannwhitneyu
from pingouin import compute_effsize
from scipy.stats import wilcoxon


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
data = pd.read_csv("data10.csv")

# Create a 'group' column based on the order of the data
data['group'] = ['control'] * 20 + ['experimental 1'] * 20 + ['experimental 2'] * 20

# Split the data into groups
groups = {
    'control': data.loc[data['group'] == 'control', :],
    'experimental 1': data.loc[data['group'] == 'experimental 1', :],
    'experimental 2': data.loc[data['group'] == 'experimental 2', :]
}

# Function to perform the tests
def perform_within_group_tests(group, dependent_variables):
    results = []
    # Loop through the dependent variables
    for i, var1 in enumerate(dependent_variables):
        for j, var2 in enumerate(dependent_variables):
            # Skip if the same variable or if this pair has been computed before
            if i >= j:
                continue
            # Check if variables are constant
            if np.all(group[var1] == group[var1].iloc[0]) or np.all(group[var2] == group[var2].iloc[0]):
                correlation, corr_pvalue, mwu_pvalue, effect_size = np.nan, np.nan, np.nan, np.nan
            else:
                # Compute correlation using Spearman's rho
                correlation, corr_pvalue = spearmanr(group[var1], group[var2])
                # Compute Mann-Whitney U test
                _, mwu_pvalue = mannwhitneyu(group[var1], group[var2], alternative='two-sided')
                # Compute effect size based on the Mann-Whitney U test
                effect_size = compute_effsize(group[var1],group[var2],eftype='r')

            # Append the results
            results.append({
                'variable1': var1,
                'variable2': var2,
                'correlation': correlation,
                'corr_pvalue': corr_pvalue,
                'mannwhitneyu_pvalue': mwu_pvalue,
                'effect_size': effect_size
            })

    return pd.DataFrame(results)

# Apply the function to each group and generate a heatmap for each
for group_name,group_data in groups.items():
    results = perform_within_group_tests(group_data,dependent_variables)

    matrix_pvalues = results.pivot(
        index='variable1',
        columns='variable2',
        values='mannwhitneyu_pvalue'
    )
    matrix_effect_sizes = results.pivot(
        index='variable1',
        columns='variable2',
        values='effect_size'
    )
    matrix_correlation = results.pivot(
        index='variable1',
        columns='variable2',
        values='correlation'
    )

    # Filter out the lower triangle values for p-values and correlations
    mask_pvalues = np.tril(np.ones_like(matrix_pvalues,dtype=bool))
    mask_correlation = np.tril(np.ones_like(matrix_correlation,dtype=bool))

    np.fill_diagonal(mask_pvalues,False)
    np.fill_diagonal(mask_correlation,False)

    matrix_pvalues = matrix_pvalues.mask(mask_pvalues)
    matrix_correlation = matrix_correlation.mask(mask_correlation)

    # Melt the matrices
    melted_pvalues = matrix_pvalues.reset_index().melt(
        id_vars=['variable1'],
        var_name='variable2',
        value_name='mannwhitneyu_pvalue'
    )
    melted_correlation = matrix_correlation.reset_index().melt(
        id_vars=['variable1'],
        var_name='variable2',
        value_name='correlation'
    )

    # Melt the effect size matrix
    melted_effect_sizes = matrix_effect_sizes.reset_index().melt(
        id_vars=['variable1'],
        var_name='variable2',
        value_name='effect_size'
    )

    # Merge the melted dataframes
    merged_melted = melted_pvalues.merge(
        melted_correlation,
        on=['variable1','variable2'],
        suffixes=('_pvalue','_correlation')
    )

    # Merge the effect sizes into the melted dataframe
    merged_melted = merged_melted.merge(
        melted_effect_sizes,
        on=['variable1','variable2'],
    )

    # Replace np.nan with a large value for 'mannwhitneyu_pvalue' and 'effect_size' in upper triangle and keep NaNs in the lower triangle
    merged_melted.loc[merged_melted['mannwhitneyu_pvalue'].isna() & (
            merged_melted['variable1'] < merged_melted['variable2']),'mannwhitneyu_pvalue'] = 1.1
    merged_melted.loc[merged_melted['effect_size'].isna() & (
            merged_melted['variable1'] < merged_melted['variable2']),'effect_size'] = 1.1

    # Create the heatmap
    heatmap = alt.Chart(merged_melted).mark_rect().encode(
        x=alt.X(
            'variable1:N',
            axis=alt.Axis(labelAngle=90,labelAlign='left',labelFontSize=10,labelLimit=800)
        ),
        y=alt.Y('variable2:N',axis=alt.Axis(labelLimit=800)),
        color=alt.condition(
            alt.datum.mannwhitneyu_pvalue > 1,  # If mannwhitneyu_pvalue is NaN
            alt.value('#d5eaf4'),  # use light blue color
            alt.Color(
                'mannwhitneyu_pvalue:Q',
                scale=alt.Scale(
                    range=['#283655','#4D648D','#b3b7b8','#d8dcd6'],
                    domain=[0,0.05,0.05,1]
                ),
                legend=alt.Legend(title='Mann-Whitney U p-value')
            )
        ),
        tooltip=['variable1','variable2','mannwhitneyu_pvalue','correlation','effect_size'],
    ).properties(
        width=600,
        height=600,
        title=f'Mann-Whitney U p-values and Correlation Heatmap for {group_name} Group'
    )

    # Similarly for the scatterplot, we add another color encoding to handle missing values
    scatterplot = alt.Chart(merged_melted).mark_point().encode(
        x=alt.X('variable1:N',axis=alt.Axis(labelAngle=90,labelAlign='left',labelFontSize=10)),
        y=alt.Y('variable2:N',axis=alt.Axis(labelLimit=800)),
        size=alt.Size('correlation:Q',scale=alt.Scale(domain=[-1,1]),legend=alt.Legend(title='Spearman Correlation')),
        color=alt.condition(
            alt.datum.effect_size > 1,  # If effect_size is NaN
            alt.value('black'),  # use light blue color
            alt.Color('effect_size:Q',scale=alt.Scale(range=["#FFE901","#fd03f5"],domainMid=0),
                      legend=alt.Legend(title='Effect Size')),
        )
    ).transform_filter(
        (alt.datum.correlation != 'NaN') & (alt.datum.effect_size != 'NaN')
    )

    # Combine the heatmap and scatterplot
    combined_chart = (heatmap + scatterplot).resolve_scale(color='independent')

    # Save the chart as an HTML file
    combined_chart.save(f'heatmap_{group_name}.html')

    # Convert the chart to JSON
    chart_json = combined_chart.to_json()

    # Print the JSON
    print(chart_json)
