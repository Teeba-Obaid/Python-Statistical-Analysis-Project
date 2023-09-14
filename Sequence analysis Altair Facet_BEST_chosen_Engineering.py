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
    match = re.match(r"(T[0-9]+)?([A-Z0-9]+)", code, re.I)
    if match:
        items = match.groups()
    else:
        return f"Code {code} not found in the dictionary."

    # Get the corresponding sentence for the text part of the code
    sentence = code_dict.get(items[1], f"Code {items[1]} not found in the dictionary.")

    # Append the trial number part in parentheses if it exists
    if items[0] is not None:
        return f"{sentence} ({items[0]})"
    else:
        return sentence

def assign_trial_number(row):
    if row['variables'] in {"1 bulb equal", "2 bulbs equal", "1 vs. 2 bulbs different"}:
        if row['cluster'] in assign_trial_number.trial_dict:
            assign_trial_number.trial_dict[row['cluster']] += 1
            return 'Trial ' + str(assign_trial_number.trial_dict[row['cluster']])
        else:
            assign_trial_number.trial_dict[row['cluster']] = 1
            return 'Trial 1'
    else:
        return 'Trial nan' # return 'Trial nan' if the row is not part of a trial

def clean_trial(x):
    word, number = x.split() # split string into two parts: 'Trial' and the number
    if pd.isnull(number) or number.lower() == 'nan':
        return np.nan
    else:
        return word + ' ' + str(int(float(number)))

def create_table_from_codes(cluster_number, codes_string):
    codes = codes_string.split(',')
    sentences = [transform_code_to_sentence(code) for code in codes]
    data = [{'cluster': f"Cluster {cluster_number}", 'code': code, 'variables': sentence, 'order': i+1} for i, (code, sentence) in enumerate(zip(codes, sentences))]
    df = pd.DataFrame(data)
    return df

clusters = {
    1: "EB1,BVE,BVD,RE1,AE,VE",
    2: "EB1,BVE,RE1,ADBA,VE,EB2,BVE,RE1,AE,VE",
    3: "DB,BVE,RID,AE,VE,EB2,BVE,RI2,AE,VE,EB2,BVE,RI2,ADBA,VE,EB1,BVE,RID,ADBA,VE,EB1,BVE,RE1,ADBA,VE",
    4: "EB1,BVE,RE1,ADBA,VE,EB1,BVE,RE1,AE,VE,DB,BVE,RID,AE,VE,EB2,BVE,RE2D,ADHL,VE",
    5: "DB,BVE,RE1,AE,VE,EB2,BVE,RE2D,ADBA,VE,EB2,BVE,RE2D,ADHL,VDHL2"
}

# Concatenate the dataframes for all clusters
df = pd.concat([create_table_from_codes(cluster, codes) for cluster, codes in clusters.items()], ignore_index=True)
print(df)

assign_trial_number.trial_dict = {}
df['trial'] = df.apply(assign_trial_number, axis=1)
df['trial'] = df['trial'].apply(clean_trial)
df['trial'] = df['trial'].fillna(method='ffill')

# Define a maximum x value for each chart
max_order = df['order'].max()

# Define sentence_order
sentence_order = [
    "1 bulb equal",
    "2 bulbs equal",
    "1 vs. 2 bulbs different",
    "Battery voltage equal",
    "Battery voltage different",
    "Resistance change: 1 or 2 bulbs",
    "Resistance change: 2 bulbs",
    "Resistance equal: 2 bulbs different value",
    "Resistance equal: 2 or 1 vs. 2 bulbs same value",
    "Resistance equal: 1 bulb",
    "Resistance equal: 2 bulbs different value & position",
    "Ammeter equal: after/before 1 or 2 bulb",
    "Ammeter different: before vs. after 1 or 2 bulbs",
    "Ammeter different: on high/low of 2 bulb",
    "Voltmeter equal: 1 bulb or 2 bulbs or battery",
    "Voltmeter equal: 2 bulbs",
    "Voltmeter different: high vs. low resistance 2 bulbs",
    "Voltmeter different: high vs. low resistance 2 bulbs vs. battery"
]

