import pandas as pd
import numpy as np
from google.colab import drive
from datetime import datetime

drive.mount('/content/drive')

cdd = pd.read_csv(r"/content/drive/MyDrive/Misc/Data.csv")
cdd.head(10)

## Turn timestamp column into a datetime object
cdd['Timestamp'] = pd.to_datetime(cdd['Timestamp'])

print(cdd['Compliance Analyst'].unique())

## Remove MXN entry from Compliance Analyst column
cdd = cdd[cdd['Compliance Analyst'].str.contains("MXN") == False]

## Group columns by compliance analysts / sort_values could also be a method to do this & wouldn't need the merges below?
grouped_data = cdd.groupby(['Compliance Analyst'], as_index=True).apply(lambda x: x['Timestamp'])

## Create dataframes for merging
transaction_dat = cdd.groupby(['Timestamp']).apply(lambda x: x['Transaction Amount'])
id_dat = cdd.groupby(['Timestamp']).apply(lambda x: x['External ID'])

## Return data into normal columnar format
grouped_data = grouped_data.reset_index(level=1, drop=True).to_frame()

def to_mins(time):
    return time.total_seconds() / 60

def convert_min(convert):
    return convert.apply(to_mins).round(2)

## Calculates for time spent subracting current row from previous row
new_data = grouped_data.assign(Time_Spent=lambda x: convert_min(x['Timestamp'].shift(-1) - x['Timestamp']))

## Replace any NaN numbers in dataframe with 0 
new_data.fillna(0, inplace=True)

print(new_data)

## Create replica of new_data dataframe for removing outliers
inter_quart_df = new_data.copy()
inter_quart_df = inter_quart_df['Time_Spent'].where(inter_quart_df['Time_Spent'] >= 0, 0).to_frame()

# inter_quart_df.to_csv(r'/content/drive/MyDrive/Andrew/check.csv')

def avg(time, count):
    return time / (count+1) 

## Create new dataframe to store Average Time Spent for each Compliance Analyst
sum_frame = pd.DataFrame(columns=['Compliance Analyst', 'Average Time Spent'])

## Put Compliance Analysts into a list for iteration
analyst_names = grouped_data.index.unique()

## Loop through each analyst and sums time spent values then calculates the average
for i in range(0, len(analyst_names)):
    analyst = new_data.loc[analyst_names[i]]
    ## This is needed as there were negative values on last record of timestamps for the compliance analysts after calculating time spent, so it excludes these negative values - this is also why there is a +1 to count to account for this
    analyst = analyst[analyst['Time_Spent'] > 0]
    save = analyst['Time_Spent'].sum()
    count = analyst['Time_Spent'].count()
    average = avg(save, count)
    ## Create a temp dataframe to store values then appends values to sum_frame dataframe
    tmp_df = pd.DataFrame([[analyst_names[i], average]], columns=['Compliance Analyst', 'Average Time Spent'])
    sum_frame = sum_frame.append(tmp_df, ignore_index=True)
    
## Makes Compliance Analyst the index of the dataframe then drops duplicate Compliance Analyst column
sum_frame.index = sum_frame['Compliance Analyst']
sum_frame = sum_frame.drop(columns=['Compliance Analyst'])

## Output looks similar to expected output +- a few decimal points, except for George Russells average
## I looked through the data to see if I could spot why but saw nothing too out of the ordinary besides some unusual looking external ID's and two record of George Russels with an Identical Timestamp @ '2022-04-29 14:39:46' which even when fixed does not account for the different in expected output
## I tried cleaning the data based on different external ID format but too many entries would be removed and it still wouldn't be close to the expected output for all compliance analysts
## Also, there is one record for Lewis Hamilton where there is an External ID instead of a transaction amount - I kept this record as it is the timespent and not the transaction amount I am after.
## I tried deleted some of the outliers on George Russells records to see if I could get closer to the expected output however it did not seem appropriate as I was deleting alot of relevant data 
## I compared the dataframe, new_data, against the original, CDD.csv, dataset and all George Russels records are seemingly correct and identifiable. 
print(sum_frame)

