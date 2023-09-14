import re
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Create a dictionary without the trial numbers in the keys
code_dict = {
    "NAN": "No new comparative trial",
    "NO": "No action",
    "TPN": "New comparative trial",
    "PCS": "Prediction Current: same rule",
    "PVDS": "Prediction Voltage Drop: same rule",
    "PCF": "Prediction Current: Fill up gaps",
    "PVDF": "Prediction Voltage Drop: Fill up gaps",
    "CCV": "Confidence Current: verify prediction",
    "CVDV": "Confidence Voltage Drop: verify prediction",
    "CCF": "Confidence Current: falsify prediction",
    "CVDF": "Confidence Voltage Drop: falsify prediction",
    "PG": "Identify problem: goal stated",
    "RCCR": "Rule Current: Confirming Redundancy",
    "RVDCR": "Rule Voltage Drop: Confirming Redundancy",
    "RCSS": "Rule Current: Simultaneous scanning",
    "RVDSS": "Rule Voltage Drop: Simultaneous scanning",
    "RCR": "Rule Current: Successive scanning",
    "RVDR": "Rule Voltage Drop: Successive scanning",
    "RCM": "Rule Current: Focus gambling",
    "RVDM": "Rule Voltage Drop: Focus gambling",
    "RCO": "Rule Current: Conservative Focusing",
    "RVDO": "Rule Voltage Drop: Conservative Focusing",
    "PtVDN": "Post-test: Voltage Drop non-normative",
    "PtCN": "Post-test: Current non-normative",
    "PtVDP": "Post-test: Voltage Drop partial",
    "PtCP": "Post-test: Current partial",
    "PtVDV1": "Post-test: Voltage Drop 1 Valid link",
    "PtCV1": "Post-test: Current 1 Valid link",
    "PtVDV2": "Post-test: Voltage Drop 2 Valid links",
    "PtCV2": "Post-test: Current 2 Valid links"
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

def assign_trial_number(group):
    trial_zero_keys = ["No new comparative trial", "New comparative trial"]  # Fill in with the correct keys
    new_trial_keys = ["Prediction Current: same rule", "Prediction Voltage Drop: same rule", "Prediction Current: Fill up gaps", "Prediction Voltage Drop: Fill up gaps"]  # Fill in with the correct keys
    trial_number = 0
    previous_key = None

    for i, row in group.iterrows():
        cluster_trial_key = (row['cluster'], row['variables'])

        # Set trial number to 0 for variables in trial_zero_keys
        if row['variables'] in trial_zero_keys:
            trial_number = 0
            group.at[i, 'trial'] = 'Trial ' + str(trial_number)

        # For variables in new_trial_keys, check whether the trial number should be incremented
        elif row['variables'] in new_trial_keys:
            # Increment the trial number if the previous variable was not in new_trial_keys
            if previous_key not in new_trial_keys:
                trial_number += 1
            group.at[i, 'trial'] = 'Trial ' + str(trial_number)

        # For other variables, set the trial number to NaN
        else:
            group.at[i, 'trial'] = 'Trial nan'

        previous_key = row['variables']

    return group


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
    1: "TPN,PCF,PVDS,CCF,CVDV,NO,RCR,RVDSS,PCS,PVDF,CCV,CVDV,RCSS,RVDR,PtVDP,PtCP",
    2: "TPN,PCS,PVDF,CCV,CVDV,PG,RCSS,RVDM,PCF,PVDS,CCV,CVDV,RCR,RVDSS,PCF,PVDS,CCF,CVDV,RCO,RVDSS,PCS,PVDS,CCF,CVDV,RCSS,RVDSS,PtVDV1,PtCV2",
    3: "TPN,PCF,PVDF,CCV,CVDV,PG,RCR,RVDSS,PCF,PVDS,CCV,CVDV,RCO,RVDR,PCF,PVDF,CCF,CVDF,RCO,RVDO,PtVDV2,PtCV2",
}

# Concatenate the dataframes for all clusters
df = pd.concat([create_table_from_codes(cluster, codes) for cluster, codes in clusters.items()], ignore_index=True)

# Apply the function to each group
df = df.groupby('cluster').apply(assign_trial_number).reset_index(drop=True)

print(df)

assign_trial_number.trial_dict = {}
df = assign_trial_number(df)
df['trial'] = df['trial'].apply(clean_trial)
df['trial'] = df['trial'].fillna(method='ffill')

# Define a maximum x value for each chart
max_order = df['order'].max()

# Define sentence_order
sentence_order = [
    "No new comparative trial",
    "New comparative trial",
    "Prediction Current: same rule",
    "Prediction Voltage Drop: same rule",
    "Prediction Current: Fill up gaps",
    "Prediction Voltage Drop: Fill up gaps",
    "Confidence Current: verify prediction",
    "Confidence Voltage Drop: verify prediction",
    "Confidence Current: falsify prediction",
    "Confidence Voltage Drop: falsify prediction",
    "No action",
    "Identify problem: goal stated",
    "Rule Current: Confirming Redundancy",
    "Rule Voltage Drop: Confirming Redundancy",
    "Rule Current: Simultaneous scanning",
    "Rule Voltage Drop: Simultaneous scanning",
    "Rule Current: Successive scanning",
    "Rule Voltage Drop: Successive scanning",
    "Rule Current: Focus gambling",
    "Rule Voltage Drop: Focus gambling",
    "Rule Current: Conservative Focusing",
    "Rule Voltage Drop: Conservative Focusing",
    "Post-test: Voltage Drop non-normative",
    "Post-test: Current non-normative",
    "Post-test: Voltage Drop partial",
    "Post-test: Current partial",
    "Post-test: Voltage Drop 1 Valid link",
    "Post-test: Current 1 Valid link",
    "Post-test: Voltage Drop 2 Valid links",
    "Post-test: Current 2 Valid links"
]

# Reverse the order of sentence_order
sentence_order_reversed = sentence_order[::-1]

# Define the color palette
color_palette = alt.Scale(domain=['Cluster 1', 'Cluster 2', 'Cluster 3'],
                          range=['#ff7f0e', '#8d0171', '#f80039'])

# Define the shape palette
shape_palette = alt.Scale(domain=['Cluster 1', 'Cluster 2', 'Cluster 3'],
                          range=['square', 'triangle-down', 'diamond'])

# Define the unique sentences
unique_sentences = df['variables'].unique().tolist()


# Create the facet charts with grid lines only for data points
chart1 = alt.Chart(df[df['cluster'] == 'Cluster 1']).mark_point(filled=True, size=200).encode(
    x=alt.X('order', axis=alt.Axis(grid=False)),
    y=alt.Y('variables',
            scale=alt.Scale(domain=sentence_order),
            sort=sentence_order_reversed,
            axis=alt.Axis(labelFontSize=16,labelLimit=800,grid=True,titleY=330, titleX=-340)),
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
            axis=alt.Axis(labelFontSize=16,labelLimit=800,grid=True,titleY=330, titleX=-340)),
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

# Arrange the charts in the specified grid
combined_chart = alt.vconcat(
    alt.hconcat(chart1, chart2),
    alt.hconcat(chart3)).resolve_scale(y='shared').properties(
    title={
      "text": 'K-Means Clustering of Search Strategies: Median String Sequences',
      "subtitle": 'Clusters Across Experimental Group 1',
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

# Save charts 3
chart3 = alt.hconcat(chart3)
chart3.save('charts3.html')


# Convert chart to JSON and print
combined_chart_json = combined_chart.to_json()
print(combined_chart_json)