# Common functions for Authoritative Lists
#
import pandas as pd
import urllib.request
import json
import certifi
import ssl
import requests
import datetime
from vocab import api_values,conservation_list_urls,listsProd,listsTest,urlSuffix
from vocab import list_names_conservation_test,list_names_sensitive_test,authorize_url,token_url
from bs4 import BeautifulSoup
import time
from io import StringIO

from flask import Flask, request, redirect, render_template_string, session

def download_ala_specieslist(url: str):
    '''
    Download ALA species list.  Returns error if list isn't right, returns dataframe if list is correct
    '''
    with urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as url:
        if url.status == 200:
            data = json.loads(url.read().decode())
            data = pd.json_normalize(data)
        else:
            # Handle the error
            print('Error in download_ala_list:', url.status)
    return data

# TODO: confirm what this is doing
def kvp_to_columns(df):
    '''
    All data is in the KVP for lists(?).  Make sure the KVP data is in a pandas dataframe by itself.
    '''
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

# TODO: determine if this is necessary
# build the list URL here
# def build_list_url(drstr: str):
#     return "https://lists.ala.org.au/ws/speciesListItems/" + drstr + "?max=10000&includeKVP=true"
    
# TODO: go through this 
def get_changelist(testdr: str, proddr: str, ltype: str):
    
    # get old and new list urls    
    oldListUrl = listsProd + proddr + urlSuffix
    newListUrl = listsTest + testdr + urlSuffix

    # print(oldListUrl)
    # print(newListUrl)

    # download old list and turn it into pandas dataframe
    oldList = download_ala_specieslist(oldListUrl)
    oldList = kvp_to_columns(oldList)
    oldList = oldList.add_suffix("_old")

    # download new list and turn it into pandas dataframe
    newList = download_ala_specieslist(newListUrl)
    newList = kvp_to_columns(newList)
    newList = newList.add_suffix("_new")

    # check for new  and old names - left join new to old, drop any colums in names_old if they are na
    # conservation lists keep track of changes
    newVsOld = pd.merge(newList, oldList, how='left', left_on='name_new', right_on="name_old")
    columns = ['name_new','scientificName_new','commonName_new']
    if ltype == "C": 
        columns = columns + ['status_new']
    additions = newVsOld[newVsOld['name_old'].isna()][columns]
    additions.columns = additions.columns.str.replace("_new", "", regex=True)
    additions['listUpdate'] = 'added'

    # removed names - left join old to new, drop na new
    oldVsNew = pd.merge(oldList, newList, how='left', left_on='name_old',right_on="name_new")
    columns = ['name_old','scientificName_old','commonName_old']
    if ltype == "C": 
        columns = columns + ['status_old']
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

    # return changelist
    changeList = changeList.sort_values('name',ascending=True)
    return changeList

def read_list_url(url=None,
                  state=None):

    if ".xls" in url.lower() or ".xlsx" in url.lower():
        # check for skipping lines for the NT
        if state == "Northern Territory":
            xls = pd.ExcelFile(url) #,skiprows = [0,1,2,3])
            sheet_names = xls.sheet_names[:-1]
            df = pd.DataFrame()
            for name in sheet_names:
                df = pd.concat([df,pd.read_excel(xls,sheet_name=name,skiprows=[0,1,2,3])])
            if 'Fauna' in url:
                # introduced status?? remove??
                df = df[['FAMILY','GENUS','SPECIES','COMMON NAME',
                         'TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION']] # 'INTRODUCED STATUS'
                df['scientificName'] = df['SPECIES']
            else:
                df = df.rename(columns={'TAXON NAME': 'scientificName'})
                df = df[['FAMILY','GENUS','SPECIES','scientificName','COMMON NAME',
                         'TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION']] # 'INTRODUCED STATUS'
        else:
            xls = pd.ExcelFile(url,engine='openpyxl')
            if state == "Tasmania":
                df = pd.read_excel(xls,sheet_name=xls.sheet_names[0])
            else:
                raise ValueError("{} not taken into account:\n\n{}\n".format(state,url))
    elif ".csv" in url:
        df = pd.read_csv(url)
    elif ".json" in url:
        # this is for only ACT?
        response = requests.get(url)
        response_json = response.json()
        df = pd.DataFrame.from_records(response_json,index=[i for i in range(len(response_json))])
    elif "https" in url:
        return webscrape_list_url(url=url,state=state)
    else:
        response = requests.get(url)
        response_json = response.json()
        df = pd.DataFrame(response_json[api_values[state]])

    return df

