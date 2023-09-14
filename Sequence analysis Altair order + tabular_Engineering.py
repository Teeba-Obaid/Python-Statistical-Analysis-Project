import re
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np


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

def transform_string_of_codes(codes_string):
    codes = codes_string.split(',')
    sentences = [transform_code_to_sentence(code) for code in codes]
    return '<br>'.join(sentences)

def create_table_from_codes(cluster_number, codes_string):
    codes = codes_string.split(',')
    sentences = [transform_code_to_sentence(code) for code in codes]
    data = [{'cluster': f"Cluster {cluster_number}", 'sentence': sentence, 'order': i+1} for i, sentence in enumerate(sentences)]
    df = pd.DataFrame(data)
    return df

clusters = {
    1: "T1EB1,T1BVE,T1BVD,T1RE1,T1AE,T1VE",
    2: "T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB2,T2BVE,T2RE1,T2AE,T2VE",
    3: "T1EB1,T1BVD,T1BVE,T1AE,T1VE,T2EB1,T2BVE,T2RE1,T2AE,T2VE,T3EB1,T3BVE,T3RE1,T3ADBA,T3VE,T4EB1,T4BVE,T4RE1,T4ADBA,T4VE,T5EB2,T5BVE,T5RE2S,T5AE,T5VE",
    4: "T1DB,T1BVE,T1RE1,T1AE,T1VE,T2EB2,T2BVE,T2RE2D,T2ADBA,T2VE,T3EB2,T3BVE,T3RE2D,T3ADHL,T3VDHL2",
    5: "T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB1,T2BVE,T2RE1,T2AE,T2VE,T3EB2,T3BVE,T3RE2D,T3AE,T3VE,T4EB2,T4BVE,T4RE2D,T4ADBA,T4VE"
}

df = pd.concat([create_table_from_codes(cluster, codes) for cluster, codes in clusters.items()], ignore_index=True)
print(df)

output_file = 'cluster_sentences.csv'

# Save the DataFrame as a CSV file
df.to_csv(output_file, index=False)
print(f"Table saved successfully to {output_file}.")

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

# Add a 'size' column to the DataFrame. Set a larger size for Cluster 1.
df['size'] = np.where(df['cluster'] == 'Cluster 1', 300, 100)  # 500 for Cluster 1, 100 for others

# Define a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['order'], empty='none')

# The basic scatter plot with shapes
points = alt.Chart(df).mark_point(filled=False, size=400).encode(  # Increase shape size with size=100
    x='order:Q',
    y=alt.Y('sentence:N',
            sort='-x',
            axis=alt.Axis(labelFontSize=16, labelLimit=800, grid=True, titleY=300, titleX=-380)  # Increase font size, label limit, add grid lines, and move title position
    ),
    color='cluster:N',
    opacity=alt.value(1),
    shape='cluster:N'  # encoding shape by cluster
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(df).mark_point().encode(
    x='order:Q',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw text labels near the points, and highlight based on selection
text = points.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'sentence:N', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(df).mark_rule(color='gray').encode(
    x='order:Q',
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
chart = alt.layer(points, selectors, rules, text,
          data=df, width=600, height=500,
          title='Sequential Sentences for Each Cluster')

# Grid
grid = alt.Chart(df).mark_rule(color='lightgray').encode(
    x=alt.X('order:Q', axis=alt.Axis(grid=False)),
    y=alt.Y('sentence:N', sort='-x', axis=alt.Axis(grid=False))
).properties(width=600, height=600)

# Put the six layers into a chart and bind the data
chart = alt.layer(grid, points, selectors, rules, text,
          data=df,
          width=600, height=500,
          title={
              "text": 'K-Means Clustering of Engineering Approaches: Median String Sequences',
              "subtitle": 'Clusters Across Control, Experimental Group 1, and Experimental Group 2',
              "color": "black",
              "subtitleColor": "gray"
          }
                  )


# Save the chart as an HTML file
chart.save('chart.html')

# Convert chart to JSON and print
chart_json = chart.to_json()
print(chart_json)