import pandas as pd
import numpy as np
import scikit_posthocs as sp
import altair as alt
from scipy.stats import spearmanr, ranksums

# Load the data
data = pd.read_csv("data10.csv")

# Create a 'group' column based on the order of the data
data['group'] = ['control' if i < 20 else 'experimental 2' if 40 <= i < 60 else 'ignore' for i in range(len(data))]

# Filter out the 'ignore' group
data = data[data['group'] != 'ignore']
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
data['group'] = ['control' if i < 20 else 'experimental 2' if 40 <= i < 60 else 'ignore' for i in range(len(data))]

# Filter out the 'ignore' group
data = data[data['group'] != 'ignore']

# Split the data into groups
control = data.loc[data['group'] == 'control', :]
exp2 = data.loc[data['group'] == 'experimental 2', :]

results = []

# For each variable, calculate the rank-biserial correlation in addition to Dunn's test and Spearman's correlation
for column in dependent_variables:
    # Perform Dunn's test
    dunn_data = pd.melt(data, id_vars='group', value_vars=column)
    p_values = sp.posthoc_dunn(dunn_data, val_col='value', group_col='group', p_adjust='holm').values

    # Calculate Spearman's correlations
    try:
        rho_control_exp2, _ = spearmanr(control[column], exp2[column])
    except ValueError:
        rho_control_exp2 = np.nan

    # Calculate rank-biserial correlations
    zscore_control_exp2, U_control_exp2 = ranksums(control[column], exp2[column])
    r_control_exp2 = 1 - 2 * U_control_exp2 / (len(control) * len(exp2))

    # Change the p_adjust parameter to 'fdr_bh' to use the Benjamini-Hochberg procedure
    p_values = sp.posthoc_dunn(dunn_data,val_col='value',group_col='group',p_adjust='fdr_bh').values

    # Recompute the significance based on the adjusted p-value
    significance = 'Significant' if p_values[0,1] < 0.05 else 'Non-significant'

    # Determine the strength of correlation
    abs_corr = abs(rho_control_exp2)
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
    results.append({
        'Variable': column,
        'Comparison': 'Control vs. Experimental 2',
        'P-value': (p_values[0,1]),
        'Z-score': (zscore_control_exp2),
        'Correlation': (abs(rho_control_exp2)),
        'Correlation Sign': 'Negative' if rho_control_exp2 < 0 else 'Positive',
        'Correlation Strength': corr_strength,
        'Effect Size': (r_control_exp2),
        'Significance': significance
    })

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Print the results of Dunn's test for significant p-values
print(df)

# Save the results of Dunn's test for significant p-values to an Excel file
df.to_excel("Dunn's test_Control_Experimental2.xlsx", index=False)

# Update the encoding part of your chart definition
chart = alt.Chart(df).mark_circle().encode(
    x=alt.X('Variable:N', title='Variable Name', sort=dependent_variables,
            axis=alt.Axis(labelAngle=90, labelFontSize=18, labelLimit=800, grid=True, titleY=360)),
    y=alt.Y('P-value:Q', title='P-value', scale=alt.Scale(type='log', base=10),
            axis=alt.Axis(labelFontSize=16)),
    color=alt.Color('Correlation Sign:N',
                    scale=alt.Scale(domain=['Negative','Positive'], range=['blue','red']),
                    legend=alt.Legend(titleFontSize=16, labelFontSize=18, titleLimit=400, labelLimit=200)),
    size=alt.Size('Correlation:Q', title='Correlation Magnitude', scale=alt.Scale(range=[100,1000])),
    opacity=alt.Opacity('Effect Size:Q', title='Effect Size', scale=alt.Scale(range=[0.2,1.0])),
    tooltip=['Variable','Comparison','Correlation','Correlation Sign','P-value','Effect Size']
).properties(
    title={
        "text": ['P-values from Dunn\'s test between Control Group vs. Experimental 2 Group for Different Variables'],
        "subtitle": ['Correlation test used: Spearman\'s rho',
                     'Effect size test used: Rank-Biserial Correlation']
    },
    width=880,
    height=400
)

dashed_line = alt.Chart(pd.DataFrame({'y': [0.05]})).mark_rule(color='black', strokeDash=[3,3], opacity=0.7).encode(y='y:Q')

# Annotation for the dashed line
annotation = alt.Chart(pd.DataFrame({
    'y': [0.05],
    'text': ['0.05']
})).mark_text(align='right', dx=-399, dy=-8, fontSize=16).encode(
    y='y:Q',
    text='text'
)

combined_chart = chart + dashed_line + annotation

# Configure the legend title font size
combined_chart = combined_chart.configure_legend(
    titleFontSize=14,  # Increase the legend title font size for 'Magnitude of Correlation' and 'Effect Size'
    labelFontSize=16  # Increase the legend label font size
)

# Configure the title font size and weight
combined_chart = combined_chart.configure_title(
    fontSize=16,  # Increase the title font size
    fontWeight='bold'  # Set the font weight to bold
)

# Interactive, so the tooltip works
combined_chart = combined_chart.interactive()

# Save chart to HTML file
combined_chart.save('chart.html')

# Convert chart to JSON and print
chart_json = combined_chart.to_json()
print(chart_json)
