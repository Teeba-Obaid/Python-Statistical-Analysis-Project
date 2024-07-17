import pandas as pd
import numpy as np
import scikit_posthocs as sp
import altair as alt
from scipy.stats import spearmanr, ranksums

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
control = data.loc[data['group'] == 'control', :]
exp1 = data.loc[data['group'] == 'experimental 1', :]
exp2 = data.loc[data['group'] == 'experimental 2', :]

results = []

# For each variable, calculate the rank-biserial correlation in addition to Dunn's test and Spearman's correlation
for column in dependent_variables:
    # Perform Dunn's test
    dunn_data = pd.melt(data, id_vars='group', value_vars=column)
    p_values = sp.posthoc_dunn(dunn_data, val_col='value', group_col='group', p_adjust='holm').values

    # Calculate Spearman's correlations
    try:
        rho_control_exp1, _ = spearmanr(control[column], exp1[column])
    except ValueError:
        rho_control_exp1 = np.nan
    try:
        rho_control_exp2, _ = spearmanr(control[column], exp2[column])
    except ValueError:
        rho_control_exp2 = np.nan
    try:
        rho_exp1_exp2, _ = spearmanr(exp1[column], exp2[column])
    except ValueError:
        rho_exp1_exp2 = np.nan

    # Calculate rank-biserial correlations
    zscore_control_exp1,U_control_exp1 = ranksums(control[column],exp1[column])
    zscore_control_exp2,U_control_exp2 = ranksums(control[column],exp2[column])
    zscore_exp1_exp2,U_exp1_exp2 = ranksums(exp1[column],exp2[column])
    U_control_exp1, _ = ranksums(control[column], exp1[column])
    r_control_exp1 = 1 - 2 * U_control_exp1 / (len(control) * len(exp1))
    U_control_exp2, _ = ranksums(control[column], exp2[column])
    r_control_exp2 = 1 - 2 * U_control_exp2 / (len(control) * len(exp2))
    U_exp1_exp2, _ = ranksums(exp1[column], exp2[column])
    r_exp1_exp2 = 1 - 2 * U_exp1_exp2 / (len(exp1) * len(exp2))

    # Determine the significance of the p-value
    significance = 'Significant' if p_values[0,1] < 0.05 else 'Non-significant'

    # Determine the strength of correlation
    abs_corr = abs(rho_control_exp1)
    if abs_corr <= 0.19:
        corr_strength = 'Very Weak'
    elif abs_corr <= 0.39:
        corr_strength = 'Weak'
    elif abs_corr <= 0.59:
        corr_strength = 'Moderate'
    elif abs_corr <= 0.79:
        corr_strength = 'Strong'
    else:
        corr_strength = 'Very Strong'

    # Store the results
    results.extend([
        {'Variable': column, 'Comparison': 'Control vs. Experimental 1', 'P-value': p_values[0, 1], 'Correlation': rho_control_exp1, 'Effect Size': r_control_exp1},
        {'Variable': column, 'Comparison': 'Control vs. Experimental 2', 'P-value': p_values[0, 2], 'Correlation': rho_control_exp2, 'Effect Size': r_control_exp2},
        {'Variable': column, 'Comparison': 'Experimental 1 vs. Experimental 2', 'P-value': p_values[1, 2], 'Correlation': rho_exp1_exp2, 'Effect Size': r_exp1_exp2}
    ])
# Create a DataFrame from the results
df = pd.DataFrame(results)

# Create an Altair chart
chart = alt.Chart(df).mark_point().encode(
    x=alt.X('Variable:N', title='Variable Name', sort=dependent_variables,
            axis=alt.Axis(labelAngle=90, labelFontSize=14, labelLimit=800, grid=True, titleY=300)),
    y=alt.Y('P-value:Q', title='P-value', scale=alt.Scale(type='log', base=10),
            axis=alt.Axis(labelFontSize=14)),
    color=alt.Color('Comparison:N',
                    scale=alt.Scale(domain=['Control vs. Experimental 1',
                                            'Control vs. Experimental 2',
                                            'Experimental 1 vs. Experimental 2'],
                                    range=['red', 'green', 'blue'])),
    shape=alt.Shape('Comparison:N', scale=alt.Scale(range=['circle', 'triangle', 'square'])),
    size=alt.Size('Correlation:Q', title='Magnitude of Correlation', scale=alt.Scale(range=[100, 1000])),
    opacity=alt.Opacity('Effect Size:Q', title='Effect Size', scale=alt.Scale(range=[0.2, 1.0])),
    tooltip=['Variable', 'Comparison', 'Correlation', 'P-value', 'Effect Size'],
).properties(
    title={
        "text": ['P-values from Dunn\'s test between Groups for Different Variables'],
        "subtitle": ['Correlation test used: Spearman\'s rho',
                     'Effect size test used: Rank-Biserial Correlation']
    },
    width=800,
    height=400
)

# Configure the legend title font size
chart = chart.configure_legend(
    titleFontSize=14,  # Increase the legend title font size for 'Magnitude of Correlation' and 'Effect Size'
    labelFontSize=14  # Increase the legend label font size
)

# Configure the title font size and weight
chart = chart.configure_title(
    fontSize=16,  # Increase the title font size
    fontWeight='bold'  # Set the font weight to bold
)


# Interactive, so the tooltip works
chart = chart.interactive()

# Save chart to HTML file
chart.save('chart.html')

# Convert chart to JSON and print
chart_json = chart.to_json()
print(chart_json)

