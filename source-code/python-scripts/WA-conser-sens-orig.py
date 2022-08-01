# WA Conservation and Sensitive Lists
# WA has the same list for both conservation and sensitive lists
#import essential libraries
# import essential libraries
#%%
import pandas as pd
import numpy as np
# import requests
# import xlrd
# from ftfy import fix_encoding
#%%
# top level directory
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/"
basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"

#Species List and Species codes URLS
# faunalisturl = "https://www.dpaw.wa.gov.au/images/documents/plants-animals/threatened-species/Listings/Threatened%20and%20Priority%20Fauna%20List.xlsx"
# floralisturl = "https://www.dpaw.wa.gov.au/images/documents/plants-animals/threatened-species/Listings/Threatened%20and%20Priority%20Flora%20List%205%20December%202018.xlsx"

faunafile = projectdir + "source-data/Threatened and Priority Fauna List.xlsx"
florafile = projectdir + "source-data/Threatened and Priority Flora List.xlsx"

dfsightings = pd.DataFrame()
#%%
print("Downloading WA Fauna List")
# response = requests.get(faunalisturl)
fauna = pd.read_excel(faunafile)
# Remove bad encoding
print("Finished Fauna download")

#%%
# Rename columns

fauna = fauna.rename(columns=
{
    'Scientific name': 'scientificName',
    'Common name': 'vernacularName',
    'Class': 'class',
    'WA Status \n(ranking)': 'sourceStatus',
    'EPBC Status \n(ranking)': 'EPBC Status',
    'WA list name': 'taxonRemarks',
    'Kimberley':'KIMB',
    'Pilbara':'PILB',
    'Goldfields':'GOLD',
    'Midwest': 'MWST',
    'Wheatbelt':'WHTB',
    'South Coast':'SCST',
    'Swan':'SWAN',
    'South West':'SWST',
    'Warren': 'WARR'
})
# Building 'DBCA Region' field. Original data has a column for each locality with 'X' marked
# in cells where the species is found

df = fauna[['KIMB', 'PILB', 'GOLD',
       'MWST', 'WHTB', 'SCST', 'SWAN', 'SWST', 'WARR']].copy()

v = np.where(df =="X")
fauna['DBCA Region'] = (pd.DataFrame(
       df.columns[v[1]], index=df.index[v[0]], columns=['result']
   ).groupby(level=0).agg(','.join).reindex(df.index)
)
#drop location columns
fauna = fauna.drop(['KIMB',
                    'PILB',
                    'GOLD',
                    'MWST',
                    'WHTB',
                    'SCST',
                    'SWAN',
                    'SWST',
                    'WARR'
], axis=1)
#%% Data Transformations
# Data Transformations
# WA Status
# 	T	Threatened Flora (Declared Rare Flora - Extant)
# 	X	Presumed Extinct (Declared Rare Flora - Extinct)
# 	1	Priority One - Poorly known Species
# 	2	Priority Two - Poorly known Species
# 	3	Priority Three - Poorly known Species
# 	4	Priority Four - Rare, Near Threatened and other species in need of monitoring
#
print('Transforming fauna')

fauna['status'] = fauna['sourceStatus'].replace(['P1', 'P2', 'P3', 'P4', 'VU',  'MI',  'CR',  'EN',
                                                 'OS', 'EX', 'EW', 'CD',
                                                 'MI (& VU or CR at subsp. level)',
                                                 'VU (& MI at sp. level)',
                                                 'CR (& MI at sp. level)',
                                                 'MI & P4'],
                                                ['P1 - Poorly known species','P2 - Poorly known species',
                                                 'P3 - Poorly known species', 'P4 - Poorly known species',
                                                 'Vulnerable', 'Migratory', 'Critically Endangered', 'Endangered',
                                                 'Other specially protected fauna', 'Extinct', 'Extinct in Wild',
                                                 'Special Conservation Interest','Migratory','Vulnerable',
                                                 'Critically Endangered', 'Migratory & P4'
                                               ])

#%%
print("Downloading WA Flora List")
# flora = pd.read_excel(floralisturl,sheet_name="List 5 December 2018")
flora = pd.read_excel(florafile,skiprows=1)
# response = requests.get(floralisturl)
# Remove bad encoding
print("Finished Flora download")

#%% Rename columns
print('Transforming flora')

flora = flora.drop(['Name ID',
                    'DBCA District',
                    'Flowering Period',
                    'IUCN Criteria',
                    'Recovery Plan'
], axis=1)

# Data Transformations
# STATUS	Conservation status of taxon - refer to definitions.
# 	T	Threatened Flora (Declared Rare Flora - Extant)
# 	X	Presumed Extinct (Declared Rare Flora - Extinct)
# 	1	Priority One - Poorly known Species
# 	2	Priority Two - Poorly known Species
# 	3	Priority Three - Poorly known Species
# 	4	Priority Four - Rare, Near Threatened and other species in need of monitoring
#
# RANK	The threat category the taxon is recognised as in Western Australia (see definitions)
# 	CR	Critically Endangered
# 	EN	Endangered
# 	VU	Vulnerable
# 	EX	Extinct
#
# EPBC 	The category that the taxon is listed under the Commonwealth's Environmental Protection and Biodiversity Conservation Act 1999. Note this list is maintained by the Commonwealth and the official list should be sourced at the Commonwealth's website
# 	CR	Critically Endangered
# 	E	Endangered
# 	V	Vulnerable
# 	X	Extinct

flora = flora.rename(columns=
{   'Name ID': 'taxonId',
    'Taxon': 'scientificName',
    'Status': 'sourceStatus',
    'Distribution': 'verbatimLocality',
    'EPBC': 'EPBC Status'
})
flora['status'] = flora['sourceStatus'].replace(['T' ,'X', 1, 2, 3, 4],
                                                        ['Threatened Flora','Presumed Extinct',
                                                         'P1 - Poorly known species','P2 - Poorly known species',
                                                         'P3 - Poorly known species', 'P4 - Poorly known species'])

#%%
# Concatenate dataframes
dfsightings = pd.concat([fauna, dfsightings], axis=0, ignore_index=True, sort=False)
dfsightings['Rank'] =""
dfsightings['DBCA Region'] =""
dfsightings['verbatimLocality'] =""
dfsightings['sensitivityZoneId'] ="WA"
dfsightings = pd.concat([flora, dfsightings], axis=0, ignore_index=True, sort=False)

#%% Write to CSV
print('writing Flora')
dfsightings.to_csv(projectdir + "current-lists/conservation-lists/WA-conservation.csv",encoding="UTF-8",index=False)
dfsightings.to_csv(projectdir + "current-lists/sensitive-lists/WA-sensitive.csv",encoding="UTF-8",index=False)
print('Completed writing')

# update the encoding on the final file / conservation is same as sensitive
#wa = pd.read_csv(fileurl,encoding='cp1252')
#wa.to_csv(fileurl, encoding="UTF-8",index=False)

#wa = wa.WATaxonId.astype(int)


