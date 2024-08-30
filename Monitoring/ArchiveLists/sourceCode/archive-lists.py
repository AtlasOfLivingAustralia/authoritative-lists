##############################################################################################
#
# Archive lists

# Archive criteria
# Lists are not authoritative lists and have one or more of the following criteria:
#  -  1 or less records
#  -  list type – “Test%”  (not case-sensitive)
#  -  list name contains "test%"   (not case-sensitive
#
#  Process
#
# - Download species list information for all lists via ALA Lists API
# - Extract lists to be archived - save to CSV
# - Extract lists not to be archived - save to CSV
# - Update collectory dataresource **isPrivate** for each list to be archived

# Urls and keys from config - keys cannot be displayed

# ALA API
#    baseUrl = 'https://api.ala.org.au/specieslist/ws/speciesList/?sort=dataResourceUid&' - Prod
#    baseUrl = 'https://api.ala.org.au/specieslist/ws/speciesList/?sort=dataResourceUid&' - Test

# Collectory
#    collectoryUrl = 'https://collections.ala.org.au/ws/' - Prod
#    collectoryUrl = 'https://collections-test.ala.org.au/ws/' - Test

##############################################################################################
#
import logging
import urllib.request
from pathlib import Path
import json
import requests
import certifi
import ssl
import datetime
import pandas as pd
import config as cfg

logger = logging.getLogger("Archive Lists")
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# formatter = logging.Formatte
# r('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# console.setFormatter(formatter)
logger.addHandler(console)

##############################################################################################

def main():

    # Set output directory
    cwd = Path.cwd()   # current working directory
    logger.info(f'Current working directory: {cwd}')
    outputdir = cwd / 'outputData'
    Path.mkdir(outputdir, exist_ok=True)
    listdf = download_listinfo()  # download list information for all lists
    archivedf = get_list_archive(listdf, outputdir)   # create dataframe with lists to update/archive
    # archivedf['cUpdStatus'] = archivedf.apply(lambda row: update_collectory_dr(row), axis=1) # update list to private
    archivedf['lUpdStatus'] = archivedf.apply(lambda row: update_list_dr(row), axis=1) # update list to private
    print('finished processing')

def download_listinfo():

    """
        Download Species List information via ALA API

        :return: dataframe of lists
    """

    baseurl = cfg.baseUrl
    limit = 1000
    offset = 0
    all_data = []
    logger.info(f'Downloading list info: ')
    while True:
        url = f'{baseurl}max={limit}&offset={offset}'
        logger.info(f'.... list: {url}')
        with urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as url:
            if url.status == 200:
                data = json.loads(url.read().decode())
                if len(data['lists']) == 0:
                    break
                data = pd.json_normalize(data)
                all_data.extend(data['lists'][0])
                offset += limit
            else:
                logger.info(f'Error downloading: {url} URl Status: {url.status}')
    df = pd.DataFrame(all_data)
    return df

def get_list_archive(infodf, outdir):
    """
     Load a file either from the cache or, if absent, retrieve it via SQL

     :param infodf Dataframe of lists
     :param outdir output directory

     :return: Dataframe of lists to be archived/updated
     """

    monthstr = datetime.datetime.now().strftime('%Y%m%d')
    authdf = infodf[(infodf['isAuthoritative'] == True)]      # authoritative lists
    notauthdf = infodf[~(infodf['isAuthoritative'] == True)]  # non-authoritative lists

    # Archive non-authoritative records that meet rules criteria
    archivedf = notauthdf[
        (notauthdf['listType'].str.contains('test', case=False, na=False)) |
        (notauthdf['listName'].str.contains('test', case=False, na=False)) |
        (notauthdf['itemCount'] <= 1)]
    archivedf['isPrivate'] = True   # set isPrivate flag to true for update

    # keep non-authoritative lists that are not to be archived
    keepdf = notauthdf[~notauthdf['dataResourceUid'].isin(archivedf['dataResourceUid'])]
    keepdf = pd.concat([authdf, keepdf], axis=0, ignore_index=True)

    # write lists to csv
    keepfile = f'{outdir}\lists-keep-{monthstr}.csv'
    archivefile = f'{outdir}\lists-archive-{monthstr}.csv'
    keepdf.to_csv(keepfile, encoding='utf-8', index=False)
    archivedf.to_csv(archivefile, encoding='utf-8', index=False)

    # ouptut list record counts
    currlistct = len(infodf)
    isauthct = len(authdf)
    nonauthct = len(notauthdf)
    checkct = len(keepdf) + len(archivedf)
    lt1rec = (notauthdf['itemCount'] <= 1).sum()
    typetest = (notauthdf['listType'].str.contains('test', case=False, na=False)).sum()
    nametest = (notauthdf['listName'].str.contains('test', case=False, na=False)).sum()

    logger.info(f'  ')
    logger.info(f'Current total number lists: {currlistct}')
    logger.info(f'Number authoritative lists: {isauthct}')
    logger.info(f'Number non-authoritative lists: {nonauthct}')
    logger.info(f'    - # lists with less than 2 records: {lt1rec}')
    logger.info(f'    - # Lists type value contains text test: {typetest}')
    logger.info(f'    - # lists name value contains text test: {nametest}')

    logger.info(f'Number of lists to keep: {len(keepdf)}')
    logger.info(f'Number of lists to archive: {len(archivedf)}')
    logger.info(f'Check record count (keep + archive): {checkct}')

    return archivedf


