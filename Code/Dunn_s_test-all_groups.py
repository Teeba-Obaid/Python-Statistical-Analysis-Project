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
data['group'] = ['control' if i < 20 else 'experiment 1' if 20 <= i < 40 else 'experiment 2' for i in range(len(data))]

# Split the data into groups
control = data.loc[data['group'] == 'control', :]
exp1 = data.loc[data['group'] == 'experiment 1', :]
exp2 = data.loc[data['group'] == 'experiment 2', :]

# Update the groups assignment with standardized shape and color names
groups = [('control',control,'experiment 1',exp1),
          ('control',control,'experiment 2',exp2),
          ('experiment 1',exp1,'experiment 2',exp2)]

results = []

for group_name1, group1, group_name2, group2 in groups:
    for column in dependent_variables:

        # Perform Dunn's test
        dunn_data = pd.concat([group1[['group', column]], group2[['group', column]]])
        p_values = sp.posthoc_dunn(dunn_data,val_col=column,group_col='group',p_adjust='holm').values

        # Calculate Spearman's correlations
        try:
            rho,_ = spearmanr(group1[column], group2[column])
        except ValueError:
            rho = np.nan

        # Calculate rank-biserial correlations
        zscore, U = ranksums(group1[column], group2[column])
        r = 1 - 2 * U / (len(group1) * len(group2))

        # Determine the significance of the p-value
        significance = 'Significant' if p_values[0, 1] < 0.05 else 'Non-significant'

        # Determine the strength of correlation
        abs_corr = abs(rho)
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
            'Comparison': f'{group_name1} vs. {group_name2}',
            'P-value': p_values[0,1],
            'Z-score': zscore,
            'Correlation': abs(rho),
            'Correlation Sign': 'Negative' if rho < 0 else 'Positive',
            'Correlation Strength': corr_strength,
            'Effect Size': r,
            'Significance': significance
        })

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Print the results of Dunn's test for significant p-values
print(df)

# Save the results of Dunn's test for significant p-values to an Excel file
df.to_excel("Dunn's test_Control_Experiment1.xlsx", index=False)


# Adjust the visualization to show different markers and colors
chart = alt.Chart(df).mark_point().encode(
    x=alt.X('Variable:N', title='Variable Name', sort=dependent_variables,
            axis=alt.Axis(labelAngle=90, labelFontSize=16, labelLimit=800, grid=True, titleY=330)),
    y=alt.Y('P-value:Q', title='P-value', scale=alt.Scale(type='log', base=10),
            axis=alt.Axis(labelFontSize=16)),
    color=alt.Color('Comparison:N',
                    scale=alt.Scale(domain=['control vs. experiment 1',
                                            'control vs. experiment 2',
                                            'experiment 1 vs. experiment 2'],
                                    range=['red','green','blue']),
                    legend=alt.Legend(title="Comparison", titleFontSize=14, labelFontSize=14, titleLimit=400,
                                      labelLimit=200)),
    size=alt.Size('Correlation:Q', title='Magnitude of Correlation', scale=alt.Scale(range=[500, 1000])),
    opacity=alt.Opacity('Effect Size:Q', title='Effect Size', scale=alt.Scale(range=[0.2, 1.0])),
    shape=alt.Shape('Comparison:N',
                    scale=alt.Scale(domain=['control vs. experiment 1',
                                            'control vs. experiment 2',
                                            'experiment 1 vs. experiment 2'],
                                    range=['circle','triangle-up','square'])),
    tooltip=['Variable', 'Comparison', 'Correlation', 'Correlation Sign', 'P-value', 'Effect Size']
).properties(
    title={
        "text": ['P-values from Dunn\'s test between Groups for Different Variables'],
        "subtitle": ['Correlation test used: Spearman\'s rho',
                     'Effect size test used: Rank-Biserial Correlation']
    },
    width=900,
    height=400
)

# Configure the legend title font size
chart = chart.configure_legend(
    titleFontSize=14,  # Increase the legend title font size for 'Magnitude of Correlation' and 'Effect Size'
    labelFontSize=16  # Increase the legend label font size
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

