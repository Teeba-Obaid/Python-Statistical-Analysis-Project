import numpy as np
import scipy.stats as stats
import pandas as pd
import altair as alt
import json


# Table 3 data
data = {
    "Normative": [5, 11, 8],
    "Non-normative": [2, 1, 1],
    "Target": [4, 11, 7],
    "Off-Target": [3, 1, 2],
    "Science": [3, 0, 2],
    "Social Justice": [3, 11, 6]
}

# Chi-Square Test for idea numbers (Table 1)
observed = np.array([92, 120, 118])
expected = np.array([330/3, 330/3, 330/3])
chi_squared_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
print(f"Chi-Square Test Statistic for Idea Numbers: {chi_squared_stat}")
print(f"Chi-Square Test P Value for Idea Numbers: {p_value}")

# Friedman Test
chi_squared_stat, p_value = stats.friedmanchisquare(*data.values())
print(f"\nFriedman Test Chi-Squared Stat: {chi_squared_stat}")
print(f"Friedman Test P Value: {p_value}")

# Convert data to DataFrame for visualization
df = pd.DataFrame(data)
df['Time Point'] = ['Pre-Test', 'Embedded', 'Post-Test']
df['Number of Ideas'] = np.sum(df.values[:, :-1], axis=1)  # Add 'Number of Ideas' column

# Melt the DataFrame to long format for Altair
df_melted = df.melt(id_vars=['Time Point', 'Number of Ideas'], var_name='Category/Theme', value_name='Value')

# Visualization with Altair
chart = alt.Chart(df_melted).mark_line(point=True).encode(
    x=alt.X('Category/Theme', title='Category/Theme'),
    y=alt.Y('Value', title='Value'),
    color=alt.Color('Time Point', title='Time Point'),
    tooltip=['Time Point', 'Category/Theme', 'Value']
).properties(
    title=alt.TitleParams('Changes in Idea Instances Across Time Points', fontSize=18),
    width=600,
    height=400
).interactive().configure_axis(
    labelFontSize=14,  # Font size of axis labels
    titleFontSize=16   # Font size of axis titles
).configure_legend(
    labelFontSize=14,  # Font size of legend labels
    titleFontSize=16   # Font size of legend title
)

# Save the chart to an HTML file
chart.save('chart.html')

# Perform bootstrap test for each category/theme and each pair of time points
comparisons = [(0, 1), (0, 2), (1, 2)]
n_iterations = 1000
np.random.seed(42)
bootstrap_data = []

for category in data.keys():
    values = np.array(data[category])
    for comp in comparisons:
        boot_diff = []
        for _ in range(n_iterations):
            resample_a = np.random.choice(data[category][comp[0]], size=data[category][comp[0]], replace=True)
            resample_b = np.random.choice(data[category][comp[1]], size=data[category][comp[1]], replace=True)

            diff = np.mean(resample_a) - np.mean(resample_b)
            boot_diff.append(diff)
        observed_diff = np.mean(values[comp[0]]) - np.mean(values[comp[1]])
        p_value = (np.sum(np.abs(boot_diff) >= np.abs(observed_diff)) + 1) / (n_iterations + 1)
        bootstrap_data.append({
            'Category/Theme': category,
            'Comparison': f'{df["Time Point"].unique()[comp[0]]} vs {df["Time Point"].unique()[comp[1]]}',
            'p_value': p_value
        })

    # Convert bootstrap data to DataFrame
    bootstrap_df = pd.DataFrame(bootstrap_data)

    # Specify custom colors
    custom_colors = ['#1f77b4','#ff7f0e','#2ca02c']

    # Visualize bootstrap test results using Altair
    bootstrap_chart = alt.Chart(bootstrap_df).mark_point(filled=False,size=300).encode(
        x=alt.X('Category/Theme:O',title='Category/Theme'),
        y=alt.Y('p_value:Q',title='p-value',scale=alt.Scale(type='log',domain=[0.0001,1])),
        color=alt.Color('Comparison:N',title='Comparison'),
        shape=alt.Shape('Comparison:N',title='Comparison'),
        tooltip=['Category/Theme','Comparison','p_value']
    ).properties(
        title="Bootstrap Test Outcomes for Each Category",
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=14
    ).configure_legend(
        labelFontSize=14,
        titleFontSize=14
    )

    # Save bootstrap test chart to an HTML file
    bootstrap_chart.save('bootstrap_test_chart.html')

    # Convert bootstrap data to JSON
    bootstrap_json = json.dumps(bootstrap_data,indent=4)

    # Print the JSON data
    print(bootstrap_json)

    # Save bootstrap data to an Excel file
    bootstrap_df.to_excel('bootstrap_test_outcomes.xlsx',index=False)