# Qld Sensitive Lists
### Sources
# Queensland Nature Conservation Act 1992
# **Sensitive**
# [Metadata - Queensland Confidential Species (Open Data Portal)](https://www.data.qld.gov.au/dataset/queensland-confidential-species)
# [Data](https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/qld-confidential-species.csv)
#
# **Codes**
# [Metadata - Qld Species codes](https://www.data.qld.gov.au/dataset/conservation-status-of-queensland-wildlife/resource/6344ea93-cadf-4e0c-9ff4-12dfb18d5f14)
# [Data](https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species-status-codes.csv)

# import essential libraries
#%%
import pandas as pd
import requests
import io
from ftfy import fix_encoding
#%%
# top level directory
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/"
basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"

#Species List and Species codes URLS
listurl = "https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/qld-confidential-species.csv"
codesurl =  "https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species-status-codes.csv"

#%%
print("Downloading Qld Species Status Codes")
response = requests.get(codesurl)
# Remove bad encoding
rtext = fix_encoding(response.text)
speciescodes = pd.read_csv(io.StringIO(rtext))

ncastatuscodes = speciescodes[speciescodes['Field'] == "NCA_status"][['Code','Code_description']]
ncastatuscodes['Code_description'] = ncastatuscodes['Code_description'].str.replace(" wildlife","")
ncastatuscodes.loc[ncastatuscodes['Code_description'] == "Critically endangered",'Code_description'] = "Critically Endangered"
ncastatuscodes.loc[ncastatuscodes['Code_description'] == "Near threatened",'Code_description'] = "Near Threatened"
#%%
endemicitycodes = speciescodes[speciescodes['Field'] == "Endemicity"][['Code','Code_description']]
# ebpc codes
epbccodes = speciescodes[speciescodes['Field'] == "EPBC_status"][['Code','Code_description']]

# Sensitive Lists
#%%
print("Downloading Qld Sensitive List")
response = requests.get(listurl)
# Remove bad encoding
rtext = fix_encoding(response.text)
confidentiallist = pd.read_csv(io.StringIO(rtext))

#%%
# join to get the codes

confidentiallist = pd.merge(confidentiallist,ncastatuscodes,left_on=['NCA status'],right_on=['Code'],how="left")
confidentiallist.drop(['Code'],axis=1,inplace=True)
confidentiallist = confidentiallist.rename(columns={'NCA status':'sourceStatus','Code_description':'status'})
# endemicity
confidentiallist = pd.merge(confidentiallist,endemicitycodes,left_on=['Endemicity'],right_on=['Code'],how="left")
confidentiallist.drop(['Code','Endemicity'],axis=1,inplace=True)
confidentiallist = confidentiallist.rename(columns={'Code_description':'endemicity'})
# epbc
confidentiallist = pd.merge(confidentiallist,epbccodes,left_on=['EPBC status'],right_on=['Code'],how="left")
confidentiallist.drop(['Code','EPBC status'],axis=1,inplace=True)
confidentiallist = confidentiallist.rename(columns={'Code_description':'epbcStatus'})
# rename fields
#%%
confidentiallist = confidentiallist.rename(columns=
{
    'Taxon Id':'taxonID',
    'Kingdom':'kingdom',
    'Class':'class',
    'Family':'family',
    'Scientific name':'scientificName',
    'Common name': 'vernacularName',
    'Taxon author':'scientificNameAuthorship',
    'Confidential':'confidential',
    'Significant':'significant'
})

#%%
confidentiallist.groupby(["kingdom","class"]).size()
# Replace kingdom and class values with scientific terms
confidentiallist.loc[confidentiallist["kingdom"] == "animals", "kingdom"] = "Animalia"
confidentiallist.loc[confidentiallist["kingdom"] == "plants", "kingdom"] = "Plantae"
confidentiallist.loc[confidentiallist["class"] == "land plants", "class"] = "Equisetopsida"
confidentiallist.loc[confidentiallist["class"] == "amphibians", "class"] = "Amphibia"
confidentiallist.loc[confidentiallist["class"] == "birds", "class"] = "Aves"
confidentiallist.loc[confidentiallist["class"] == "cartilaginous fishes", "class"] = "Chondrichthyes"
confidentiallist.loc[confidentiallist["class"] == "insects", "class"] = "Insecta"
confidentiallist.loc[confidentiallist["class"] == "malacostracans", "class"] = "Malacostraca"
confidentiallist.loc[confidentiallist["class"] == "mammals", "class"] = "Mammalia"
confidentiallist.loc[confidentiallist["class"] == "ray-finned fishes", "class"] = "Actinopterygii"
confidentiallist.loc[confidentiallist["class"] == "reptiles", "class"] = "Reptilia"
confidentiallist.loc[confidentiallist["class"] == "snails", "class"] = "Gastropoda"
confidentiallist.loc[confidentiallist["class"] == "arachnids", "class"] = "Arachnida"

confidentiallist.groupby(["kingdom","class"]).size()

#%%
#Write to CSV
print("Writing to CSV")
confidentiallist.to_csv(projectdir + "current-lists/sensitive-lists/QLD-sensitive.csv",encoding="UTF-8",index=False)
print("Processing finished")