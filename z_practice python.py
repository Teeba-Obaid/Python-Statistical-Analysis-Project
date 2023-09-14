import pandas as pd

# reading all observations
df = pd.read_csv("data10.csv")
print(df)
# reading 5 observations
print(df.head())

# list of columns
columns = df.columns
print(columns)

# dimensions
shape = df.shape
print(shape)

# slicing observations and variables
# use iloc for columns if there is no index for columns
sliced_rows_columns = df.iloc[5:10, :3]
print(sliced_rows_columns)

# slicing specific rows
sliced_rows_columns = df.loc[:5]
print(sliced_rows_columns)

# slicing observations using loc as boolean mask
sliced_rows_columns = df.loc[5:10, "No action":"Prediction Current: same rule"]
print(sliced_rows_columns)

# slicing all rows but specific columns
sliced_rows_columns = df.loc[:, "No action":"Prediction Current: same rule"]
print(sliced_rows_columns)

# selecting using .loc[]
select = df.loc[[4, 5], ["No action", "Post-test: Voltage Drop 2 Valid links"]]
print(select)

# obtain dataframe values + index + column name
value = df.loc[[4], ["Post-test: Voltage Drop 2 Valid links"]]
print(value)

# obtain dataframe values without index and column name
value = df.loc[4, "Post-test: Voltage Drop 2 Valid links"]
print(value)

# select single column without writing .loc
single_column = df[["Post-test: Voltage Drop 2 Valid links"]]
print(single_column)

# obtain data bottom-up
value = df.iloc[-3:, -2:]
print(value)

# sorting values
sort = df.iloc[:, -2:].sort_values(by="Post-test: Voltage Drop 2 Valid links", ascending=False)
print(sort)

# summary statistics
stats = df.iloc[:, [24, 28]].describe()
print(stats)

# summary statistics of all observations
stats = df.describe(include="all")
print(stats)

# single statistics
stats = df.iloc[:, [24, 28]].sum()
print(stats)

# single statistics
stats = df.iloc[:, [24, 28]].count()
print(stats)

# single statistics
stats = df.iloc[:, [24, 28]].median()
print(stats)

# frequency
stats = df.iloc[:, [24]].value_counts()
print(stats)

# write frequency of all columns
stats_all = {}

# loop through each column
# In the first iteration, column is set to the name of the first column in df, and df[column] refers to that column.
# In the second iteration, column is set to the name of the second column in df, and df[column] refers to that column.
for column in df.columns:
    stats_all[column] = df[column].value_counts()

# Convert to DataFrame
stats_df = pd.DataFrame.from_dict(stats_all, orient='columns')

# Save to CSV
stats_df.to_csv('stats.csv')