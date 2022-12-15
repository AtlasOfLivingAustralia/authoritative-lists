##
import pandas as pd
import requests
import json


projectdir = "/Users/oco115/PycharmProjects/iNaturalist-lists/"
inatcsv = "/Users/oco115/PycharmProjects/iNaturalist-lists/data/inaturalist-australia-9-conservation_statuses.csv"
outcsv = "/Users/oco115/PycharmProjects/iNaturalist-lists/data/inaturalist-australia.csv"
usercsv = "/Users/oco115/PycharmProjects/iNaturalist-lists/data/inaturalist-708886-update-statuses.csv"
apiurlbase = "https://api.inaturalist.org/v1/taxa/"

## Read inaturalist conservation statuses file
df = pd.read_csv(inatcsv,encoding='UTF-8')

# Retrieve all Australian records
df = df.dropna(subset=['place_display_name'])
df1 = df[df['place_display_name'].str.contains('Australia')]
df2 = df[df['place_display_name'].str.contains(', AU')]
dfaus = df1.append(df2, ignore_index=True)
dfx = df.dropna(subset=['authority'])
filterlist = ['Australia', 'Australia Exclusive Economic Zone', 'Australian Capital Territory, AU', 'Brisbane City, Cairns - Pt B, QL, AU', 'Christmas Island', 'New South Wales, AU', 'Norfolk Island', 'Norfolk Island (Phillip Island)', 'Northern Territory, AU', 'Rottnest Island, AU', 'South Australia, AU', 'South Australia, marine waters', 'South East Queensland, QL, AU', 'Tasmania, AU', 'Victoria, AU', 'Western Australia, AU', 'Yarrabah, QL, AU', 'Queensland, AU']
dfa = dfx.apply(lambda row: row[dfx['place_display_name'].isin(filterlist)])
dfaus1 = dfaus.append(dfa, ignore_index=True)

# Extract records for User 708886 (Peggy)
# Remove duplicates from append above first

dfaus1 = dfaus1.drop_duplicates(subset=None, inplace=False)
checkrecs = dfaus1[dfaus1['user_id']== 708886]
checkrecs['taxon_id'] = checkrecs['taxon_id'].astype(int)


#%%
#Retrieve taxon information and statuses from iNaturalist API
rlist = []
ct = 0
df = pd.DataFrame(columns=['id','taxonid','taxonname', 'taxonstatus', 'authority', 'taxonurl'])   # create empty dataframe with columns
for ind in checkrecs.index:
    # print('record count is: ', ct, 'taxonid is: ', taxonid)
    print(checkrecs['taxon_id'][ind], checkrecs['authority'][ind])
    print('record count is: ', ct, 'taxonid is: ', checkrecs['taxon_id'][ind], 'authority is: ', checkrecs['authority'][ind])
    apiurl = apiurlbase + str(checkrecs['taxon_id'][ind])
    response = requests.request("GET", apiurl)
    rlist.append(json.loads(response.text))
    numstatus = len(rlist[ct]['results'][0]['conservation_statuses'])
    # taxonpname = rlist[ct]['results'][0]['preferred_common_name']
    taxonid = checkrecs['taxon_id'][ind]
    inatid = checkrecs['id'][ind]
    authority = checkrecs['authority'][ind]
    taxonname = rlist[ct]['results'][0]['name']

    for i in range(numstatus):
        if rlist[ct]['results'][0]['conservation_statuses'][i]['authority'] == checkrecs['authority'][ind]:
            print('found value')
            taxonstatus = rlist[ct]['results'][0]['conservation_statuses'][i]['status']
            taxonurl = rlist[ct]['results'][0]['conservation_statuses'][i]['url']
            taxonlist = [inatid, taxonid, taxonname, taxonstatus, authority, taxonurl]
            df.loc[len(df)] = taxonlist
            break

    ct += 1
df.to_csv(usercsv,index = False,encoding='utf-8-sig')
print('finished')