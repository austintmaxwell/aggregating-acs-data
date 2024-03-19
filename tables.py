# Assignment header
"""
Austin Maxwell
March 3, 2024
Spring 2024 - Data 51100 - Section 002
Programming Assignment #7
"""

# Importing necessary libraries
import pandas as pd

# Initialize variables needed for algorithm
pums_data = r'/Users/austinmaxwell/ss13hil.csv'
table_nms = ["Descriptive Statistics of HINCP, grouped by HHT",
             "HHL vs. ACCESS - Frequency Table",
             "Quantile Analysis of HINCP - Household income (past 12 months)"]
access_map = {1:"Yes w/ Subsrc.", 2:"Yes, wo/ Subsrc.", 3:'No'}
hht_map = {1:"Married couple household",
           2:"Other family household:Male householder, no wife present",
           3:"Other family household:Female householder, no husband present",
           4:"Nonfamily household:Male householder:Living alone",
           5:"Nonfamily household:Male householder:Not living alone",
           6:"Nonfamily household:Female householder:Living alone",
           7:"Nonfamily household:Female householder:Not living alone"}
hhl_map = {1:"English Only",
           2:'Spanish',
           3:"Other Indo-European Languages",
           4:"Asian and Pacific Island Languages",
           5:"Other Language"}

# Creating helper functions
def hincp_stats(group_object):
    return {'mean': group_object.mean(),
            'std': group_object.std(),
            'count': group_object.count(),
            'min':group_object.min(),
            'max':group_object.max()}

# Set column width for output
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', None)

# Load the ss13hil.csv file into DataFrame
pums_df = pd.read_csv(pums_data)

# Create 3 tables
## TABLE 1: Statistics of HINCP
### Group HINCP data by HHT and collect statistical information
hincp_group = pums_df['HINCP'].groupby(pums_df['HHT'])
table1 = hincp_group.apply(hincp_stats).unstack()

### Rename index, remap index values, sort, and remove decimals
table1.index.names = ["HHT - Household/Family Type"]
table1.rename(index=hht_map, inplace=True)
table1.sort_values('mean', ascending=False, inplace=True)
table1[['count', 'min', 'max']] = table1[['count',
                                          'min',
                                          'max']].astype('int64')

### Display table 1
print(f"*** Table 1 - {table_nms[0]} ***")
print(table1)
print('')

## TABLE 2: HHL - Household language vs. ACCESS
### Remove NA values then create pivot table with percentages
table2 = pums_df[['HHL','ACCESS','WGTP']].dropna()
wgtp = table2['WGTP']
pivot = pd.pivot_table(table2,
                      index='HHL',
                      columns='ACCESS',
                      aggfunc=lambda x: f"{sum(x)/sum(wgtp):.2%}",
                      margins=True)

### Rename index, remap index values and rename columns
pivot.index.names = ["HHL - Household Language"]
pivot.rename(index = hhl_map, inplace=True)
pivot.rename(columns = access_map, inplace=True)

### Display table 2
print(f"*** Table 2 - {table_nms[1]} ***")
print("                                              sum")
print(pivot)
print('')

## TABLE 3: Quantile Analysis of HINCP
table3 = pums_df[['HINCP','WGTP']]

### Get quantiles of HINCP then group by quantilies to calculate stats
quantiles = pd.qcut(table3['HINCP'],
                    [0, 1/3, 2/3, 1],
                    labels=['low', 'medium', 'high'])
table3 = table3.groupby(quantiles).agg({'HINCP': ['min','max', 'mean'],
                                        'WGTP': 'sum'})

### Rename index values, rename columns and remove decimals
table3.index.names = ['HINCP']
table3.columns = ['min', 'max', 'mean', 'household_count']
table3[['min', 'max']] = table3[['min', 'max']].astype('int64')

### Display table 3
print(f"*** Table 3 - {table_nms[2]} ***")
print(table3)
