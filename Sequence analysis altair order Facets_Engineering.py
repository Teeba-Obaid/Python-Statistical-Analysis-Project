import re
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Create a dictionary without the trial numbers in the keys
code_dict = {
    "EB1": "1 bulb equal",
    "EB2": "2 bulbs equal",
    "DB": "1 vs. 2 bulbs different",
    "BVE": "Battery voltage equal",
    "BVD": "Battery voltage different",
    "RID": "Resistance change: 1 or 2 bulbs",
    "RI2": "Resistance change: 2 bulbs",
    "RE2D": "Resistance equal: 2 bulbs different value",
    "RE2S": "Resistance equal: 2 or 1 vs. 2 bulbs same value",
    "RE1": "Resistance equal: 1 bulb",
    "RE2DP": "Resistance equal: 2 bulbs different value & position",
    "AE": "Ammeter equal: after/before 1 or 2 bulb",
    "ADBA": "Ammeter different: before vs. after 1 or 2 bulbs",
    "ADHL": "Ammeter different: on high/low of 2 bulb",
    "VE": "Voltmeter equal: 1 bulb or 2 bulbs or battery",
    "VEHL2": "Voltmeter equal: 2 bulbs",
    "VDHL2": "Voltmeter different: high vs. low resistance 2 bulbs",
    "VDHL2B": "Voltmeter different: high vs. low resistance 2 bulbs vs. battery"
}

def transform_code_to_sentence(code):
    # Separate the text and number parts of the code
    match = re.match(r"(T[0-9]+)([A-Z0-9]+)", code, re.I)
    if match:
        items = match.groups()
    else:
        return f"Code {code} not found in the dictionary."

    # Get the corresponding sentence for the text part of the code
    sentence = code_dict.get(items[1], f"Code {items[1]} not found in the dictionary.")

    # Append the trial number part in parentheses
    return f"{sentence} ({items[0]})"

def create_table_from_codes(cluster_number, codes_string):
    codes = codes_string.split(',')
    sentences = [transform_code_to_sentence(code) for code in codes]
    data = [{'cluster': f"Cluster {cluster_number}", 'code': code, 'variables': sentence, 'order': i+1} for i, (code, sentence) in enumerate(zip(codes, sentences))]
    df = pd.DataFrame(data)
    return df

clusters = {
    1: "T1EB1,T1BVE,T1BVD,T1RE1,T1AE,T1VE",
    2: "T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB2,T2BVE,T2RE1,T2AE,T2VE",
    3: "T1EB1,T1BVD,T1BVE,T1AE,T1VE,T2EB1,T2BVE,T2RE1,T2AE,T2VE,T3EB1,T3BVE,T3RE1,T3ADBA,T3VE,T4EB1,T4BVE,T4RE1,T4ADBA,T4VE,T5EB2,T5BVE,T5RE2S,T5AE,T5VE",
    4: "T1DB,T1BVE,T1RE1,T1AE,T1VE,T2EB2,T2BVE,T2RE2D,T2ADBA,T2VE,T3EB2,T3BVE,T3RE2D,T3ADHL,T3VDHL2",
    5: "T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB1,T2BVE,T2RE1,T2AE,T2VE,T3EB2,T3BVE,T3RE2D,T3AE,T3VE,T4EB2,T4BVE,T4RE2D,T4ADBA,T4VE"
}

# Concatenate the dataframes for all clusters
df = pd.concat([create_table_from_codes(cluster, codes) for cluster, codes in clusters.items()], ignore_index=True)
print(df)

# Define sentence_order
sentence_order = [
    '1 bulb equal (T1)',
    '1 vs. 2 bulbs different (T1)',
    'Battery voltage equal (T1)',
    'Battery voltage different (T1)',
    'Resistance equal: 1 bulb (T1)',
    'Resistance change: 1 or 2 bulbs (T1)',
    'Ammeter equal: after/before 1 or 2 bulb (T1)',
    'Ammeter different: before vs. after 1 or 2 bulbs (T1)',
    'Voltmeter equal: 1 bulb or 2 bulbs or battery (T1)',
    '1 bulb equal (T2)',
    '2 bulbs equal (T2)',
    'Battery voltage equal (T2)',
    'Resistance equal: 1 bulb (T2)',
    'Resistance equal: 2 bulbs different value (T2)',
    'Ammeter equal: after/before 1 or 2 bulb (T2)',
    'Ammeter different: before vs. after 1 or 2 bulbs (T2)',
    'Voltmeter equal: 1 bulb or 2 bulbs or battery (T2)',
    '1 bulb equal (T3)',
    '2 bulbs equal (T3)',
    'Battery voltage equal (T3)',
    'Resistance equal: 1 bulb (T3)',
    'Resistance equal: 2 bulbs different value (T3)',
    'Ammeter equal: after/before 1 or 2 bulb (T3)',
    'Ammeter different: before vs. after 1 or 2 bulbs (T3)',
    'Ammeter different: on high/low of 2 bulb (T3)',
    'Voltmeter equal: 1 bulb or 2 bulbs or battery (T3)',
    'Voltmeter different: high vs. low resistance 2 bulbs (T3)',
    '1 bulb equal (T4)',
    '2 bulbs equal (T4)',
    'Battery voltage equal (T4)',
    'Resistance equal: 1 bulb (T4)',
    'Resistance equal: 2 bulbs different value (T4)',
    'Ammeter different: before vs. after 1 or 2 bulbs (T4)',
    'Voltmeter equal: 1 bulb or 2 bulbs or battery (T4)',
    '2 bulbs equal (T5)',
    'Battery voltage equal (T5)',
    'Resistance equal: 2 or 1 vs. 2 bulbs same value (T5)',
    'Ammeter equal: after/before 1 or 2 bulb (T5)',
    'Voltmeter equal: 1 bulb or 2 bulbs or battery (T5)'
]

