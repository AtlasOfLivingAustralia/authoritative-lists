#%% md
# iNaturalist sensitive lists
# Taxa in iNaturalist have conservation statuses that the ALA is responsible for maintaining.
# The process for bulk loads is to submit the data to iNaturalist in December/January using provided templates
# and checklists:
#
# https://docs.google.com/spreadsheets/d/1yTwWh4d-lHeaBGCB9m70-HKEMtvrquHsPu3Zrgz9BcE/edit#gid=1531097917
#
# Current statuses per iNaturalist taxonID are available in the iNaturalist site export, accessible via an
# iNaturalist AU site admin and in this repository (inaturalist-australia-9-conservation_statuses.xls)

### Suggested approach:

# To update the statuses (eg for Qld), we need to:
# 1. Find the taxon name for each iNaturalist taxonID in an Australian place. We'll need to match the lists by taxon name.
# 2. We need to find:
#     * New - those on the Qld list that are not on the iNat list (the list I uploaded before had authority: `QLD DEHP`
#     and my user id is 708886).
#     * Update - those on the Qld list that need updating (probably most because I feel we should change the authority
#     text and try to link out to the wildnet page for each taxonID)
#     * Remove - I expect there will be a few of these
#%% md

#%%
import pandas as pd
import requests
import json
projectdir = "/Users/oco115/PycharmProjects/iNaturalist-lists/"
listdir = "/Users/oco115/PycharmProjects/authoritative-lists/current-lists/"
inatcsv = projectdir + "data/inaturalist-australia-9-conservation_statuses.csv"
outcsv = projectdir + "data/inaturalist-australia.csv"
usercsv = projectdir + "/data/inaturalist-708886-update-statuses.csv"
matchtaxoncsv = projectdir + "/data/inaturalist-qld-match.csv"
newtaxoncsv = projectdir + "/data/inaturalist-qld-newtaxon.csv"
apiurlbase = "https://api.inaturalist.org/v1/taxa/"
#%%
## Read inaturalist conservation statuses file
df = pd.read_csv(inatcsv, encoding='UTF-8')
pd.Series(list(df.columns))
#%% md
### Retrieve all Australian records

# Records are not consistent in place names/locality so we need to:
# 1. extract records with place_display_name containing 'Australia' or 'AU'
# 2. extract records manually identified with place_display_name in the list of other place names in australia that are present
# 3. Merge the 2 extracts - this will result in duplicates that need to be removed
#%%
# Identified Australian place names
filterlist = ['Australia', 'Australia Exclusive Economic Zone', 'Australian Capital Territory, AU', 'Brisbane City, Cairns - Pt B, QL, AU', 'Christmas Island', 'New South Wales, AU', 'Norfolk Island', 'Norfolk Island (Phillip Island)', 'Northern Territory, AU', 'Rottnest Island, AU', 'South Australia, AU', 'South Australia, marine waters', 'South East Queensland, QL, AU', 'Tasmania, AU', 'Victoria, AU', 'Western Australia, AU', 'Yarrabah, QL, AU', 'Queensland, AU']
#%%
# I have kept each iteration of the dataframe just for debugging/comparison purposes
dfna = df.dropna(subset=['place_display_name'])   # need to drop NA in order to search for
df1 = dfna[dfna['place_display_name'].str.contains('Australia')]
df2 = dfna[dfna['place_display_name'].str.contains(', AU')]
dfaus = df1.append(df2, ignore_index=True)
dfana = df.dropna(subset=['authority'])
dfana = dfana.apply(lambda row: row[dfana['place_display_name'].isin(filterlist)])
dfaus1 = dfaus.append(dfana, ignore_index=True)
dfaus1 = dfaus1.drop_duplicates(subset=None, inplace=False)
#%% md
### Extract records for User 708886 (Peggy)

#%%
checkrecs = dfaus1[dfaus1['user_id'] == 708886]
checkrecs['taxon_id'] = checkrecs['taxon_id'].astype(int)
#%%
rlist = []
ct = 0
dfextract = pd.DataFrame(columns=['id', 'taxonid', 'taxonname', 'taxonstatus', 'authority', 'taxonurl'])   # create empty dataframe with columns
#%%
# Retrieve taxon information and statuses from iNaturalist API
#%%
for ind in checkrecs.index:
    # print('record count is: ', ct, 'taxonid is: ', taxonid)
    print(checkrecs['taxon_id'][ind], checkrecs['authority'][ind])
    print('record count is: ', ct, 'taxonid is: ', checkrecs['taxon_id'][ind], 'authority is: ', checkrecs['authority'][ind])
    apiurl = apiurlbase + str(checkrecs['taxon_id'][ind])
    response = requests.request("GET", apiurl)
    rlist.append(json.loads(response.text))
    numstatus = len(rlist[ct]['results'][0]['conservation_statuses'])
    # taxonpname = rlist[ct]['results'][0]['preferred_common_name'] # This field is not always available
    taxonid = checkrecs['taxon_id'][ind]
    inatid = checkrecs['id'][ind]
    authority = checkrecs['authority'][ind]
    taxonname = rlist[ct]['results'][0]['name']
    # Loop through results in JSON record an extract conservation statuses
    # Note: there are multiple records for each species. We need to select the record that has 'authority' matching authority in the input dataset
    # Build final dataframe
    for i in range(numstatus):
        if rlist[ct]['results'][0]['conservation_statuses'][i]['authority'] == checkrecs['authority'][ind]:
            taxonstatus = rlist[ct]['results'][0]['conservation_statuses'][i]['status']
            taxonurl = rlist[ct]['results'][0]['conservation_statuses'][i]['url']
            taxonlist = [inatid, taxonid, taxonname, taxonstatus, authority, taxonurl]
            dfextract.loc[len(dfextract)] = taxonlist
            break

    ct += 1
