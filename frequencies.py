import pandas as pd
from tabulate import tabulate
from openpyxl import Workbook

data = [
    "Observation1,T1EB1,T1BVD,T1RID,T1AE,N,T2EB1,T2BVD,T2RID,T2AE,T2VE,,,,,,,,,,,,,,,,",
    "Observation2,T1EB1,T1BVD,T1RE1,T1AE,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation3,T1EB1,T1BVD,T1RE1,T1AE,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation4,T1EB1,T1BVD,T1RE1,T1AE,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation5,T1EB2,T1BVE,T1RE2S,T1ADBA,T1VE,T2EB2,T2BVE,T2RE2D,T2ADHL,T2VDHL2,,,,,,,,,,,,,,,",
    "Observation6,T1EB1,T1BVE,T1RID,T1AE,T1VE,T2EB1,T2BVD,T2RE1,T2AE,T2VE,T3EB2,T3BVE,T3RE2S,T3ADBA,N,T4EB2,T4BVE,T4RE2D,T4ADBA,N,,,,,",
    "Observation7,T1EB1,T1BVE,T1RID,T1ADBA,T1VE,T2EB2,T2BVE,T2RE2D,T2ADBA,T2VE,,,,,,,,,,,,,,,",
    "Observation8,T1EB1,T1BVE,T1RID,T1ADBA,T1VE,T2EB1,T2BVD,T2RE1,T2AE,T2VE,T3EB1,T3BVE,T3RID,T3ADBA,T3VE,T4EB2,T4BVE,T4RE2D,T4AE,T4VDHL2B,,,,,",
    "Observation9,T1EB2,T1BVD,T1RI2,T1ADBA,T1VDHL2B,,,,,,,,,,,,,,,,,,,,",
    "Observation10,T1EB1,T1BVE,T1RID,T1AE,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation11,T1EB2,T1BVE,T1RE2D,T1ADHL,T1VDHL2,,,,,,,,,,,,,,,,,,,,",
    "Observation12,T1EB1,T1BVD,T1RID,T1AE,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation13,T1DB,T1BVE,T1RE2S,T1AE,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation14,T1EB1,T1BVE,T1RID,T1AE,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation15,T1EB1,T1BVE,T1RID,T1AE,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation16,T1EB1,T1BVD,T1RE1,T1AE,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation17,T1EB2,T1BVE,T1RE2S,T1ADBA,N,,,,,,,,,,,,,,,,,,,,",
    "Observation18,T1EB1,T1BVE,T1RID,T1AE,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation19,T1EB2,T1BVE,T1RE2S,T1AE,N,,,,,,,,,,,,,,,,,,,,",
    "Observation20,T1EB2,T1BVD,T1RE1,T1AE,N,,,,,,,,,,,,,,,,,,,,",
    "Observation21,T1EB2,T1BVE,T1RE2D,T1AE,T1VDHL2B,T2EB2,T2BVE,T2RE2D,T2ADHL,T2VE,T3EB2,T3BVE,T3RE2D,T3ADHL,T3VDHL2,,,,,,,,,,",
    "Observation22,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB2,T2BVE,T2RE2D,T2ADHL,T2VE,T3EB2,T3BVE,T3RE2D,T3AE,T3VDHL2,T4EB2,T4BVE,T4RE2D,T4AE,T4VDHL2B,,,,,",
    "Observation23,T1EB1,T1BVE,T1RE1,T1AE,T1VE,T2DB,T2BVE,T2RID,T2AE,T2VE,,,,,,,,,,,,,,,",
    "Observation24,T1EB2,T1BVE,T1RI2,T1ADHL,T1VDHL2,T2EB1,T2BVD,T2RE1,T2AE,T2VE,T3EB1,T3BVE,T3RE1,T3AE,T3VE,T4EB2,T4BVE,T4RE2S,T4ADBA,T4VE,,,,,",
    "Observation25,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation26,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB1,T2BVE,T2RID,T2ADBA,T2VE,T3EB2,T3BVE,T3RE2D,T3ADHL,T3VE,,,,,,,,,,",
    "Observation27,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2DB,T2BVE,T2RID,T2AE,T2VE,,,,,,,,,,,,,,,",
    "Observation28,T1DB,T1BVE,T1RID,T1ADBA,T1VE,T2DB,T2BVE,T2RID,T2AE,T2VE,T3DB,T3BVE,T3RE2D,T3AE,T3VE,T4EB2,T4BVE,T4RE2D,T4ADHL,T4VE,,,,,",
    "Observation29,T1EB2,T1BVE,T1RI2,T1AE,T1VE,T2EB2,T2BVE,T2RI2,T2AE,T2VE,,,,,,,,,,,,,,,",
    "Observation30,T1DB,T1BVE,T1RE2S,T1AE,T1VE,T2EB2,T2BVE,T2RI2,T2ADHL,T2VE,,,,,,,,,,,,,,,",
    "Observation31,T1DB,T1BVE,T1RID,T1AE,T1VE,T2EB2,T2BVE,T2RE2S,T2ADBA,T2VE,T3EB2,T3BVE,T3RE2D,T3ADHL,T3VE,T4EB2,T4BVE,T4RE2D,T4AE,T4VDHL2,,,,,",
    "Observation32,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB2,T2BVE,T2RE2DP,T2ADHL,T2VDHL2,,,,,,,,,,,,,,,",
    "Observation33,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2DB,T2BVE,T2RE2DP,T2AE,T2VDHL2,,,,,,,,,,,,,,,",
    "Observation34,T1EB2,T1BVE,T1RE2D,T1ADHL,T1VE,T2EB1,T2BVE,T2RE1,T2ADBA,T2VE,,,,,,,,,,,,,,,",
    "Observation35,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB2,T2BVE,T2RID,T2AE,T2VDHL2,,,,,,,,,,,,,,,",
    "Observation36,T1DB,T1BVE,T1RID,T1AE,T1VE,T2EB2,T2BVE,T2RI2,T2AE,T2VE,T3EB2,T3BVE,T3RI2,T3ADBA,T3VE,T4EB1,T4BVE,T4RI2,T4ADBA,T4VE,T5EB1,T5BVE,T5RE1,T5ADBA,T5VE",
    "Observation37,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB2,T2BVE,T2RI2,T2AE,T2VDHL2,,,,,,,,,,,,,,,",
    "Observation38,T1EB2,T1BVE,T1RI2,T1AE,T1VE,T2EB1,T2BVE,T2RID,T2ADBA,T2VE,T3EB2,T3BVE,T3RE2D,T3ADHL,T3VEHL2,,,,,,,,,,",
    "Observation39,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB2,T2BVE,T2RE2S,T2AE,T2VE,,,,,,,,,,,,,,,",
    "Observation40,T1EB2,T1BVE,T1RE2D,T1ADBA,T1VDHL2,T2EB2,T2BVE,T2RE2D,T2ADHL,T2VDHL2B,,,,,,,,,,,,,,,",
    "Observation41,T1DB,T1BVE,T1RID,T1AE,T1VE,T2EB2,T2BVE,T2RID,T2AE,T2VE,,,,,,,,,,,,,,,",
    "Observation42,T1EB2,T1BVE,T1RI2,T1AE,T1VE,T2EB2,T2BVE,T1RE2DP,T2ADBA,T2VDHL2,,,,,,,,,,,,,,,",
    "Observation43,T1EB1,T1BVD,T1RE1,T1AE,T1VE,T2EB2,T2BVE,T2RE2D,T2ADBA,T2VE,,,,,,,,,,,,,,,",
    "Observation44,T1EB2,T1BVD,T1RE2S,T1AE,T1VE,T2EB1,T2BVE,T2RID,T2AE,T2VE,,,,,,,,,,,,,,,",
    "Observation45,T1EB1,T1BVD,T1RE1,T1AE,T1VE,T2EB2,T2BVE,T2RE2D,T2ADBA,T2VE,T3EB2,T3BVE,T3RI2,T3AE,T3VDHL2,,,,,,,,,,",
    "Observation46,T1EB1,T1BVD,T1RE1,T1AE,T1VE,T2EB1,T2BVE,T2RE1,T2ADBA,T2VE,T3EB1,T3BVE,T3RE1,T3AE,T3VE,T4EB2,T4BVE,T4RE2DP,T4AE,T4VEHL2,T5EB2,T5BVE,T5RE2S,T5AE,T5VDHL2",
    "Observation47,T1EB1,T1BVE,T1RID,T1AE,T1VE,T2EB1,T2BVE,T2RID,T2ADBA,T2VE,T3EB1,T3BVE,T3RID,T3ADBA,T3VE,T4EB1,T4BVD,T4RE1,T4ADBA,T4VE,,,,,",
    "Observation48,T1EB1,T1BVD,T1RE1,T1AE,T1VE,T2DB,T2BVE,T2VE,T2AE,T2VDHL2,T3EB1,T3BVD,T3RE1,T3AE,T3VE,T4EB1,T4BVE,T4RE1,T4ADBA,T4VE,T5DB,T5BVE,T5RE2S,T5AE,T5VE",
    "Observation49,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,,,,,,,,,,,,,,,,,,,,",
    "Observation50,T1DB,T1BVE,T1RE2S,T1ADBA,T1VE,T2DB,T2BVD,T2RE2S,T2ADBA,T2VE,T3DB,T3BVD,T3RE2S,T3AE,T3VE,,,,,,,,,,",
    "Observation51,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB1,T2BVD,T2RE1,T2AE,T2VE,,,,,,,,,,,,,,,",
    "Observation52,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB1,T2BVD,T2RE1,T2AE,T2VE,,,,,,,,,,,,,,,",
    "Observation53,T1DB,T1BVE,T1RID,T1AE,T1VE,T2EB2,T2BVE,T2RE2D,T2AE,T2VE,T3EB2,T3BVE,T3RE2D,T3AE,T3VDHL2,,,,,,,,,,",
    "Observation54,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB1,T2BVD,T2RE1,T2AE,T2VE,T3EB2,T3BVD,T3RE2S,T3AE,T3VEHL2,T4EB2,T4BVE,T4RE2D,T4AE,T4VEHL2,,,,,",
    "Observation55,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB2,T2BVE,T2RI2,T2AE,T2VDHL2,,,,,,,,,,,,,,,",
    "Observation56,T1EB1,T1BVD,T1RE1,T1AE,T1VE,T2EB1,T2BVE,T2RE1,T2ADBA,T2VE,,,,,,,,,,,,,,,",
    "Observation57,T1DB,T1BVE,T1RID,T1AE,T1VE,T2EB2,T2BVE,T2RE2S,T2AE,T2VE,T3EB2,T3BVE,T3RE2D,T3ADBA,T3VDHL2,,,,,,,,,,",
    "Observation58,T1DB,T1BVE,T1RID,T1AE,T1VE,T2EB1,T2BVE,T2RE1,T2ADBA,T2VE,,,,,,,,,,,,,,,",
    "Observation59,T1EB1,T1BVD,T1RE1,T1AE,T1VE,T2DB,T2BVE,T2RID,T2AE,T2VE,T3EB2,T3BVE,T3RID,T3ADBA,T3VE,T4EB2,T4BVE,T4RE2S,T4ADBA,T4VE,,,,,",
    "Observation60,T1EB1,T1BVE,T1RE1,T1ADBA,T1VE,T2EB1,T2BVE,T2RE1,T2AE,T2VDHL2B,T3EB1,T3BVE,T3RE1,T3AE,T3VE,T4DB,T4BVE,T4RI2,T4ADBA,T4VDHL2B,,,,,",
    ]

