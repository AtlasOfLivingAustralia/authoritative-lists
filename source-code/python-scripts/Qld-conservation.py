# Qld Conservation and Sensitive Lists
### Sources
# Queensland Nature Conservation Act 1992
#
# **Conservation**
# [Metadata - Qld Species (Open Data Portal)](https://www.data.qld.gov.au/dataset/conservation-status-of-queensland-wildlife)
# [Data](https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species.csv)
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
listurl = "https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species.csv"
codesurl =  "https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species-status-codes.csv"

#%%
print("Downloading Qld Species Status Codes")
response = requests.get(codesurl)
# Remove bad encoding
rtext = fix_encoding(response.text)
# speciescodes = pd.read_csv(rtext)
speciescodes = pd.read_csv(io.StringIO(rtext))

# Process Conservation Lists
#%%
print("Downloading Qld Conservation List")
response = requests.get(listurl)
# Remove bad encoding
rtext = fix_encoding(response.text)
conservationlist = pd.read_csv(io.StringIO(rtext))

# speciescodes = pd.read_csv(projectdir + "source-data/QLD/species-status-codes.csv",encoding='cp1252')
ncastatuscodes = speciescodes[speciescodes['Field'] == "NCA_status"][['Code','Code_description']]
ncastatuscodes['Code_description'] = ncastatuscodes['Code_description'].str.replace(" wildlife","")
ncastatuscodes.loc[ncastatuscodes['Code_description'] == "Critically endangered",'Code_description'] = "Critically Endangered"
ncastatuscodes.loc[ncastatuscodes['Code_description'] == "Near threatened",'Code_description'] = "Near Threatened"

#%%
# conservationlist = pd.read_csv(projectdir + "source-data/QLD/species.csv",encoding='cp1252')
conservationlist = pd.merge(conservationlist,ncastatuscodes,left_on=['NCA_status'],right_on=['Code'],how="left")
conservationlist.drop(['Code'],axis=1,inplace=True)
conservationlist = conservationlist.rename(columns={'NCA_status':'sourceStatus','Code_description':'status'})

#%%
endemicitycodes = speciescodes[speciescodes['Field'] == "Endemicity"][['Code','Code_description']]
# expand endemicity
endemicitycodes = speciescodes[speciescodes['Field'] == "Endemicity"][['Code','Code_description']]
conservationlist = pd.merge(conservationlist,endemicitycodes,left_on=['Endemicity'],right_on=['Code'],how="left")
conservationlist.drop(['Code'],axis=1,inplace=True)
conservationlist = conservationlist.rename(columns={'Code_description':'Endemicity_description'})

#%%
#expand ebpc codes
epbccodes = speciescodes[speciescodes['Field'] == "EPBC_status"][['Code','Code_description']]
conservationlist = pd.merge(conservationlist,epbccodes,left_on=['EPBC_status'],right_on=['Code'],how="left")
conservationlist.drop(['Code'],axis=1,inplace=True)
conservationlist = conservationlist.rename(columns={'Code_description':'EPBC_status_description'})
conservationlist.drop(['EPBC_status'],axis=1,inplace=True)

#%%
# any without a status?
conservationlist[conservationlist['status'].isna()].groupby(["Class","Endemicity_description"]).size()
conservationlist = conservationlist.rename(columns=
{
    'Taxon_Id':'taxonID',
    'Kingdom':'kingdom',
    'Class':'class',
    'Family':'family',
    'Scientific_name':'scientificName',
    'Common_name': 'vernacularName',
    'Taxon_author':'scientificNameAuthorship',
    'NCA_status':'sourceStatus',
    'EPBC_status_description':'epbcStatus',
    'Endemicity_description':'endemicity',
    'Significant':'significant',
    'Confidential':'confidential'
})
# remove empty or Least Concern status records
conservationlist = conservationlist[((conservationlist['status'] != "Least concern") & (conservationlist['status'].notna()))]

# Replace kingdom and class values with scientific terms
conservationlist.loc[conservationlist["kingdom"] == "animals", "kingdom"] = "Animalia"
conservationlist.loc[conservationlist["kingdom"] == "plants", "kingdom"] = "Plantae"
conservationlist.loc[conservationlist["class"] == "land plants", "class"] = "Equisetopsida"
conservationlist.loc[conservationlist["class"] == "amphibians", "class"] = "Amphibia"
conservationlist.loc[conservationlist["class"] == "birds", "class"] = "Aves"
conservationlist.loc[conservationlist["class"] == "cartilaginous fishes", "class"] = "Chondrichthyes"
conservationlist.loc[conservationlist["class"] == "insects", "class"] = "Insecta"
conservationlist.loc[conservationlist["class"] == "malacostracans", "class"] = "Malacostraca"
conservationlist.loc[conservationlist["class"] == "mammals", "class"] = "Mammalia"
conservationlist.loc[conservationlist["class"] == "ray-finned fishes", "class"] = "Actinopterygii"
conservationlist.loc[conservationlist["class"] == "reptiles", "class"] = "Reptilia"
conservationlist.loc[conservationlist["class"] == "snails", "class"] = "Gastropoda"
conservationlist.loc[conservationlist["class"] == "arachnids", "class"] = "Arachnida"
conservationlist.groupby(["kingdom","class"]).size()
#%%
#Write to CSV
print("Writing to CSV")
conservationlist.to_csv(projectdir + "current-lists/conservation-lists/QLD-conservation.csv",encoding="UTF-8",index=False)
print("Processing finished")
