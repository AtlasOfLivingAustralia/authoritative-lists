##############################################################################################
#
# Identify Duplicate lists
# Output report
# Output information files to : ..\authoritative-lists\analysis\reports
##############################################################################################
#
import sys
import os
import datetime
import urllib.request
import json
import certifi
import ssl
import pandas as pd

projectdir = "/Users/oco115/PycharmProjects/authoritative-lists/"
outdir = projectdir + "Monitoring/DuplicateLists/"
sys.path.append(os.path.abspath(projectdir + "source-code/includes"))
import list_functions as lf
import configuration as cfg

monthStr = datetime.datetime.now().strftime('%Y%m%d')
##############################################################################################

def download_url(urlprefix: str, urlsuffix: str, drId: str):
    lUrl = urlprefix + drId + urlsuffix
    print("download from: ", lUrl)
    with urllib.request.urlopen(lUrl, context=ssl.create_default_context(cafile=certifi.where())) as lUrl:
        if lUrl.status == 200:
            data = json.loads(lUrl.read().decode())
            data = pd.json_normalize(data)
        else:
            # Handle the error
            print('Error in download_ala_list:', lUrl.status)
    return data, lUrl

def build_markdown(df, dStr):
    global outdir
    listUrl = 'https://lists.ala.org.au/speciesListItem/list/'
    # Create markdown from dataframe, add headers and description
    mheader = "## Species Lists Duplicate Record counts \n"
    mheader2 = "## Species Lists Duplicate Record counts \n"
    mfooter = "\n"
    # Format links for markdown
    print(f"... format dataResourceUid and create URL links")
    df['drUrl'] = listUrl + df['dataResourceUid']
    df['dataResourceUid'] = f'<font size="4" color="green">' + df['dataResourceUid'] + '</font>'
    df['dataResourceUid'] = df.apply(lambda row: lf.create_markdown_link(row, 'dataResourceUid', 'drUrl'), axis=1)
    df['itemCount'] = df['itemCount'].astype(int)
    df = df.sort_values(by='itemCount', ascending=False)
    # Group DataFrame by 'itemCount' and sort groups by 'itemCount' in descending order
    grouped = df.groupby('itemCount', sort=False)
    group_counts = grouped.size()
    mdf = ""
    for group_key, group_data in grouped:
        group_data = group_data.drop(['drUrl', 'itemCount', 'listType', 'dateCreated', 'lastUpdated'], axis=1)
        mdf += f"### Species lists with {group_key} records ({group_counts[group_key]}) \n\n"
        mdf += group_data.to_markdown(index=False) + "\n\n"

    mdf = mheader  + mdf + mfooter
    mfile = outdir + 'Species_Lists_Duplicates' + '.md'
    print('Writing report to markdown file')
    with open(mfile, 'w') as f:
        f.write(mdf)
    return mdf

# Production
# listsUrl = cfg.listsProd
# splists = lf.get_listDataframe(listsUrl)
# splists = splists.sort_values('listName', ascending=True)
# drop null columns
# splists = splists.dropna(axis=1, how='all')
# splists = splists.drop(dropcols, axis=1)
# splists.to_csv(outdir + "prod-species-lists.csv", index=False, encoding='utf-8')

# get specieslistItems for each list
# litemsdf = pd.DataFrame()
# litemsdf = splists.apply(lf.get_specieslistItems, axis=1)
# litemsdf = pd.concat([lf.get_specieslistItems(row, row_num,'') for row_num, row in splists.iterrows()], ignore_index=True)
# drop null columns
# litemsdf = litemsdf.dropna(axis=1, how='all')
# litemsdf.to_csv(outdir + "prod-specieslistitems.csv", index=False, encoding='utf-8')

# read species list data from saved CSVs
splists = pd.read_csv(outdir + 'prod-specieslists.csv', encoding='utf-8', dtype=str)
# splists = splists.dropna(axis=1, how='all')
dropcols = ['fullName', 'region', 'category', 'generalisation', 'authority', 'sdsType',
            'isInvasive', 'isThreatened', 'looseSearch', 'wkt', 'lastMatched']
splists = splists.drop(dropcols, axis=1)

litemsdf = pd.read_csv(outdir + 'prod-specieslistitems.csv', encoding='utf-8', dtype=str)
litemsdf = litemsdf.dropna(axis=1, how='all')

# Get species lists with duplicate record counts
dupCount = splists[splists.duplicated(subset=['itemCount'], keep=False)]
dupCount['itemCount'] = dupCount['itemCount'].astype(int)
dupCount = dupCount.sort_values(by='itemCount', ascending=False)
dupCount.to_csv(outdir + "prod-dupCount-drs.csv", index=False, encoding='utf-8')
mdsdf = build_markdown(dupCount, monthStr)

##############################################################################################

# print('Writing report to markdown')
# pmdfile = outdir + "Authoritative-lists-prod.md"
# tmdfile = outdir + "Authoritative-lists-test.md"
# lf.list_to_markdown("P", pconsdf, psensdf, pmdfile)
# lf.list_to_markdown("T", tconsdf, tsensdf, tmdfile)
print('Finished Processing')