frequency_dict = {}
for i in range(len(data)):
    data[i] = data[i].replace("T1EB1", "TEB1").replace("T2EB1", "TEB1").replace("T3EB1", "TEB1").replace("T4EB1", "TEB1").replace("T5EB1", "TEB1").replace("T6EB1", "TEB1")\
                     .replace("T1EB2", "TEB2").replace("T2EB2", "TEB2").replace("T3EB2", "TEB2").replace("T4EB2", "TEB2").replace("T5EB2", "TEB2").replace("T6EB2", "TEB2")\
                     .replace("T1DB", "TDB").replace("T2DB", "TDB").replace("T3DB", "TDB").replace("T4DB", "TDB").replace("T5DB", "TDB").replace("T6DB", "TDB")\
                     .replace("T1BVE", "TBVE").replace("T2BVE", "TBVE").replace("T3BVE", "TBVE").replace("T4BVE", "TBVE").replace("T5BVE", "TBVE").replace("T6BVE", "TBVE")\
                     .replace("T1BVD", "TBVD").replace("T2BVD", "TBVD").replace("T3BVD", "TBVD").replace("T4BVD", "TBVD").replace("T5BVD", "TBVD").replace("T6BVD", "TBVD")\
                     .replace("T1RID", "TRID").replace("T2RID", "TRID").replace("T3RID", "TRID").replace("T4RID", "TRID").replace("T5RID", "TRID").replace("T6RID", "TRID")\
                     .replace("T1RI2", "TRI2").replace("T2RI2", "TRI2").replace("T3RI2", "TRI2").replace("T4RI2", "TRI2").replace("T5RI2", "TRI2").replace("T6RI2", "TRI2")\
                     .replace("T1RE2D", "TRE2D").replace("T2RE2D", "TRE2D").replace("T3RE2D", "TRE2D").replace("T4RE2D", "TRE2D").replace("T5RE2D", "TRE2D").replace("T6RE2D", "TRE2D")\
                     .replace("T1RE2S", "TRE2S").replace("T2RE2S", "TRE2S").replace("T3RE2S", "TRE2S").replace("T4RE2S", "TRE2S").replace("T5RE2S", "TRE2S").replace("T6RE2S", "TRE2S")\
                     .replace("T1RE1", "TRE1").replace("T2RE1", "TRE1").replace("T3RE1", "TRE1").replace("T4RE1", "TRE1").replace("T5RE1", "TRE1").replace("T6RE1", "TRE1")\
                     .replace("T1RE2DP", "TRE2DP").replace("T2RE2DP", "TRE2DP").replace("T3RE2DP", "TRE2DP").replace("T4RE2DP", "TRE2DP").replace("T5RE2DP", "TRE2DP").replace("T6RE2DP", "TRE2DP")\
                     .replace("T1AE", "TAE").replace("T2AE", "TAE").replace("T3AE", "TAE").replace("T4AE", "TAE").replace("T5AE", "TAE").replace("T6AE", "TAE")\
                     .replace("T1ADBA", "TADBA").replace("T2ADBA", "TADBA").replace("T3ADBA", "TADBA").replace("T4ADBA", "TADBA").replace("T5ADBA", "TADBA").replace("T6ADBA", "TADBA")\
                     .replace("T1ADHL", "TADHL").replace("T2ADHL", "TADHL").replace("T3ADHL", "TADHL").replace("T4ADHL", "TADHL").replace("T5ADHL", "TADHL").replace("T6ADHL", "TADHL")\
                     .replace("T1VE", "TVE").replace("T2VE", "TVE").replace("T3VE", "TVE").replace("T4VE", "TVE").replace("T5VE","TVE").replace("T6VE", "TVE")\
                     .replace("T1VEHL2", "TVEHL2").replace("T2VEHL2", "TVEHL2").replace("T3VEHL2", "TVEHL2").replace("T4VEHL2", "TVEHL2").replace("T5VEHL2", "TVEHL2").replace("T6VEHL2", "TVEHL2")\
                     .replace("T1VDHL2", "TVDHL2").replace("T2VDHL2", "TVDHL2").replace("T3VDHL2", "TVDHL2").replace("T4VDHL2", "TVDHL2").replace("T5VDHL2","TVDHL2").replace("T6VDHL2", "TVDHL2")\
                     .replace("T1VDHL2B", "TVDHL2B").replace("T2VDHL2B", "TVDHL2B").replace("T3VDHL2B", "TVDHL2B").replace("T4VDHL2B", "TVDHL2B").replace("T5VDHL2B","TVDHL2B").replace("T6VDHL2B", "TVDHL2B")\