# Reverse the order of sentence_order
sentence_order_reversed = sentence_order[::-1]

# Define the color palette
color_palette = alt.Scale(domain=['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5'],
                          range=['#1f77b4', '#ff7f0e', '#4eac01', '#8d0171', '#f80039'])

# Define the shape palette
shape_palette = alt.Scale(domain=['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5'],
                          range=['circle', 'square', 'cross', 'triangle-down', 'diamond'])

# Define the unique sentences
unique_sentences = df['variables'].unique().tolist()


# Create the facet charts with grid lines only for data points
chart1 = alt.Chart(df[df['cluster'] == 'Cluster 1']).mark_point(filled=True, size=200).encode(
    x=alt.X('order', axis=alt.Axis(grid=False)),
    y=alt.Y('variables',
            scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed,
            axis=alt.Axis(labelFontSize=16,labelLimit=800,grid=True,titleY=330, titleX=-430)),
    color=alt.Color('cluster:N',scale=color_palette),
    shape=alt.Shape('cluster:N',scale=shape_palette),
    order=alt.Order('order'),  # This line is added to order the line correctly
    tooltip=['variables']
).properties(
    title='Cluster 1',
    width=500,
    height=600
) + alt.Chart(df[df['cluster'] == 'Cluster 1']).mark_line().encode(
    x='order',
    y=alt.Y('variables', scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed),
    order=alt.Order('order')  # This line is added to order the line correctly
)

annotations_chart1 = alt.Chart(df[(df['cluster'] == 'Cluster 1') & df['trial'].notna()]).mark_text(
    align='left',
    baseline='middle',
    dx=-35,  # Nudges text to right so it doesn't appear on top of the point
    dy=10
).encode(
    x='order',
    y=alt.Y('variables', scale=alt.Scale(domain=sentence_order), sort=sentence_order_reversed),
    text='trial:N',
)

# Include the annotations in the chart
chart1 = chart1 + annotations_chart1

# Create the facet charts with grid lines only for data points
chart2 = alt.Chart(df[df['cluster'] == 'Cluster 2']).mark_point(filled=True, size=200).encode(
    x=alt.X('order', axis=alt.Axis(grid=False)),
    y=alt.Y('variables',
            title=None,
            scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed,
            axis=alt.Axis(labels=False, grid=True)),
    color=alt.Color('cluster:N',scale=color_palette),
    shape=alt.Shape('cluster:N',scale=shape_palette),
    order=alt.Order('order'),  # This line is added to order the line correctly
    tooltip=['variables']
).properties(
    title='Cluster 2',
    width=500,
    height=600
) + alt.Chart(df[df['cluster'] == 'Cluster 2']).mark_line().encode(
    x='order',
    y=alt.Y('variables', scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed),
    order=alt.Order('order')  # This line is added to order the line correctly
)
annotations_chart2 = alt.Chart(df[(df['cluster'] == 'Cluster 2') & df['trial'].notna()]).mark_text(
    align='left',
    baseline='middle',
    dx=-38,  # Nudges text to right so it doesn't appear on top of the point
    dy=10

).encode(
    x='order',
    y=alt.Y('variables', scale=alt.Scale(domain=sentence_order), sort=sentence_order_reversed),
    text='trial:N',
)

# Include the annotations in the chart
chart2 = chart2 + annotations_chart2


