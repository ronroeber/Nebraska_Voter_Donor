#importing Libraries
import pandas as pd
import os
import string
import re
from matplotlib import pyplot as plt
import seaborn as sns
# %matplotlib inline #Jupiter Interactive Notebook display options.
import warnings
warnings.filterwarnings('ignore')

# FUTURE: write routine to download data, unpack and import
# my data structure .. is project directory
# ..\code (location of this file)
# ..\Donors 
# ..\Votors
# ..\Census
#Import File 
donors = pd.read_table('..\\Donors\\FORMB1AB.txt', sep='|')

#Rename columns to 'managable' names -- singleWord
donors.columns = ['CommitteeName', 'CommitteeID', 'DateReceived',
       'TypeofContributor', 'ContributorID', 'ContributionDate',
       'CashContribution', 'InKindContribution', 'UnpaidPledges',
       'ContributorLN', 'ContributorFN',
       'ContributorMI', 'ContributorOrg',
       'ContributorAddress', 'ContributorCity', 'ContributorState',
       'ContributorZip']

#Do some entry Clean up
#####
# Clean up mixed datatypes in Dataframe
donors.CommitteeName = donors.CommitteeName.astype('str')
donors.ContributorCity = donors.ContributorCity.astype('str')
donors.ContributorAddress = donors.ContributorAddress.astype('str')
donors.ContributorState = donors.ContributorState.astype('str')
donors.ContributorZip = donors.ContributorZip.astype('str')
donors.TypeofContributor = donors.TypeofContributor.astype('category')

# Fix dates - convert to datetime format - first to a string, then to datetime format
donors.ContributionDate = donors.ContributionDate.astype('str')
donors.DateReceived = donors.DateReceived.astype('str')
donors['ContributionDate'] = pd.to_datetime(donors['ContributionDate'])
donors['DateReceived'] = pd.to_datetime(donors['DateReceived'])

# Capitalize address entries
toUpper = ['ContributorCity', 'ContributorState', 'ContributorAddress']
for fieldname in toUpper:
    donors[fieldname]=donors[fieldname].str.upper()

# Remove punctuation from fields
# create list of punctuation in patterns that will be removed
rem = string.punctuation
pattern = r"[{}]".format(rem)
# create list of fields needing capitalization
removePunct = ['ContributorCity', 'ContributorAddress', 'ContributorFN', 'ContributorLN']
for fieldname in removePunct:
    donors[fieldname]=donors[fieldname].str.replace(pattern, "")
# Clean up the Address
# Standardize street directional prefix
directions=['NORTH', 'SOUTH', 'EAST', 'WEST']
for pointer in directions:
    donors['ContributorAddress'] = donors['ContributorAddress'].str.replace(pointer, pointer[0])

# Standardize street names
streets ={'STREET':'ST', 'AVENUE':'AVE', 'ROAD':'RD', 'CIRCLE':'CR', 'ROUTE':'RTE', 'PLACE':'PLA', 'PLAZA':'PLZ', 'PARKWAY':'PKWY', 'COURT':'CT'}
for way in streets.keys():
    donors['ContributorAddress'] = donors['ContributorAddress'].str.replace(way, streets[way])

# Filter the dataframe to hone in on individuals to match voterfile
# Define Filters
Filter1 = donors.TypeofContributor == 'I' # Individual Contributors
Filter2 = donors.CashContribution > 0
Filter3 = donors.InKindContribution > 0 # Remove NaN & Negative contributions
Filter4 = donors.ContributorState =='NE' # lost some. need to look for blank states

# Create wrangling database to fix up 
wrangleD = donors[Filter1 & (Filter2 | Filter3) & Filter4]