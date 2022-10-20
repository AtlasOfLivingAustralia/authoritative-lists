# NSW Sensitive List
#%%
import urllib.request, json 
import pandas as pd

#%%
# top level directory
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/NSW-2022-10/"
# basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"

#%%
with urllib.request.urlopen("https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesNames") as url:
    data = json.loads(url.read().decode())

df = pd.json_normalize(data, record_path =['value'])
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
sensitive.to_csv(projectdir + "current-lists/sensitive-lists/NSW-sensitive-2022-10.csv",encoding="UTF-8",index=False)
print('Finished processing')


