# NSW conservation List

#%%
import urllib.request, json 
import pandas as pd

#%%
# top level directory
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/NSW-2022-10/"

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
conservation = conservation[['taxonRank', 'kingdom' ,'class','order','family','genus','scientificName','specificEpithet','vernacularName','establishmentMeans','stateConservation','protectedInNSW','sensitivityClass','TSProfileID','countryConservation','dcterms_modified','speciesID','taxonID']]
conservation['status'] = conservation['stateConservation']
conservation = conservation.rename(columns={"stateConservation": "sourceStatus"})
conservation = conservation.rename(columns={"TSProfileID": "tsprofileid"})


#%%
#Write to CSV
print("Writing to CSV")
conservation.to_csv(projectdir + "current-lists/conservation-lists/NSW-conservation-2022-10.csv",encoding="UTF-8",index=False)
print('Finished processing')