def get_conservation_codes(state=None):

    if state is None:
        raise ValueError("Please provide a state for specific conservation codes.")
    
    if state == "Northern Territory":
        
        # get codes, rename and drop anything with NaNs
        xls = pd.ExcelFile(conservation_list_urls[state][0])
        codes = pd.read_excel(xls,sheet_name='CLASSIFICATION',skiprows=[x for x in range(13)])
        codes = codes.rename(columns={'Unnamed: 0': 'Code'})
        codes = codes.dropna(how='any')

        # remove spaces from Code 
        codes['Code'] = codes['Code'].str.replace(' ','')
        codes['Categories for classification'] = list(map(lambda x: x.split(' - ')[0] if '-' in x else x,
                                                             codes['Categories for classification']))
        return codes
    
    elif state == "Queensland":

        codes = pd.read_csv("https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species-status-codes.csv")

        # do something here...?
        codes = codes[codes['Field'] == "NCA_status"][['Code', 'Code_description']]

        # change code description to be capitalized
        codes.loc[codes['Code_description'] == "Critically endangered", 'Code_description'] = "Critically Endangered"
        codes.loc[codes['Code_description'] == "Near threatened", 'Code_description'] = "Near Threatened"

        return codes 
    
    elif state == "Tasmania":

        xls = pd.ExcelFile(conservation_list_urls[state][0])
        # first sheet name is species, second sheet is codes
        return pd.read_excel(xls,sheet_name=xls.sheet_names[1],skiprows=[0,6,7,8])[['Category code','Category']][0:4]
    
    elif state == "Western Australia":

        # get the data from the url
        response = requests.get(conservation_list_urls[state][0])
        
        # parse the html to get the spreadsheets
        soup =  BeautifulSoup(response.text, 'html.parser')
        strings = list(soup.find_all('a'))
        test = list(set([str(s) for s in strings if ".xlsx" in str(s)]))
        xls = pd.ExcelFile(test[0].split("\"")[1])
        
        # comment here
        if "Flora" in test[0]:
            df = pd.read_excel(xls,sheet_name=xls.sheet_names[4],skiprows=[1,2,3,4,5,6,7,8,9])[['Unnamed: 1','Unnamed: 2']]
        else:
            df = pd.read_excel(xls,sheet_name=xls.sheet_names[1],skiprows=[1,2,3,4,5,6,7,8,9])[['Unnamed: 1','Unnamed: 2']]
        df = df[~df['Unnamed: 2'].isna()]
        return df.rename(columns={
            'Unnamed: 1': 'Code',
            'Unnamed: 2': 'Category'
        }).reset_index(drop=True)
    
    else:
    
        return None
    
