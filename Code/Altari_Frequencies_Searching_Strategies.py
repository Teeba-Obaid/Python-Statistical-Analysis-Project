import pandas as pd
import numpy as np
import altair as alt

# Define the dependent variables as the outcome variables
variable_order = [
    'No action',
    'No new comparative trial',
    'New comparative trial',
    'Prediction Current: same rule',
    'Prediction Voltage Drop: same rule',
    'Prediction Current: Fill up gaps',
    'Prediction Voltage Drop: Fill up gaps',
    'Confidence Current: verify prediction',
    'Confidence Voltage Drop: verify prediction',
    'Confidence Current: falsify prediction',
    'Confidence Voltage Drop: falsify prediction',
    'Rule Current: Confirming Redundancy',
    'Rule Voltage Drop: Confirming Redundancy',
    'Identify problem: goal stated',
    'Rule Current: Simultaneous scanning',
    'Rule Voltage Drop: Simultaneous scanning',
    'Rule Current: Successive scanning',
    'Rule Voltage Drop: Successive scanning',
    'Rule Current: Focus gambling',
    'Rule Voltage Drop: Focus gambling',
    'Rule Current: Conservative Focusing',
    'Rule Voltage Drop: Conservative Focusing',
    'Post-test: Voltage Drop non-normative',
    'Post-test: Current non-normative',
    'Post-test: Current partial',
    'Post-test: Voltage Drop partial',
    'Post-test: Current 1 Valid link',
    'Post-test: Voltage Drop 1 Valid link',
    'Post-test: Current 2 Valid links',
    'Post-test: Voltage Drop 2 Valid links'
]

# Load the data
data = pd.read_csv("data10.csv")

# Create a 'group' column based on the order of the data
data['group'] = ['control'] * 20 + ['experimental 1'] * 20 + ['experimental 2'] * 20

# Melt the data to make it long-form, which works better for Altair
melted_data = pd.melt(data, id_vars='group', value_vars=variable_order)

# Group the data by group and variable, then sum the values
grouped_data = melted_data.groupby(['group', 'variable'])['value'].sum().reset_index(name='sum')

# Change variable column into categorical with defined order
grouped_data['variable'] = pd.Categorical(grouped_data['variable'], categories=variable_order, ordered=True)

# Map each group to a color
color_scale = alt.Scale(domain=['control', 'experimental 1', 'experimental 2'],
                        range=['blue', 'red', 'orange'])
# Create the chart
chart = alt.Chart(grouped_data).mark_line(point=True).encode(
    x=alt.X(
        'variable:N',
        title='Variable',
        sort=variable_order,
        axis=alt.Axis(
            labelAngle=90,
            labelFontSize=14,
            labelLimit=800,
            grid=True,
            titleY=300
        )
    ),
    y=alt.Y(
        'sum:Q',
        title='Sum',
        axis=alt.Axis(
            labelFontSize=14)),  # Increase the y-axis labelFontSize


    color=alt.Color('group:N', scale=color_scale, title='Group'),
    tooltip=['variable', 'sum', 'group']
).properties(
    title={
        "text": ['Sum of Frequencies for Different Variables for each Group'],
        "subtitle": ['Search Strategies'],
        "fontSize": 20,
        "fontWeight": 'bold'
    },
    width=800,
    height=400
)

# Configure the legend title font size
chart = chart.configure_legend(
    titleFontSize=14,  # Increase the legend title font size for 'Magnitude of Correlation' and 'Effect Size'
    labelFontSize=16  # Increase the legend label font size
)

# Interactive, so the tooltip works
chart = chart.interactive()

# Save chart to HTML file
chart.save('chart.html')

# Convert chart to JSON and print
chart_json = chart.to_json()
print(chart_json)