# Create the facet charts with grid lines only for data points
chart3 = alt.Chart(df[df['cluster'] == 'Cluster 3']).mark_point(filled=True, size=200).encode(
    x=alt.X('order', axis=alt.Axis(grid=False)),
    y=alt.Y('variables',
            scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed,
            axis=alt.Axis(labelFontSize=16,labelLimit=800,grid=True,titleY=330, titleX=-430)),
    color=alt.Color('cluster:N',scale=color_palette),
    shape=alt.Shape('cluster:N',scale=shape_palette),
    order=alt.Order('order'),  # This line is added to order the line correctly
    tooltip=['variables']
).properties(
    title='Cluster 3',
    width=500,
    height=600
) + alt.Chart(df[df['cluster'] == 'Cluster 3']).mark_line().encode(
    x='order',
    y=alt.Y('variables', scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed),
    order=alt.Order('order')  # This line is added to order the line correctly
)

annotations_chart3 = alt.Chart(df[(df['cluster'] == 'Cluster 3') & df['trial'].notna()]).mark_text(
    align='left',
    baseline='middle',
    dx=7  # Nudges text to right so it doesn't appear on top of the point
).encode(
    x='order',
    y=alt.Y('variables', scale=alt.Scale(domain=sentence_order), sort=sentence_order_reversed),
    text='trial:N',
)

# Include the annotations in the chart
chart3 = chart3 + annotations_chart3

# Create the facet charts with grid lines only for data points
chart4 = alt.Chart(df[df['cluster'] == 'Cluster 4']).mark_point(filled=True, size=200).encode(
    x=alt.X('order', axis=alt.Axis(grid=False)),
    y=alt.Y('variables',
            title=None,
            scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed,
            axis=alt.Axis(labels=False, grid=True)),
    color=alt.Color('cluster:N',scale=color_palette),
    shape=alt.Shape('cluster:N',scale=shape_palette),
    order=alt.Order('order'),  # This line is added to order the line correctly
    tooltip=['variables']
).properties(
    title='Cluster 4',
    width=500,
    height=600
) + alt.Chart(df[df['cluster'] == 'Cluster 4']).mark_line().encode(
    x='order',
    y=alt.Y('variables', scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed),
    order=alt.Order('order')  # This line is added to order the line correctly
)

annotations_chart4 = alt.Chart(df[(df['cluster'] == 'Cluster 4') & df['trial'].notna()]).mark_text(
    align='left',
    baseline='middle',
    dx=7  # Nudges text to right so it doesn't appear on top of the point
).encode(
    x='order',
    y=alt.Y('variables', scale=alt.Scale(domain=sentence_order), sort=sentence_order_reversed),
    text='trial:N',
)

# Include the annotations in the chart
chart4 = chart4 + annotations_chart4


# Create the facet charts with grid lines only for data points
chart5 = alt.Chart(df[df['cluster'] == 'Cluster 5']).mark_point(filled=True, size=200).encode(
    x=alt.X('order', axis=alt.Axis(grid=False)),
    y=alt.Y('variables',
            scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed,
            axis=alt.Axis(labelFontSize=16,labelLimit=800,grid=True,titleY=330, titleX=-430)),
    color=alt.Color('cluster:N',scale=color_palette),
    shape=alt.Shape('cluster:N',scale=shape_palette),
    order=alt.Order('order'),  # This line is added to order the line correctly
    tooltip=['variables']
).properties(
    title='Cluster 5',
    width=500,
    height=600
) + alt.Chart(df[df['cluster'] == 'Cluster 5']).mark_line().encode(
    x='order',
    y=alt.Y('variables', scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed),
    order=alt.Order('order')  # This line is added to order the line correctly
)

annotations_chart5 = alt.Chart(df[(df['cluster'] == 'Cluster 5') & df['trial'].notna()]).mark_text(
    align='left',
    baseline='middle',
    dx=7,  # Nudges text to right so it doesn't appear on top of the point

).encode(
    x='order',
    y=alt.Y('variables', scale=alt.Scale(domain=sentence_order), sort=sentence_order_reversed),
    text='trial:N',
)

# Include the annotations in the chart
chart5 = chart5 + annotations_chart5

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
        "subtitleColor": "gray",
        "anchor": "middle",
        "subtitlePadding": 5,
        "fontSize": 18,
        "subtitleFontSize": 16
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