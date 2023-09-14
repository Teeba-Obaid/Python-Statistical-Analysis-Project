import pandas as pd
import numpy as np
import altair as alt

# Define the dependent variables as the outcome variables
variable_order = [
    'No action',
    '1 bulbs equal',
    '2 bulbs equal',
    '1 vs. 2 bulbs different',
    'Battery voltage equal',
    'Battery voltage different',
    'Resistance change: 1 or 2 bulbs',
    'Resistance change: 2 bulbs',
    'Resistance equal: 2 bulbs different value',
    'Resistance equal: 2 or 1 vs. 2 bulbs same value',
    'Resistance equal: 1 bulb',
    'Resistance equal: 2 bulbs different value & position',
    'Ammeter equal: after/before 1 or 2 bulb',
    'Ammeter different: before vs. after 1 or 2 bulbs',
    'Ammeter different: on high/low of 2 bulb',
    'Voltmeter equal: 1 bulb or 2 bulbs or battery',
    'Voltmeter equal: 2 bulbs',
    'Voltmeter different: high vs. low resistance 2 bulbs',
    'Voltmeter different: high vs. low resistance 2 bulbs vs. battery'
]

# Load the data
data = pd.read_csv("data8.csv")

# Create a 'group' column based on the order of the data
data['group'] = ['control'] * 20 + ['experimental 1'] * 20 + ['experimental 2'] * 20

# Check the columns in your data
print("Columns in the DataFrame: \n", data.columns)

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
            titleY=350
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
        "subtitle": ['Engineering Approaches'],
        "fontSize": 20,
        "fontWeight": 'bold'
    },
    width=600,
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