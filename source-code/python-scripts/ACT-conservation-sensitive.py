#%% ACT Conservation Threatened Species Lists
# API documentation:
# Home Page: https://dev.socrata.com/foundry/www.data.act.gov.au/9ikf-qahj
# API/Data Info: https://www.data.act.gov.au/Environment/ACT-Nature-Conservation-Threatened-Native-Species-/9ikf-qahj
# Code sample https://dev.socrata.com/foundry/www.data.act.gov.au/9ikf-qahj

#%%
# Conservation List: dr649
# Sensitive List: dr2627

#%%
import pandas as pd
from sodapy import Socrata
#%%
# top level directory
projectdir = "/Users/oco115/PycharmProjects/authoritative-lists/"

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("www.data.act.gov.au", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(www.data.act.gov.au,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.

#%%
results = client.get("9ikf-qahj", limit=20000)
# Convert to pandas DataFrame
resultsdf = pd.DataFrame.from_records(results)

#%% Write to CSV
print('writing ACT data')
resultsdf.to_csv(projectdir + "current-lists/sensitive-lists/ACT-sensitive-2022-10.csv",encoding="UTF-8",index=False)
print('Completed writing')