# Define the list of search strings
search_strings = ['TEB1', 'TEB2', 'TDB', 'TBVE', 'TBVD', 'TRID', 'TRI2', 'TRE2D', 'TRE2S', 'TRE1', 'TRE2DP', 'TAE', 'TADBA', 'TADHL', 'TVE', 'TVEHL2', 'TVDHL2', 'TVDHL2B', 'N']

# Loop through the data and count the frequency of each search string
for i in range(len(data)):
    for search_str in search_strings:
        frequency = data[i].count(search_str)
        if search_str not in frequency_dict:
            frequency_dict[search_str] = [0] * len(data)
        frequency_dict[search_str][i] = frequency

# Convert the dictionary to a DataFrame and save to Excel
df = pd.DataFrame(frequency_dict)
df.index = ['Observation ' + str(i+1) for i in range(len(data))]
df.to_excel('frequencies.xlsx', index=True)

df = pd.read_csv('data3.csv', index_col=0)

# slice rows for observations 1 to 20 and calculate mean and standard deviation
obs1to20 = df.iloc[1:21,:]
obs1to20_mean = obs1to20.mean()
obs1to20_std = obs1to20.std()

# slice rows for observations 21 to 40 and calculate mean and standard deviation
obs21to40 = df.iloc[21:41,:]
obs21to40_mean = obs21to40.mean()
obs21to40_std = obs21to40.std()