#%%
# Write dataframe to csv for checking and future use
dfextract.to_csv(usercsv, index=False, encoding='utf-8-sig')
#%% md
### Extract unique authorities for each state
 # * find unique authorities
 # * manually determine lists for each state
#%%
authlist = df['authority'].unique().tolist()
print(authlist)
qldlocs = ['QLD DEHP', 'Queensland Government', 'Queensland Nature Conservation Act 1992']
# nswlocs = ['NSW Office of Environment & Heritage']
# actlocs = ['ACT Government']
# viclocs = ['VIC Government' 'Victoria Flora and Fauna Guarantee Act 1988', 'Victoria Flora and Fauna Guarantee Act 1988 ']
# salocs = ['SA DEWNR']
# walocs = ['WA Department of Environment and Convservation']
# ntlocs = ['NT NRETAS']
#%% md
### Process Qld
# * Retrieve ALA Qld sensitive species list
# * Extract Qld records from iNat dataframe based on Qld Locations
# * Create lists of taxon name for Sensitive List and iNat data, for searching
# * Create dataframes of records:
#    * in Qld Sensitive list and in iNat - matchdf
#    * in Qld Sensitive list but not in iNat -notmatchdf
#%%
qldsensitive = pd.read_csv(listdir + "sensitive-lists/QLD-sensitive.csv")
qldinat = dfextract[dfextract['authority'].isin(qldlocs)]   # Records for identified Qld Locations
# qldinat = df[df['authority'].isin(qldlocs)]   # Records for identified Qld Locations
# print(df['taxonstatus'].unique())
# qlddf
# qldsensitive.columns
# qldsensitive
#%%
taxsearch1 = qldinat['taxonname'].tolist()   # iNat taxon
taxsearch2 = qldsensitive['scientificName'].tolist()   # Qld sensitive List taxon
matchdf = qldinat[qldinat['taxonname'].isin(taxsearch2)]     # in Qld sensitive list and in iNat
nomatchdf = qldsensitive[~qldsensitive['scientificName'].isin(taxsearch1)]  # in Qld Sensitive list but not on iNat

#%% md
### Merge sensitive list and iNat dataframes to include all columns from both
# * Rename iNat dataframe column taxonname to scientificName to use as column in merge
# * Take the matched rows and compare with status in sensitive list
# * Merge List and iNat data frames with matching rows based on taxon
#%% md
### Records for : taxon matches found in both Sensitive list and iNat
#%%
qldinat1=qldinat.rename(columns={'taxonname' : 'scientificName'})
taxmatch=qldinat1.merge(qldsensitive, how='inner', on=['scientificName'])
#%%
taxmatch.to_csv(matchtaxoncsv, index=False, encoding='utf-8-sig')
#%% md
### New records for iNat - taxon in Sensitive list but not in iNat
#%%
taxlistfound = taxmatch['scientificName'].tolist()  # iNat taxon
taxonnew = qldsensitive[~qldsensitive['scientificName'].isin(taxlistfound)]
taxonnew.to_csv(newtaxoncsv,index = False,encoding='utf-8-sig')
#%%
taxonnew.to_csv(newtaxoncsv,index = False,encoding='utf-8-sig')
#%% md
## Build iNaturalist Templates
# Based on templates found at: https://docs.google.com/spreadsheets/d/1yTwWh4d-lHeaBGCB9m70-HKEMtvrquHsPu3Zrgz9BcE/edit#gid=1531097917

#%% md
# New Records
# * Write New template if update required
#
# ** Question? How do we know the taxon_id and iNaturalist Place ID when these are new records???**
#%%
newtemplate = pd.DataFrame(columns=['Taxon Name','Status','Authority','IUCN equivalent','Description',
                                    'iNaturalist Place ID','url','Taxon Geoprivacy','Username','taxon_id'])
# newtemplate['Taxon Name'] = taxonnew['scientificName']
# newtemplate['Status'] = taxonnew['scientificName']
# newtemplate['Authority'] = taxonnew['scientificName']
# newtemplate['IUCN equivalent'] = taxonnew['scientificName']
# newtemplate['Description'] = taxonnew['scientificName']
# newtemplate['iNaturalist Place ID'] = taxonnew['scientificName']
# newtemplate['url'] = taxonnew['scientificName']
# newtemplate['Taxon Geoprivacy'] = taxonnew['scientificName']
# newtemplate['Username'] = taxonnew['scientificName']
# newtemplate['taxon_id'] = taxonnew['scientificName']
#%% md
# Records for Update- needs
# * Set status to standard terms
# * Compare status for sensitive vs iNat
# * Write Update template if update required
#%%
updatetemplate = pd.DataFrame(columns=['action', 'taxon_name', 'taxon_id', 'status', 'iucn equivalent',
                                    'authority','url', 'geoprivacy', 'place_id', 'username'])

print('finished')