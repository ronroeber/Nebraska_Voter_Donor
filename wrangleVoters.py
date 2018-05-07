# create dataframe compatable with analysis
#importing Libraries
import pandas as pd
import os
from matplotlib import pyplot as plt
import seaborn as sns
# %matplotlib inline # uncomment if using in Jupyter labs
import warnings
warnings.filterwarnings('ignore')

# write routine to download data, unpack and import

#Import File 
os.chdir('C:\\Users\\ronro\\OneDrive\\Data Science\\NeDP\\Voters\\')
voters = pd.read_excel('VoterSample.xlsx', 'Sheet1')