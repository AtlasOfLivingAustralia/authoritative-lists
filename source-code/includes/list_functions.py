#%%
# Common functions for Authoritative Lists
#
#
import pandas as pd
import urllib.request
import json
import certifi
import ssl
import requests


def download_ala_list(url: str):
    with urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as url:
        data = json.loads(url.read().decode())
        data = pd.json_normalize(data)
        return data


def kvp_to_columns(df):
    d0 = pd.DataFrame()
    for i in df.index:
        kvpdf = pd.json_normalize(df.kvpValues[i])
        kvpdf = kvpdf.transpose()
        kvpdf.columns = kvpdf.loc['key']   # rename columns to the keys
        kvpdf.drop(['key'], inplace=True)  # drop the keys row
        kvpdf['id'] = df.id[i]
        kvpdf = pd.merge(df, kvpdf, "inner", on="id")
        d0 = pd.concat([d0, kvpdf])
    return d0


def get_changelist(newListUrl: str, oldListUrl: str):
    oldList = download_ala_list(oldListUrl)
    oldList = kvp_to_columns(oldList)
    newList = download_ala_list(newListUrl)
    newList = kvp_to_columns(newList)
    # new names
    newVsOld = pd.merge(newList, oldList, how='left', on='name', suffixes=('_new', '_old'))
    newVsOld = newVsOld[newVsOld['scientificName_old'].isna()][['name', 'commonName_new',
                                                                'scientificName_new', 'status_new']]
    newVsOld['listUpdate'] = 'added'
    # removed names
    oldVsNew = pd.merge(oldList, newList, how='left', on='name', suffixes=('_old', '_new'))
    oldVsNew = oldVsNew[oldVsNew['scientificName_new'].isna()][['name', 'commonName_old',
                                                                'scientificName_old', 'status_old']]
    oldVsNew['listUpdate'] = 'removed'
    # status changes
    statusChanges = pd.merge(newList, oldList, how='left', on='name', suffixes=('_new', '_old'))
    statusChanges = statusChanges[statusChanges['status_new'] !=
                                  statusChanges['status_old']][['name', 'commonName_new',
                                                                'scientificName_new', 'status_new', 'status_old']]
    statusChanges['listUpdate'] = 'status change'
    # union and display in alphabetical order and save locally
    changeList = pd.concat([newVsOld, oldVsNew])
    #changeList = changeList[['listUpdate','name', 'scientificName_x','commonName_x','status_x','status_y']].sort_values('name')
    return changeList

def gbifparse(indf):
    # GBIF Parser - returns binomial and trinomial names for scientificName
    namesonly = indf['name']
    url = "https://api.gbif.org/v1/parser/name"
    headers = {'content-type': 'application/json'}
    data = namesonly.to_json(orient="values")
    params = {'name': data}
    r = requests.post(url=url, data=data, headers=headers)
    results = pd.read_json(r.text)
    return results