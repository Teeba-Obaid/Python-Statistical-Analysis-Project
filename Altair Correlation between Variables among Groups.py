import pandas as pd
import numpy as np
import scikit_posthocs as sp
import altair as alt
from scipy.stats import spearmanr

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
# [Your 'dependent_variables' list stays as it is.]

# Load the data
data = pd.read_csv("data10.csv")

# Create a 'group' column based on the order of the data
data['group'] = ['control'] * 20 + ['experimental 1'] * 20 + ['experimental 2'] * 20

# Split the data into groups
control = data.loc[data['group'] == 'control', :]
exp1 = data.loc[data['group'] == 'experimental 1', :]
exp2 = data.loc[data['group'] == 'experimental 2', :]

results = []
# Perform Dunn's test and Spearman's correlation for each variable
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

    # Store the results
    results.extend([
        {'Variable': column, 'Comparison': 'Control vs. Experimental 1', 'P-value': p_values[0, 1], 'Correlation': rho_control_exp1},
        {'Variable': column, 'Comparison': 'Control vs. Experimental 2', 'P-value': p_values[0, 2], 'Correlation': rho_control_exp2},
        {'Variable': column, 'Comparison': 'Experimental 1 vs. Experimental 2', 'P-value': p_values[1, 2], 'Correlation': rho_exp1_exp2}
    ])

# Create a DataFrame from the results
df = pd.DataFrame(results)
# Print the DataFrame before filtering for significant results
print(df)

# Filter the DataFrame for significant results
df = df[df['P-value'] < 0.05]

# Create an Altair chart
chart = alt.Chart(df).mark_circle().encode(
    x=alt.X('Variable:N', title='Variable Name', sort=dependent_variables, axis=alt.Axis(labelAngle=-90, labelFontSize=10, labelLimit=800, grid=True)),  # Adjust label angle, font size, label limit, and add grid lines here
    y=alt.Y('Correlation:Q', title='Correlation', scale=alt.Scale(domain=[-1, 1])),
    color=alt.Color('Comparison:N', scale=alt.Scale(domain=['Control vs. Experimental 1', 'Control vs. Experimental 2', 'Experimental 1 vs. Experimental 2'], range=['red', 'green', 'blue'])),
    size=alt.Size('Correlation:Q', title='Magnitude of Correlation'),
    tooltip=['Variable', 'Comparison', 'Correlation', 'P-value']
).properties(
    title='Correlations between Variables for Different Groups',
    width=800,  # Increase the width of the chart if necessary
    height=400  # Increase the height of the chart if necessary
)

# Interactive, so the tooltip works
chart = chart.interactive()

# Save chart to HTML file
chart.save('chart.html')

# Convert chart to JSON and print
chart_json = chart.to_json()
print(chart_json)

