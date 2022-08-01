# NSW conservation List

#%%
import urllib.request, json 
import pandas as pd

#%%
# top level directory
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/"
basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"

with urllib.request.urlopen("https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames") as url:
    data = json.loads(url.read().decode())
data = pd.json_normalize(data, record_path =['value'])

#%% Not sure why this is being done
# data.to_csv('testCon-NSW.csv', index= None)
#%%
# df = pd.read_csv("testCon-NSW.csv")
df = data
# Build dataframe
print('Start processing')
df = df[df.stateConservation != 'Not Listed']

conservation = df[(df['speciesID'] == df['taxonID'])]
conservation['status'] = conservation['stateConservation']

#%%
#Write to CSV
print("Writing to CSV")
conservation.to_csv(projectdir + "current-lists/conservation-lists/NSW-conservation.csv",encoding="UTF-8",index=False)
print('Finished processing')

