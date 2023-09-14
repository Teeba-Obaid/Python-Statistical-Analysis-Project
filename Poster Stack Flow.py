import pandas as pd
import altair as alt

# Load the CSV data
df = pd.read_csv("4_case_study.csv")

# Create separate dataframes for each category
df_engineering = df[df['Category'] == 'Engineering Approaches']
df_search = df[df['Category'] == 'Search Strategies']

# Melt the DataFrame to a long format
df_engineering_melt = df_engineering.melt(id_vars=['Category', 'Variables'],
                                          value_vars=['Student A: KI Voltage Drop: 2; KI Current: 2',
                                                      'Student B: KI Voltage Drop: 3; KI Current: 2',
                                                      'Student C: KI Voltage Drop: 3; KI Current: 4',
                                                      'Student D: KI Voltage Drop: 5; KI Current: 4'],
                                          var_name='Case Study', value_name='Frequency')

df_search_melt = df_search.melt(id_vars=['Category', 'Variables'],
                                value_vars=['Student A: KI Voltage Drop: 2; KI Current: 2',
                                            'Student B: KI Voltage Drop: 3; KI Current: 2',
                                            'Student C: KI Voltage Drop: 3; KI Current: 4',
                                            'Student D: KI Voltage Drop: 5; KI Current: 4'],
                                var_name='Case Study', value_name='Frequency')

# Define color scheme
color_scheme = alt.Scale(
    domain=['Student A: KI Voltage Drop: 2; KI Current: 2',
            'Student B: KI Voltage Drop: 3; KI Current: 2',
            'Student C: KI Voltage Drop: 3; KI Current: 4',
            'Student D: KI Voltage Drop: 5; KI Current: 4'],
    range=['#1f77b4', '#ff7f0e', '#83D350', '#d62728']  # Substitute with the colors you want
)
legend_data = pd.DataFrame({
    'Case Study': ['Student A: KI Voltage Drop: 2; KI Current: 2',
                   'Student B: KI Voltage Drop: 3; KI Current: 2',
                   'Student C: KI Voltage Drop: 3; KI Current: 4',
                   'Student D: KI Voltage Drop: 5; KI Current: 4'],
})

# Apply color_scheme to color encoding in legend_symbols
legend_symbols = alt.Chart(legend_data).mark_circle(size=150).encode(
    y=alt.Y('Case Study:N', axis=None, title=None),
    color=alt.Color('Case Study:N', legend=None, scale=color_scheme)
)
# Apply color_scheme to color encoding in chart_engineering
chart_engineering = alt.Chart(df_engineering_melt).mark_bar(size=9).encode(
    y=alt.Y('Variables:N', sort=df_engineering['Variables'].unique().tolist(),
            axis=alt.Axis(labelFontSize=18, labelLimit=420, titleX=-415)),
    x=alt.X('Frequency:Q', scale=alt.Scale(domain=(0, 10)), axis=alt.Axis(tickCount=11, labels=True, labelFontSize=14)),
    color=alt.Color('Case Study:N', legend=None, scale=color_scheme),
    tooltip=['Case Study', 'Category', 'Frequency', 'Variables']
).properties(
    width=200,  # Add your desired width
    height=400  # Add your desired height
)

# Apply color_scheme to color encoding in chart_search
chart_search = alt.Chart(df_search_melt).mark_bar(size=9).encode(
    y=alt.Y('Variables:N', sort=df_search['Variables'].unique().tolist(),
        axis=alt.Axis(labelFontSize=18, labelLimit=350, titleX=-323, title=None)),
    x=alt.X('Frequency:Q', scale=alt.Scale(domain=(0, 8)), axis=alt.Axis(tickCount=11, labelFontSize=14)),
    color=alt.Color('Case Study:N', legend=None, scale=color_scheme),
    tooltip=['Case Study', 'Category', 'Frequency', 'Variables']
).properties(
    width=200,  # Add your desired width
    height=400  # Add your desired height
)


# Apply color_scheme to color encoding in legend_symbols
legend_symbols = alt.Chart(legend_data).mark_circle(size=150).encode(
    y=alt.Y('Case Study:N', axis=None, title=None),
    color=alt.Color('Case Study:N', legend=None, scale=color_scheme)
)


# Combine the two charts horizontally
combined_chart = alt.hconcat(chart_engineering, chart_search)

# Create legend chart
legend_data = pd.DataFrame({
    'Case Study': ['Student A: KI Voltage Drop: 2; KI Current: 2',
                   'Student B: KI Voltage Drop: 3; KI Current: 2',
                   'Student C: KI Voltage Drop: 3; KI Current: 4',
                   'Student D: KI Voltage Drop: 5; KI Current: 4'],
})

# Create symbols for the legend
# Apply color_scheme to color encoding in legend_symbols
legend_symbols = alt.Chart(legend_data).mark_circle(size=150).encode(
    y=alt.Y('Case Study:N', axis=None, title=None),
    color=alt.Color('Case Study:N', legend=None, scale=color_scheme)
)

# Create labels for the legend
legend_labels = alt.Chart(legend_data).mark_text(align='left', dx=-125, fontSize=18).encode(
    y=alt.Y('Case Study:N', axis=None, title=None),
    text=alt.Text('Case Study:N')
)


# Combine symbols and labels
legend_chart = alt.hconcat(legend_symbols, legend_labels).resolve_scale(
    y='shared',
    color='independent'
)

# Combine the charts and the legend, and remove the stroke around the charts
final_chart = alt.vconcat(combined_chart, legend_chart).resolve_scale(color='independent').configure_view(stroke=None)

# Save and display
final_chart.save('chart.html')

final_chart_json = final_chart.to_json()
print(final_chart_json)