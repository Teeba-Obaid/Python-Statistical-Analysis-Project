import re
import pandas as pd
import plotly.graph_objects as go

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
    return ', '.join(sentences)

import pandas as pd

def create_table_from_codes(cluster_number, codes_string):
    codes = codes_string.split(',')
    data = [{'cluster': f"cluster {cluster_number}", 'sentence': transform_code_to_sentence(code)} for code in codes]
    df = pd.DataFrame(data)
    return df

clusters = {
    1: "T1EB1,T1BVE,T1BVD,T1AE,T1VE",
    2: "T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB2,T2BVE,T2RE1,T2AE,T2VE",
    3: "T1EB1,T1BVE,T1RID,T1AE,T1VE,T2EB1,T2BVE,T2RE1,T2AE,T2VE,T3EB1,T3BVE,T3RE1,T3ADBA,T3VE,T4EB2,T4BVE,T4RE2D,T4ADBA,T4VE,T5EB2,T5BVE,T5RE2D,T5AE,T5VE,T6EB2,T6BVE,T6RE2D",
    4: "T1EB1,T1BVE,T1RE1,T1AE,T1VE,T2EB1,T2BVE,T2RID,T2AE,T2VE,T3EB2,T3BVE,T3RE2D,T3AE,T3VE"
}

df = pd.concat([create_table_from_codes(cluster, codes) for cluster, codes in clusters.items()], ignore_index=True)

print(df)

import numpy as np

import plotly.express as px

fig = px.parallel_categories(df, dimensions=['cluster', 'sentence'], color=df.index, labels={'cluster':'Cluster', 'sentence':'Sentence'})

fig.update_layout(
    width=1000,
    height=600,
    autosize=True,
)

fig.show()

# Create a data frame for the treemap with sentences
treemap_df = pd.DataFrame(columns=['cluster', 'sentence_count', 'sentences'])
for cluster, codes in clusters.items():
    sentence_count = len(codes.split(','))
    sentences = transform_string_of_codes(codes)  # Transform codes to sentences
    treemap_df = treemap_df.append({'cluster': f"Cluster {cluster}", 'sentence_count': sentence_count, 'sentences': sentences}, ignore_index=True)

# Plot the treemap
fig = go.Figure(go.Treemap(
    labels=treemap_df['cluster'],  # Set the cluster names as labels
    parents=['', '', '', ''],  # Set empty parents to get root nodes
    values=treemap_df['sentence_count'],  # Set sentence counts as values
    text=treemap_df['sentences'],  # Set sentences as text (will be displayed inside boxes)
    textinfo='label+text',  # Show both labels and text
    hovertemplate='<b>%{label}</b><br>%{text}',  # Define hover template
    textfont=dict(size=14),  # Set the font size of the sentences
))

fig.update_layout(
    width=800,
    height=600,
    title_text='Distribution of Sentences across Clusters',
    title_x=0.5
)

fig.show()