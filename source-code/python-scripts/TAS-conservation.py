# TAS Conservation list
#%%
import pandas as pd

# top level directory
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/"
basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"

# Conservation species URL
taslisturl = "https://nre.tas.gov.au/Documents/TasThreatenedSpecies.XLS"

#%%
# Process Sensitive List
print('Downloading TAS Sensitive List')
tasconservation = pd.read_excel(taslisturl)
# tas = pd.read_csv(fileurl,encoding='cp1252')
print('Finished downloading')

#%% Process dataframe

# do conversion of status - see conservation list csv file for values oops missed it before
tasconservation = tasconservation.rename(columns={'Origin': 'sourceOrigin',
                                                  'species': 'scientificName',
                                                  'Authority': 'authority',
                                                  'Common Name': 'vernacularName',
                                                  'Family': 'family',
                                                  'sch': 'sourceStatus',
                                                  'EPBCA': 'epbcaStatus',
                                                  'Classification': 'class'
                                        })

tasconservation.drop(['Group', 'Flora/Fauna'], axis=1, inplace=True)


#%%
# Write to CSV
print('Writing to CSV')
tasconservation.to_csv(projectdir + "current-lists/conservation-lists/TAS-conservation.csv", encoding="UTF-8", index=False)
print('Finished processing')