# Reverse the order of sentence_order
sentence_order_reversed = sentence_order[::-1]

# Define the color palette
color_palette = alt.Scale(domain=['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5'],
                          range=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])

# Define the shape palette
shape_palette = alt.Scale(domain=['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5'],
                          range=['circle', 'square', 'cross', 'diamond', 'triangle-down'])

# Define the unique sentences
unique_sentences = df['variables'].unique().tolist()


# Create the facet charts with grid lines only for data points
chart1 = alt.Chart(df[df['cluster'] == 'Cluster 1']).mark_point(filled=True, size=200).encode(
    x=alt.X('order', axis=alt.Axis(grid=True)),
    y=alt.Y('variables',
            scale=alt.Scale(domain=sentence_order),  # Adjusted domain to sentence_order
            sort=sentence_order_reversed,
            axis=alt.Axis(labelFontSize=16,labelLimit=800,grid=True,titleY=330, titleX=-380)),
    color=alt.Color('cluster:N',scale=color_palette),
    shape=alt.Shape('cluster:N',scale=shape_palette),  # Use shape_palette
    tooltip=['variables']
).properties(
    title='Cluster 1',
    width=500,
    height=600
)

chart2 = alt.Chart(df[df['cluster'] == 'Cluster 2']).mark_point(filled=True, size=200).encode(
    x='order',
    y=alt.Y('variables',title=None,scale=alt.Scale(domain=sentence_order),  # Use sentence_order
            sort=sentence_order_reversed,
            axis=alt.Axis(grid=True,labels=False)),
    color=alt.Color('cluster:N',scale=color_palette),
    shape=alt.Shape('cluster:N',scale=shape_palette),  # Use shape_palette
    tooltip=['variables']
).properties(
    title='Cluster 2',
    width=500,
    height=600
)

chart3 = alt.Chart(df[df['cluster'] == 'Cluster 3']).mark_point(filled=True, size=200).encode(
    x='order',
    y=alt.Y('variables',
            scale=alt.Scale(domain=sentence_order),  # Adjusted domain to sentence_order
            sort=sentence_order_reversed,
            axis=alt.Axis(labelFontSize=16,labelLimit=800,grid=True,titleY=330,titleX=-380)),
    color=alt.Color('cluster:N',scale=color_palette),
    shape=alt.Shape('cluster:N',scale=shape_palette),  # Use shape_palette
    tooltip=['variables']
).properties(
    title='Cluster 3',
    width=500,
    height=600
)

chart4 = alt.Chart(df[df['cluster'] == 'Cluster 4']).mark_point(filled=True, size=200).encode(
    x='order',
    y=alt.Y('variables',title=None,scale=alt.Scale(domain=sentence_order),  # Use sentence_order
            sort=sentence_order_reversed,
            axis=alt.Axis(grid=True,labels=False)),
    color=alt.Color('cluster:N',scale=color_palette),
    shape=alt.Shape('cluster:N',scale=shape_palette),  # Use shape_palette
    tooltip=['variables']
).properties(
    title='Cluster 4',
    width=500,
    height=600
)

# Define the chart for Cluster 5
chart5 = alt.Chart(df[df['cluster'] == 'Cluster 5']).mark_point(filled=True, size=200).encode(
    x='order',
    y=alt.Y('variables',
            scale=alt.Scale(domain=sentence_order),  # Adjusted domain to sentence_order
            sort=sentence_order_reversed,
            axis=alt.Axis(labelFontSize=16,labelLimit=800,grid=True,titleY=330,titleX=-380)),
    color=alt.Color('cluster:N',scale=color_palette),
    shape=alt.Shape('cluster:N',scale=shape_palette),  # Use shape_palette
    tooltip=['variables']
).properties(
    title='Cluster 5',
    width=500,
    height=600
)

# Arrange the charts in the specified grid
combined_chart = alt.vconcat(
    alt.hconcat(chart1, chart2),
    alt.hconcat(chart3, chart4),
    chart5  # On its own row
).resolve_scale(y='shared').properties(
    title={
      "text": 'K-Means Clustering of Engineering Approaches: Median String Sequences',
      "subtitle": 'Clusters Across Control, Experimental Group 1, and Experimental Group 2',
      "color": "black",
      "subtitleColor": "gray"
    }
)

# Configure the legend title font size
combined_chart = combined_chart.configure_legend(
    titleFontSize=14,  # Increase the legend title font size for 'Magnitude of Correlation' and 'Effect Size'
    labelFontSize=16  # Increase the legend label font size
)

# Configure the title font size and weight
combined_chart = combined_chart.configure_title(
    fontSize=16,  # Increase the title font size
    fontWeight='bold',# Set the font weight to bold
    align="center"
)

# Save the chart as an HTML file
combined_chart.save('facet_chart.html')

# Save charts 1 and 2 together
chart12 = alt.hconcat(chart1, chart2)
chart12.save('charts12.html')

# Save charts 3 and 4 together
chart34 = alt.hconcat(chart3, chart4)
chart34.save('charts34.html')

# Save chart 5 alone
chart5.save('chart5.html')


# Convert chart to JSON and print
combined_chart_json = combined_chart.to_json()
print(combined_chart_json)