def webscrape_list_url(url=None,
                       state=None):

    if state == "EPBC":
        # get the data from the url
        response = requests.get(url)
        soup =  BeautifulSoup(response.text, 'html.parser')
        strings = list(soup.stripped_strings)
        test = list(set([s for s in strings if ".csv" in s]))
        if len(test) > 1:
            raise ValueError("There are more than one list - check that you have the correct one")
        else:
            return pd.read_csv(test[0])
    
    elif state == "Western Australia":

        # get the data from the url
        response = requests.get(url)

        # parse the html to get the spreadsheets
        soup =  BeautifulSoup(response.text, 'html.parser')
        strings = list(soup.find_all('a'))
        test = list(set([str(s) for s in strings if ".xlsx" in str(s)]))
        xls = pd.ExcelFile(test[0].split("\"")[1])
        temp = pd.read_excel(xls,sheet_name=xls.sheet_names[0])
        
        if 'fauna' in url:
            temp2 = temp.rename(columns={
                'Scientific name': 'scientificName',
                'Common name': 'vernacularName',
                'WA listing': 'status',
                'WA listing.1': 'sourceStatus'
            })
            temp2['family'] = None
            return temp2[['scientificName','vernacularName','family','status','sourceStatus']]
        elif 'flora' in url:
            codes = get_conservation_codes(state=state)
            temp2 = pd.merge(temp,codes,left_on='WA Status',right_on='Code')
            temp2 = temp2.rename(columns={
                'Taxon': 'scientificName',
                'Family': 'family',
                'Code': 'status',
                'Category': 'sourceStatus'
            })
            temp2['vernacularName'] = None
            return temp2[['scientificName','vernacularName','family','status','sourceStatus']]
        else:
            raise ValueError("There is a case that is not considered, or list doesn't contain 'flora' or 'fauna':\n\n{}\n".format(url))
        
    elif state == "New South Wales":      
        
        # figure out what this does....
        with urllib.request.urlopen(url,context=ssl._create_unverified_context()) as new_url:
            data = json.loads(new_url.read().decode())
        return pd.json_normalize(data, record_path =['value'])

    elif state == "Victoria":

        return pd.read_csv(url) #data, sep=",")

    else:

        # need to write a new loop
        print("do separate webscrape function for {} for now".format(state))
        import sys
        sys.exit()
    
def format_data_for_post(list_data=None,
                         state=None,
                         list_type=None):

    # { "listName": "list1", "listType": "TEST", "listItems": [ { "itemName": "item1", "kvpValues": [ { "key": "key1", "value": "value1" }, { "key": "key2", "value": "value2" } ] } ] }
    if list_type == "C":
        post_data = {"listName": list_names_conservation_test[state],"listType": "TEST","listItems": [None for i in range(list_data.shape[0])]} 
    elif list_type == "S":
        post_data = {"listName": list_names_sensitive_test[state],"listType": "TEST","listItems": [None for i in range(list_data.shape[0])]} 
    else:
        raise ValueError("Only two values are needed: 'C' for Conservation, 'S' for Sensitive")

    # print(list(list_data.columns).re)
    columns = list(list_data.columns)
    columns.remove('scientificName')
    
    # loop over each row to generate kvp values
    for i,row in list_data.iterrows():
        post_data["listItems"][i] = {"itemName": row['scientificName'],"kvpValues": [{x:row[x] for x in columns}]}

    # return data
    return post_data

def post_list_to_test(list_data=None,
                      druid=None,
                      state=None,
                      list_type=None):
    
    # format your data for posting to test
    data = format_data_for_post(list_data=list_data,state=state,list_type=list_type)

    # get authentication for server
    auth = get_authentication()
    
    # check if access token is expired
    test = is_access_token_expired(expires_at = auth['expires_at'])
    
    # if it is expired, run the following loop
    if test:

        # refresh tokens
        new_access_token, new_refresh_token, new_expires_in = refresh_access_token(refresh_token=auth['refresh_token'],
                        client_id = auth['id_token'])
        auth['access_token'] = new_access_token
        auth['refresh_token'] = new_refresh_token
        auth['expires_at'] = new_expires_in

        # write them to your file
        out_file = open('auth-confidential.json','w')
        json.dumps(auth,out_file)
        out_file.close()

    # create headers with authentication
    headers = {'user-agent': 'token-refresh/0.1.1', 'Authorization': 'Bearer {0}'.format(auth['access_token'])}

    # create the response and then return none
    response = requests.post("https://api.test.ala.org.au/specieslist/ws/speciesListPost/{}".format(druid),data=data,headers=headers)
    return None

def get_authentication():

    with open('auth-confidential.json') as f:
        return json.load(f)
    
def is_access_token_expired(expires_at=None):
    return expires_at is None or time.time() > expires_at

def refresh_access_token(refresh_token=None,
                         client_id = None):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
    }
    response = requests.post(token_url, data=data, headers={'Accept': 'application/json'})
    if response.status_code == 200:
        auth_response = response.json()
        new_access_token = auth_response['access_token']
        new_refresh_token = auth_response.get('refresh_token', 'N/A')
        new_expires_in = auth_response.get('expires_in', 'N/A')
        return new_access_token, new_refresh_token, new_expires_in
    else:
        return None, None, None