def update_collectory_dr(row) -> str:
    """
    Update list - set isPrivate flag in collectory DR

    :param row: list information from dataframe
    :return str: Update request response code
    """

    drID = row['dataResourceUid']
    jstr = row.to_dict()
    url = cfg.collectoryUrl + "dataResource/" + drID
    authorization = cfg.collectoryApiKey
    # logger.debug("POST %s to %s", row['json_string'], url)
    logger.debug("POST to %s", url)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": authorization
    }
    try:
        with requests.post(url, json=jstr, headers=headers) as response:
            if response.status_code == 200 or response.status_code == 201:
                return str(response.status_code)
            else:
                response.raise_for_status()
    except Exception as e:
        logger.error("Error in creating %s: %s for %s", url, jstr, e)
        response.raise_for_status()

# def update_list_dr(row) -> str:
#     """
#     Update list - set isPrivate flag in list
#
#     :param row: list information from dataframe
#     :return str: Update request response code
#     """
#
#     drID = row['dataResourceUid']
#     jstr = row.to_dict()
#     # get list items from list
#     url = f'{cfg.litemsUrl}{drID}'
#     logger.info(f'.... list: {url}')
#     with urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as url:
#         if url.status == 200:
#             data = json.loads(url.read().decode())
#             # data = pd.json_normalize(data)
#         else:
#             logger.info(f'Error downloading: {url} URl Status: {url.status}')
#     # df = pd.DataFrame(data)
#     print('got to here')
#     return url.status

def update_list_dr(row) -> str:
    """
    Update list - set isPrivate flag in list

    :param row: list information from dataframe
    :return str: Update request response code
    """

    authorization = cfg.collectoryApiKey
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": authorization
    }

    druid = row['dataResourceUid']
    jstr = row.to_dict()      # List info detail
    # get list items
    url = f'{cfg.litemPrefix}{druid}{cfg.litemSuffix}'
    logger.info(f'Downloading list items from: ')
    logger.info(f'.... list: {url}')
    with urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as url:
        if url.status == 200:
            data = json.loads(url.read().decode())   # List item detail
            # data = pd.json_normalize(data)
        else:
            logger.info(f'Error downloading: {url} URl Status: {url.status}')
    # Append list info and list data then update
    jstr['listItems'] = data
    # post the data to test

    try:
        # response = requests.post("https://lists-test.ala.org.au/ws/speciesList/{}?".format(druid),
        #                          data=json.dumps(data_for_post), headers=headers)
        with requests.post("https://lists-test.ala.org.au/ws/speciesList/{}?".format(druid),
                                 data=json.dumps(jstr), headers=headers) as response:
        # with requests.post(url, json=jstr, headers=headers) as response:
            if response.status_code == 200 or response.status_code == 201:
                return str(response.status_code)
            else:
                response.raise_for_status()
    except Exception as e:
        print(' the updated died')
        logger.error("Error in creating %s: %s for %s", url, jstr, e)
        response.raise_for_status()
    print ('got to here ok')
    return url.status

# def format_data_for_post(list_data=None,
#                          state=None,
#                          list_type=None):
#     '''
#     Turn a pandas dataframe into a dictionary for posting to the lists test environment
#     '''
#
#
#         post_data = {"listName": list_names_sensitive_test[state], "listType": "TEST",
#                      "listItems": [None for i in range(list_data.shape[0])]}
#
#
#     # get all values needed for posting
#     columns = list(list_data.columns)
#     columns.remove('scientificName')
#
#     # loop over each row to generate kvp values
#     for i, row in list_data.iterrows():
#         post_data["listItems"][i] = {"itemName": row['scientificName'], "kvpValues": []}
#         for x in columns:
#             post_data["listItems"][i]["kvpValues"].append({"key": x, "value": row[x]})
#
#     # return data
#     return post_data


# Main processing

if __name__ == "__main__":
    main()


