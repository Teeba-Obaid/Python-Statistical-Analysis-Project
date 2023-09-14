import altair as alt
import pandas as pd

# Create a dataframe from your data
data = pd.DataFrame({
    'n_clusters': [2, 3, 4, 5, 6, 7, 8],
    'silhouette_score': [
        0.5397036615200967,
        0.5305015754339137,
        0.5857589521887961,
        0.6002326192689588,
        0.5545306089415436,
        0.5714849259148564,
        0.5933831805928853
    ]
})

max_score = data['silhouette_score'].max()

# Create the chart
chart = alt.Chart(data).mark_bar(
    size=18               # change the size of the bars
).encode(
    x=alt.X('n_clusters:O', axis=alt.Axis(title="Number of clusters", titleFontSize=14, labelFontSize=14)),   # change the label and font size of x-axis
    y=alt.Y('silhouette_score:Q', axis=alt.Axis(title="Silhouette score", titleFontSize=14, labelFontSize=14, format=".2f")),   # change the label and round y-axis labels to two decimal places
    color=alt.condition(
        alt.datum.silhouette_score == max_score,
        alt.value('crimson'),     # if the condition is True, the color is red
        alt.value('gray')   # if the condition is False, the color is gray
    )
).properties(
    title=alt.TitleParams(
        text='Silhouette Scores for Different Numbers of Clusters',
        subtitle='Control, Experimental 1, and Experimental 2',
        fontSize=14    # change the font size of the title
    ),
    width=300,    # adjust the width of the chart
    height=400    # adjust the height of the chart
).configure_axis(
    grid=False
)

# Save the chart to an HTML file
chart.save('chart.html')