#%%
# Common functions for Authoritative Lists
#
import pandas as pd
import urllib.request
import json
import certifi
import ssl
import requests
import datetime

def download_ala_specieslist(url: str):
    with urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as url:
        if url.status == 200:
            data = json.loads(url.read().decode())
            data = pd.json_normalize(data)
        else:
            # Handle the error
            print('Error in download_ala_list:', url.status)
    return data

def kvp_to_columns(df):
    d0 = pd.DataFrame()
    for i in df.index:
        if len(df['kvpValues'][i]) > 0:
            kvpdf = pd.json_normalize(df.kvpValues[i])
            kvpdf = kvpdf.transpose()
            kvpdf.columns = kvpdf.loc['key']   # rename columns to the keys
            kvpdf.drop(['key'], inplace=True)  # drop the keys row
            kvpdf['id'] = df.id[i]
            kvpdf = pd.merge(df, kvpdf, "inner", on="id")
            d0 = pd.concat([d0, kvpdf])
    return d0

def build_list_url(drstr: str):
    url = "https://lists.ala.org.au/ws/speciesListItems/" + drstr + "?max=10000&includeKVP=true"
    return url

def get_specieslistItems(row, row_num, numrows):
    drstr = row['dataResourceUid']
    url = "https://lists.ala.org.au/ws/speciesListItems/" + drstr
    # url = "https://lists.ala.org.au/ws/speciesListItems/" + drstr + "?max=10000&includeKVP=true"
    row =  download_ala_specieslist(url)
    return row

def get_changelist(testdr: str, proddr: str, ltype: str):
    oldListPref = "https://lists.ala.org.au/ws/speciesListItems/"
    newListPref = "https://lists-test.ala.org.au/ws/speciesListItems/"
    urlSuffix = "?max=10000&includeKVP=true"
    oldListUrl = oldListPref + proddr + urlSuffix
    newListUrl = newListPref + testdr + urlSuffix

    oldList = download_ala_specieslist(oldListUrl)
    oldList = kvp_to_columns(oldList)
    oldList = oldList.add_suffix("_old")
    newList = download_ala_specieslist(newListUrl)
    newList = kvp_to_columns(newList)
    newList = newList.add_suffix("_new")

    # new names - left join new to old, drop na old
    newVsOld = pd.merge(newList, oldList, how='left', left_on='name_new', right_on="name_old")
    columns = ['name_new','scientificName_new','commonName_new']
    if ltype == "C": columns = columns + ['status_new']
    additions = newVsOld[newVsOld['name_old'].isna()][columns]
    additions.columns = additions.columns.str.replace("_new", "", regex=True)
    additions['listUpdate'] = 'added'

    # removed names - left join old to new, drop na new
    oldVsNew = pd.merge(oldList, newList, how='left', left_on='name_old',right_on="name_new")
    columns = ['name_old','scientificName_old','commonName_old']
    if ltype == "C": columns = columns + ['status_old']
    removals = oldVsNew[oldVsNew['name_new'].isna()][columns]
    removals.columns = removals.columns.str.replace("_old", "", regex=True)
    removals['listUpdate'] = 'removed'

    # status changes - only check status changes for conservation list
    if ltype=='C':
        statusChanges = pd.merge(newList, oldList, how='inner', left_on='name_new', right_on='name_old')
        statusChanges = statusChanges[statusChanges['status_new'] != statusChanges['status_old']][['name_new','scientificName_new','commonName_new','status_new','status_old']]
        statusChanges.columns = statusChanges.columns.str.replace("_new", "", regex=True)
        statusChanges['listUpdate'] = 'status change'

    # union and display in alphabetical order and save locally
    if ltype == 'C':
        changeList = pd.concat([additions, removals, statusChanges])
    else:
        changeList = pd.concat([additions, removals])
    changeList = changeList.sort_values('name',ascending=True)
    return changeList

def gbifparse(indf):
    print('gbifparse')
    # GBIF Parser - returns binomial and trinomial names for scientificName
    namesonly = indf['name']
    url = "https://api.gbif.org/v1/parser/name"
    headers = {'content-type': 'application/json'}
    data = namesonly.to_json(orient="values")
    params = {'name': data}
    r = requests.post(url=url, data=data, headers=headers)
    results = pd.read_json(r.text)
    return results

def map_status(state, fname, dframe):
    codeslist = pd.read_csv(fname, dtype=str)
    codeslist['sourceStatus'] = codeslist['sourceStatus'].str.strip()
    codeslist['Status'] = codeslist['Status'].str.strip()
    code_status_dict = dict(zip(codeslist['sourceStatus'], codeslist['Status']))
    if 'sourcestatus' in dframe.columns:
        dframe = dframe.rename(columns={'sourcestatus' : 'sourceStatus'})
    dframe['status'] = dframe['sourceStatus'].map(code_status_dict)
    return dframe

# list_information_report functions

def get_listDataframe(listurl:str):
    print("get_listDataframe: ", listurl)
    limit = 1000
    offset = 0
    fulldf = pd.DataFrame()
    results_list = []

    while True:
        urlSuffix = "?max=" + str(limit) + "&offset=" + str(offset)
        listUrl = listurl + urlSuffix
        pList = download_ala_specieslist(listUrl)
        for item in pList['lists']:
            listdf = pd.DataFrame(columns=item[0].keys())
            for subitem in item:
                listdf.loc[len(listdf)] = [subitem[column] for column in listdf.columns]
        fulldf = pd.concat([fulldf, listdf], ignore_index=True)
        # Check if there are more results to fetch
        nrecs = pList['listCount'][0]
        if (offset + limit) < nrecs:
            # Update the offset for the next page
            offset += limit
        else:
           break
    return fulldf


def filterDataframe(fulldf, filter_dict):
    print('filterDataframe')
    # Create a boolean mask based on the key-value pair
    # drvals = filter_dict.values()
    filtered_df = fulldf[fulldf['dataResourceUid'].isin(filter_dict.values())]
    # Apply the mask to the DataFrame to get the filtered rows
    return filtered_df

def df_to_markdown(df, y_index=False):
    from tabulate import tabulate
    blob = tabulate(df, headers='keys', tablefmt='pipe')
    if not y_index:
        # Remove the index with some creative splicing and iteration
        return '\n'.join(['| {}'.format(row.split('|', 2)[-1]) for row in blob.split('\n')])
    return blob

def create_markdown_link(row, col, colurl):
    # return markdown_text
    return f"[{row[col]}]({row[colurl]})"

def wrap_text(text, width):
    return ' '.join([text[i:i + width] for i in range(0, len(text), width)])

def list_to_markdown(ltype, cdf, sdf, mfile):
    # Output dataframe to markdown
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if ltype=='P':
        fheader = "## Authoritative Lists - Production:   " + today + "  \n"
    else:
        fheader = "## Authoritative Lists - Test:   " + today + "  \n"

    # Conservation List
    ltypeheader = "### Conservation Lists" + "  \n"
    mdcdf = df_to_markdown(cdf)
    mdcdf = fheader + ltypeheader + mdcdf

    # Sensitive List
    ltypeheader = "### Sensitive Lists" + "  \n"
    mdsdf = df_to_markdown(sdf)
    mdsdf = fheader + ltypeheader + mdsdf
    with open(mfile, 'w') as f:
        f.write(mdcdf)
        f.write(mdsdf)