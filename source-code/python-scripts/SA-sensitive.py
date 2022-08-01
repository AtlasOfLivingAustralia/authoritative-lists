# SA Sensitive Lists
# Import fauna and vascular plants taxonomies from BDBSA and export lists for use in the ALA
#%%
import pandas as pd
import numpy as np

# top level directory
projectdir = "/Users/oco115/PycharmProjects/auth-lists-updates/"
basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"

# Sensitive Species Lists URLS
senslisturl = "https://data.environment.sa.gov.au/Content/Publications/DEW_SAEnvironmentallySensitiveDataREGISTER.xls"

#%%
# Process Sensitive List
print('Downloading SA Sensitive List')
sasensitive = pd.read_excel(senslisturl)

sasensitive = sasensitive.rename(columns=
{
    'Date Listed':'dateListed',
    'Fauna/Flora':'faunaFlora',
    'SPECIESTYPE':'speciesType',
    'SA Species Code (NSXCODE)':'saSpeciesCode',
    'SPECIES':'scientificName',
    'COMMON NAME':'vernacularName',
    'Clarifier':'clarifier'
})
print('Finished downloading')
#%%
#Write to CSV
print('Writing to CSV')
sasensitive.to_csv(projectdir + "current-lists/sensitive-lists/SA-sensitive.csv",encoding="UTF-8",index=False)
print('Finished processing')