# slice rows for observations 41 to 60 and calculate mean and standard deviation
obs41to60 = df.iloc[41:61,:]
obs41to60_mean = obs41to60.mean()
obs41to60_std = obs41to60.std()

print("Mean for observations 1 to 20:\n", obs1to20_mean)
print("Standard deviation for observations 1 to 20:\n", obs1to20_std)
print("Mean for observations 21 to 40:\n", obs21to40_mean)
print("Standard deviation for observations 21 to 40:\n", obs21to40_std)
print("Mean for observations 41 to 60:\n", obs41to60_mean)
print("Standard deviation for observations 41 to 60:\n", obs41to60_std)

# Write the mean and standard deviation to an Excel file
writer = pd.ExcelWriter('observations.xlsx')
obs1to20_mean.to_excel(writer, sheet_name='Obs 1-20 Mean')
obs1to20_std.to_excel(writer, sheet_name='Obs 1-20 Std')
obs21to40_mean.to_excel(writer, sheet_name='Obs 21-40 Mean')
obs21to40_std.to_excel(writer, sheet_name='Obs 21-40 Std')
obs41to60_mean.to_excel(writer, sheet_name='Obs 41-60 Mean')
obs41to60_std.to_excel(writer, sheet_name='Obs 41-60 Std')
writer.save()

