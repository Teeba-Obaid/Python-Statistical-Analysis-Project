import re
import pandas as pd
import plotly.graph_objects as go
import altair as alt


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
    1: "T1EB1,T1BVE,T1BVD,T1AE,T1VE",
    2: "T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB2,T2BVE,T2RE1,T2AE,T2VE",
    3: "T1EB1,T1BVE,T1RID,T1AE,T1VE,T2EB1,T2BVE,T2RE1,T2AE,T2VE,T3EB1,T3BVE,T3RE1,T3ADBA,T3VE,T4EB2,T4BVE,T4RE2D,T4ADBA,T4VE,T5EB2,T5BVE,T5RE2D,T5AE,T5VE,T6EB2,T6BVE,T6RE2D",
    4: "T1EB1,T1BVE,T1RE1,T1AE,T1VE,T2EB1,T2BVE,T2RID,T2AE,T2VE,T3EB2,T3BVE,T3RE2D,T3AE,T3VE"
}

df = pd.concat([create_table_from_codes(cluster, codes) for cluster, codes in clusters.items()], ignore_index=True)
print(df)

output_file = 'cluster_sentences.csv'

# Save the DataFrame as a CSV file
df.to_csv(output_file, index=False)

print(f"Table saved successfully to {output_file}.")

# Save the DataFrame as a CSV file
df.to_csv(output_file, index=False)
print(f"Table saved successfully to {output_file}.")

# Create the Altair chart
chart = alt.Chart(df).mark_circle().encode(
    x='order:Q',
    y='sentence:N',
    color='cluster:N',
    tooltip='sentence:N',
    size=alt.Size('size:Q', scale=alt.Scale(range=[100, 1000]), legend=None)  # Map the 'size' encoding to the new 'size' column
).properties(
    width=600,
    height=600,
    title='Sequential Sentences for Each Cluster'
).facet(
    column='cluster:N'
)

# Save the chart as an HTML file
output_chart = 'sequential_sentences.html'
chart.save(output_chart)
print(f"Visualization saved successfully as {output_chart}.")