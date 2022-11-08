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
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/WA-2022-10/"
basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"
# Species List and Species codes URLS
faunafile = "https://www.dpaw.wa.gov.au/images/Threatened%20and%20Priority%20Fauna%20List%207%20October%202022.xlsx"
florafile = "https://www.dpaw.wa.gov.au/images/Threatened%20and%20Priority%20Flora%20List%206%20October%202022.xlsx"
# faunafile = projectdir + "source-data/Threatened and Priority Fauna List 7 October 2022-fixed.xlsx"
# florafile = projectdir + "source-data/Threatened and Priority Flora List 6 October 2022-fixed.xlsx"

dfsightings = pd.DataFrame()

#%%
def readsource(sourceurl,rskip):
    skiprows=1
    dframe = pd.read_excel(sourceurl,skiprows=rskip)
    return dframe

#%%
# Process Fauna
#
print("Downloading WA Fauna Conservation List")
#%%
def processfauna(dframe):
    dframe = dframe.rename(columns=
    {
        'Scientific name': 'scientificName',
        'Common name': 'vernacularName',
        'Class': 'class',
        'WA listing': 'sourceStatus',
        'National listing': 'epbc status',
        'WA listing note': 'wa listing note',
        'Notes': 'taxonRemarks',
        # 'WA Status \n(ranking)': 'sourceStatus',
        # 'EPBC Status \n(ranking)': 'EPBC Status',
        # 'WA list name': 'taxonRemarks',
        'Kimberley': 'KIMB',
        'Pilbara': 'PILB',
        'Goldfields': 'GOLD',
        'Midwest': 'MWST',
        'Wheatbelt': 'WHTB',
        'South Coast': 'SCST',
        'Swan': 'SWAN',
        'South West': 'SWST',
        'Warren': 'WARR'
    })
    # Building 'DBCA Region' field. Original data has a column for each locality with 'X' marked
    # in cells where the species is found

    df = dframe[['KIMB', 'PILB', 'GOLD',
                'MWST', 'WHTB', 'SCST', 'SWAN', 'SWST', 'WARR']].copy()
    v = np.where(df == "X")
    dframe['dbca region'] = (pd.DataFrame(
        df.columns[v[1]], index=df.index[v[0]], columns=['result']
    ).groupby(level=0).agg(','.join).reindex(df.index)
                            )
    # drop location columns
    dframe = dframe.drop(['KIMB',
                        'PILB',
                        'GOLD',
                        'MWST',
                        'WHTB',
                        'SCST',
                        'SWAN',
                        'SWST',
                        'WARR'
                        ], axis=1)

    # %% Data Transformations
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

    dframe['status'] = dframe['sourceStatus'].replace(['P1', 'P2', 'P3', 'P4', 'VU', 'MI', 'CR', 'EN',
                                                     'OS', 'EX', 'EW', 'CD',
                                                     'MI (& VU or CR at subsp. level)',
                                                     'VU (& MI at sp. level)',
                                                     'CR (& MI at sp. level)',
                                                     'MI & P4'],
                                                    ['P1 - Poorly known species', 'P2 - Poorly known species',
                                                     'P3 - Poorly known species', 'P4 - Poorly known species',
                                                     'Vulnerable', 'Migratory', 'Critically Endangered', 'Endangered',
                                                     'Other specially protected fauna', 'Extinct', 'Extinct in Wild',
                                                     'Special Conservation Interest', 'Migratory', 'Vulnerable',
                                                     'Critically Endangered', 'Migratory & P4'
                                                     ])

    return dframe

#%%
def processflora(dframe):
    print('Transforming flora')

    # dframe = dframe.drop(['Name ID',
    dframe = dframe.drop(['Flowering Period',
                        'WA IUCN Criteria',
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

    dframe = dframe.rename(columns=
                         {'Name ID': 'taxonId',
                          'Taxon': 'scientificName',
                          'WA Status': 'sourceStatus',
                          'WA Rank': 'wa rank',
                          'DBCA Region': 'dbca region',
                          'DBCA District': 'dbca district',
                          'Distribution': 'verbatimLocality',
                          'EPBC': 'epbc status',
                          'Notes': 'taxonRemarks'
                          })
    dframe['status'] = dframe['sourceStatus'].replace(['T', 'X', 1, 2, 3, 4],
                                                    ['Threatened Flora', 'Presumed Extinct',
                                                     'P1 - Poorly known species', 'P2 - Poorly known species',
                                                     'P3 - Poorly known species', 'P4 - Poorly known species'])

    return dframe

#%%
def builddf(df1,df2):
    # Concatenate dataframes
    dfsightings = pd.DataFrame()
    dfsightings = pd.concat([df1, dfsightings], axis=0, ignore_index=True, sort=False)
    dfsightings['verbatimLocality'] = ""
    dfsightings['sensitivityZoneId'] = "WA"
    dfsightings = pd.concat([df2, dfsightings], axis=0, ignore_index=True, sort=False)
    return dfsightings

#%%
print("Downloading WA Fauna List")
fauna = readsource(faunafile, 1)
print("Finished Fauna download")
print("Downloading WA Flora List")
flora = readsource(florafile, 1)
print("Finished Flora download")

#%% Process Dataframes
fauna = processfauna(fauna)
flora = processflora(flora)

#%%
# Concatenate dataframes
dfsightings = builddf(fauna,flora)

#%% Write to CSV
print('writing Flora')
dfsightings.to_csv(projectdir + "current-lists/conservation-lists/WA-conservation-2022-10.csv",encoding="UTF-8",index=False)
dfsightings.to_csv(projectdir + "current-lists/sensitive-lists/WA-sensitive-2022-10.csv",encoding="UTF-8",index=False)
print('Completed writing')

# update the encoding on the final file / conservation is same as sensitive
#wa = pd.read_csv(fileurl,encoding='cp1252')
#wa.to_csv(fileurl, encoding="UTF-8",index=False)

#wa = wa.WATaxonId.astype(int)


