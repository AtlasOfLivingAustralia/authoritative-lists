# SA Conservation and Sensitive Lists
# Import fauna and vascular plants taxonomies from BDBSA and export lists for use in the ALA

import pandas as pd
import numpy as np
import requests
import io
import xlrd
from ftfy import fix_encoding
#%%
#%%
# top level directory
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/"
basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"

# Conservation Species Lists URLS
faunalisturl = "https://data.environment.sa.gov.au/Content/Publications/fauna-bdbsa-taxonomy.xlsx"
floralisturl =  "https://data.environment.sa.gov.au/Content/Publications/vascular-plants-bdbsa-taxonomy.xlsx"

#%%
# Process Fauna
# fauna = pd.read_excel("~/IdeaProjects/authoritative-lists/source-data/South Australia/fauna-bdbsa-taxonomy.xlsx",sheet_name="Taxonomic List")
#
print("Downloading SA Fauna Conservation List")
fauna = pd.read_excel(faunalisturl,sheet_name="Taxonomic List",skiprows=3)
# Fixes to fauna file:
# set dataframe names to line 2
# remove first 3 lines
# filter by NPW ACT Status is one of : E, V or R. Expand this value to the status field
# rename the columns to DwC friendly names
# remove some unwanted columns
print("Finished downloading SA Fauna List")
# fauna.columns = fauna.iloc[2]
# fauna = fauna[3:]
fauna = fauna[fauna['NPW ACT STATUS'].isin(['R','V','E'])]
fauna["status"] = np.where(fauna['NPW ACT STATUS'] == "E",'Endangered',
                           np.where(fauna['NPW ACT STATUS'] == "R",'Rare',
                                    np.where(fauna['NPW ACT STATUS'] == "V",'Vulnerable','UNK')))
fauna = fauna.rename(columns=
{
    'CLASSNAME (CLASSGROUP for Inverts)':'class',
    'ORDERNAME':'order',
    'FAMILYNAME':'family',
    'COMMON NAME':'vernacularName',
    'NSXCODE':'taxonID',
    'GENUS':'genus',
    'SP':'species',
    'SCIENTIFIC NAME':'scientificName',
    'NPW ACT STATUS':'sourceStatus',
    'NPW ACT STATUS COMMENTS':'npwActStatusComments',
    'EPBC ACT STATUS':'epbcStatus',
    'EPBC ACT STATUS COMMENTS':'epbcActStatusComments',
    'OFFICIAL SPECIES COMMENTS':'taxonRemarks',
    'DATE CREATED IN BDBSA':'bdbsaCreatedDate',
    'DATE TAXONOMY MODIFIED IN BDBSA':'bdbsaModifiedDate',
    'SPECIES AUTHOR':'scientificNameAuthorship',
    'SUBSPECIES AUTHOR':'subspeciesAuthor'
})
fauna.drop(['TEMPORARY TAXONOMIC SORT ORDER','SPECIESTYPE','INTRODUCED'],axis=1,inplace=True)

# Process Flora
flora = pd.read_excel(floralisturl,sheet_name="Taxonomic list")
# Fixes to flora file:
# * filter by NPW ACT Status is one of : E, V or R. Expand this value to the status field
# * rename the columns to DwC friendly names
# * remove some unwanted columns
#%%
flora = flora[flora['NPWSA ACT STATUS'].isin(['R','V','E','R*','V*','E*'])]
flora["status"] = np.where(flora['NPWSA ACT STATUS'].str.startswith('E'),'Endangered',
                           np.where(flora['NPWSA ACT STATUS'].str.startswith('R'),'Rare',
                                    np.where(flora['NPWSA ACT STATUS'].str.startswith('V'),'Vulnerable','UNK')))
#%%
flora = flora.rename(columns=
{
    'MAJOR GROUP':'majorGroup',
    'FAMILYNAME':'family',
    'COMMON NAME':'vernacularName',
    'NSXCODE':'taxonID',
    'GENUS':'genus',
    'SP':'species',
    'SUBSPECIES':'subSpecies',
    'SCIENTIFIC NAME':'scientificName',
    'NPWSA ACT STATUS':'sourceStatus',
    'NPWSA ACT STATUS COMMENT':'npwActStatusComments',
    'EPBC ACT STATUS':'epbcStatus',
    'EPBC ACT STATUS COMMENT':'epbcActStatusComments',
    'Weed of National Significance':'weedOfNationalSignificance',
    'NRM ACT Weed Status':'nrmActWeedStatus',
    'CREATIONDATE':'bdbsaCreatedDate',
    'MODIFIEDDATE':'bdbsaModifiedDate',
    'SPECIES with AUTHOR':'scientificNameAuthorship'
})
flora.drop(['TEMPORARY TAXONOMIC SORT ORDER','INTRODUCED'],axis=1,inplace=True)

#%%
saList = pd.concat([fauna,flora])
#Write to CSV
print("Writing to CSV")
salist.to_csv(projectdir + "current-lists/conservation-lists/NSW-conservation.csv",encoding="UTF-8",index=False)
print('Finished processing')


