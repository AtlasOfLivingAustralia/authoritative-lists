# NSW Sensitive List
#%%
import urllib.request, json 
import pandas as pd

#%%
# top level directory
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/"
basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"

#%%
with urllib.request.urlopen("https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames") as url:
    data = json.loads(url.read().decode())

data = pd.json_normalize(data, record_path =['value'])

#%% Not sure why this needs to happen

# data.to_csv('testNSW.csv', index= None)
#%%
# df = pd.read_csv("testNSW.csv")
df = data
dictn = {"Category 3": "1km",
       "Category 2": "10km",
       "Category 1": "WITHHOLD"
}

#%%
select = ['Category 3','Category 2','Category 1']
#%%
df['generalisation'] = df['sensitivityClass']
#%%
df['generalisation'] = df['generalisation'].replace(dictn)
#%%
sensitive = df[(df['speciesID'] == df['taxonID']) & df['sensitivityClass'].isin(select)]

sensitive = sensitive[['taxonRank', 'kingdom' ,'class','order','family','genus','scientificName','specificEpithet','vernacularName','establishmentMeans','stateConservation','protectedInNSW','sensitivityClass','TSProfileID','countryConservation','dcterms_modified','speciesID','taxonID','generalisation']]
#%%
sensitive['status'] = sensitive['stateConservation']
sensitive = sensitive.rename(columns={"stateConservation": "sourceStatus"})
#%%
#Write to CSV
print("Writing to CSV")
sensitive.to_csv(projectdir + "current-lists/sensitive-lists/NSW-sensitive.csv",encoding="UTF-8",index=False)
print('Finished processing')