## Saves sum_frame dataframe to CSV
# sum_frame.to_csv(r'/content/drive/MyDrive/Andrew/sum_avg.csv')

## Turn timestamp into string and formats the time string value into am or pm
new_data['am/pm'] = new_data['Timestamp'].apply(lambda x: x.strftime('%p'))

## Removes compliance analyst as the index and makes it a column
new_data = new_data.reset_index()

## Merge and organize dataframes to view summary of data - also dropping duplicates based on identical timestamp and transaction amounts
merged_df = pd.merge(transaction_dat, new_data, on='Timestamp')
merged_df = pd.merge(id_dat, merged_df, on='Timestamp')
## Drops duplicates under George Russells records on merge due to identical timestamp
merged_df.drop_duplicates(subset=['Timestamp', 'Transaction Amount'], inplace=True)
merged_df.loc[:, 'Time_Spent' ] = np.where(merged_df['Time_Spent'] < 0, 0, merged_df['Time_Spent'])
merged_df = merged_df.reindex(columns=['Timestamp', 'Compliance Analyst', 'External ID', 'Transaction Amount', 'am/pm', 'Time_Spent'])
merged_df = merged_df.sort_values(by=['Compliance Analyst', 'Timestamp'], ascending=[False, True])

print(merged_df)

# merged_df.to_csv(r'/content/drive/MyDrive/Andrew/Merged.csv')



## Calculates quartile 3 and quartile 1 of dataframe
q3, q1 = inter_quart_df['Time_Spent'].quantile([0.75, 0.25])

# inter_quart_df.to_csv(r'/content/drive/MyDrive/Andrew/intquart.csv')

## Calculates the interquartile range
quart_range = q3 - q1

## Calculates the upper and lower bound range of values, upperbound being 2321.215 and lowerbound being -1323.625 due to the low q1 and high q3 value aswell as highly skewed data as 'Time_Spent' has values in the 10's and some near 100,000 including one at 484742 
## With these upper and lower bound values - my output is far above the expected output in the test instructions 
## I tried to decrease the upperbound value to what was given as an example which was 1262 minutes, but the values are still considerably above the expected output
## I tried the Z-Score method but that only identified extreme outliers and did not make values closer to expected output
## I manually looked through the data and everything is correctly within the upper and lowerbound values.
## I also compared data to original dataset to see if there any discrepencies, but everything seems to be correct.
upper, lower = q3 + (1.5* quart_range),  q1 - (1.5 * quart_range)
# upper, lower = 1262, qL - (1.5 * quart_range)
print(upper, lower)

## Makes the dataframe only contain data within the upper and lower bound range
inter_quart_df = inter_quart_df[(inter_quart_df['Time_Spent'] > lower) & (inter_quart_df['Time_Spent'] < upper)]

## Creating new dataframe to store interquartile average summary
inter_sum_avg = pd.DataFrame(columns=['Compliance Analyst', 'Average Time Spent'])

## Alternate avg function as negative numbers changed to 0 so not necessary to add +1 to count (note: possibly -1 to count??? as some negative values fall below the lowerbound?? still does not change average drastically enough to fit expected output)
def avg2(time, count):
    return time / count

for i in range(0, len(analyst_names)):
    analyst = inter_quart_df.loc[analyst_names[i]]
    save = analyst['Time_Spent'].sum()
    count = analyst['Time_Spent'].count()
    average = avg2(save, count)
    ## Create a temp dataframe to store values then appends values to sum_frame dataframe
    tmp_df = pd.DataFrame([[analyst_names[i], average]], columns=['Compliance Analyst', 'Average Time Spent'])
    inter_sum_avg = inter_sum_avg.append(tmp_df, ignore_index=True)

print(inter_sum_avg)
# inter_sum_avg.to_csv(r'/content/drive/MyDrive/Andrew/inter_quart_sum.csv')


