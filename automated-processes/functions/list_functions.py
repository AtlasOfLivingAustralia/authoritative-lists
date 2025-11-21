# Common functions for Authoritative Lists
#
import pandas as pd
import urllib.request
import json
import certifi
import ssl
import requests
from .vocab import api_values,conservation_list_urls,get_listsProd,get_listsTest,urlSuffix
from .vocab import list_names_conservation_test,list_names_sensitive_test,token_url
# from .vocab import upload_listsTest,ingest_listsTest,progress_listsTest
from bs4 import BeautifulSoup
import time

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

def kvp_to_columns(df):
    '''
    All data is in the KVP for lists.  Make sure the KVP data is in a pandas dataframe by itself.
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
    
def get_changelist(testdr: str, proddr: str, ltype: str):
    '''
    Determines changes between current lists in production ("old") and the lists we uploaded 
    to test ("new").  Returns a pandas dataframe with all the changes
    '''
    
    # get old and new list urls    
    oldListUrl = get_listsProd + proddr + urlSuffix
    newListUrl = get_listsTest + testdr + urlSuffix

    # download old list and turn it into pandas dataframe
    oldList = download_ala_specieslist(oldListUrl)
    oldList = kvp_to_columns(oldList)
    oldList = oldList.add_suffix("_old")
    columns_to_strip = ['name_old','scientificName_old']
    oldList[columns_to_strip] = oldList[columns_to_strip].apply(lambda x: x.str.strip())
    oldList = oldList.fillna(value='') # fill all None values since it's the new default

    # download new list and turn it into pandas dataframe
    newList = download_ala_specieslist(newListUrl)
    newList = kvp_to_columns(newList)
    newList = newList.add_suffix("_new")
    columns_to_strip = ['name_new','scientificName_new']
    newList[columns_to_strip] = newList[columns_to_strip].apply(lambda x: x.str.strip())

    # check for new  and old names - left join new to old, drop any columns in names_old if they are na
    # conservation lists keep track of changes
    newVsOld = pd.merge(newList, oldList, how='left', left_on=['name_new'], right_on=['name_old'])
    columns = ['name_new','scientificName_new']
    if ltype == "C": 
        columns = columns + ['status_new']
    additions = newVsOld[newVsOld['name_old'].isna()][columns]
    additions['listUpdate'] = 'added'

    # removed names - left join old to new, drop na new
    oldVsNew = pd.merge(oldList, newList, how='left', left_on=['name_old'],right_on=['name_new'])
    columns = ['name_old','scientificName_old']
    if ltype == "C": 
        columns = columns + ['status_old']
    removals = oldVsNew[oldVsNew['name_new'].isna()][columns]
    removals.columns = removals.columns.str.replace("_old", "", regex=True)
    removals['listUpdate'] = 'removed'

    # status changes - only check status changes for conservation list
    if ltype=='C':
        statusChanges = pd.merge(newList, oldList, how='inner', left_on=['name_new','vernacularName_new'], right_on=['name_old','vernacularName_old'])
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
    '''
    Determine what type of parsing is needed for each URL
    '''

    if ".xls" in url.lower() or ".xlsx" in url.lower():
        # check for skipping lines for the NT
        if state == "NT":
            xls = pd.ExcelFile(url) #,skiprows = [0,1,2,3])
            sheet_names = xls.sheet_names[:-1]
            df = pd.DataFrame()
            for name in sheet_names:
                df = pd.concat([df,pd.read_excel(xls,sheet_name=name,skiprows=[0,1,2,3])])
            if 'Fauna' in url:
                df = df[['FAMILY','GENUS','SPECIES','COMMON NAME',
                         'TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION']] # 'INTRODUCED STATUS'
                df['scientificName'] = df['SPECIES'].copy()
            else:
                df = df.rename(columns={'TAXON NAME': 'scientificName'})
                df = df[['FAMILY','GENUS','SPECIES','scientificName','COMMON NAME',
                         'TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION']] # 'INTRODUCED STATUS'
        else:
            xls = pd.ExcelFile(url) #,engine='openpyxl')            
            if state == "TAS":
                df = pd.read_excel(xls) #,sheet_name=xls.sheet_names[0])
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
    '''
    Gets conservation codes for relevant states
    '''

    if state is None:
        raise ValueError("Please provide a state for specific conservation codes.")
    
    if state == "NT":
        
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
    
    elif state == "QLD":

        codes = pd.read_csv("https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species-status-codes.csv")

        # do something here...?
        codes = codes[codes['Field'] == "NCA_status"][['Code', 'Code_description']]

        # change code description to be capitalized
        codes.loc[codes['Code_description'] == "Critically endangered", 'Code_description'] = "Critically Endangered"
        codes.loc[codes['Code_description'] == "Near threatened", 'Code_description'] = "Near Threatened"

        return codes 
        
    elif state == "WA":

        # get the data from the url
        response = requests.get(conservation_list_urls[state][0])
        
        # parse the html to get the spreadsheets
        soup =  BeautifulSoup(response.text, 'html.parser')
        strings = list(soup.find_all('a'))
        test = list(set([str(s) for s in strings if ".xlsx" in str(s)]))
        for url in test:
            if 'flora' in url.lower():
                # read the excel file
                if url.split("\"")[1][0:6] == "/sites":
                    xls = pd.ExcelFile("https://www.dbca.wa.gov.au{}".format(url.split("\"")[1]))
                else:
                    xls = pd.ExcelFile(url.split("\"")[1])
                
                df = pd.read_excel(xls,sheet_name=xls.sheet_names.index('Conservation Codes'),skiprows=[1,2,3,4,5,6,7,8,9])[['Unnamed: 1','Unnamed: 2']]
                df = df[~df['Unnamed: 2'].isna()]
                return df.rename(columns={
                    'Unnamed: 1': 'Code',
                    'Unnamed: 2': 'Category'
                }).reset_index(drop=True)
        
        return None
    
    else:
    
        return None
    
def webscrape_list_url(url=None,
                       state=None):
    '''
    Webscrape for new list files for certain states
    '''

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
    
    elif state == "WA":

        # get the data from the url
        response = requests.get(url)

        # parse the html to get the spreadsheets
        soup =  BeautifulSoup(response.text, 'html.parser')
        strings = list(soup.find_all('a'))
        urls = list(set([str(s) for s in strings if ".xls" in str(s)]))
        
        # initialise dataframe
        df_wa = pd.DataFrame()

        # loop over urls to find flora and fauna
        for url in urls:
            
            # read the excel file - amended if/elif/else statement to catch duplicates and lists we don't want
            if url.split("\"")[1][0:6] == "/sites" and 'Threatened and Priority' in url:
                xls = pd.ExcelFile("https://www.dbca.wa.gov.au{}".format(url.split("\"")[1]))
            elif 'Threatened and Priority' in url:
                xls = pd.ExcelFile(url.split("\"")[1])
            else:
                continue

            # first check for fauna
            if 'fauna' in url.lower():
                temp = pd.read_excel(xls,sheet_name=xls.sheet_names[0])
                temp2 = temp.rename(columns={
                    'Scientific name': 'scientificName',
                    'Common name': 'vernacularName',
                    'WA listing': 'status',
                    'WA listing.1': 'sourceStatus'
                })
                temp2['family'] = None
                temp2['kingdom'] = 'Animalia'
                df_wa = pd.concat([df_wa,temp2]).reset_index(drop=True)
                
            # then check for flora
            elif 'flora' in url.lower():
                # try this
                temp = pd.read_excel(xls,sheet_name=xls.sheet_names[0])[['Taxon', 'Family', 'WA Rank']]
                temp1 = pd.read_excel(xls,sheet_name=xls.sheet_names[1])[['Taxon', 'Family', 'WA Status']]
                temp = temp.rename(columns={'WA Rank': 'WA Status'})
                temp = pd.concat([temp,temp1])
                
                # get codes and ensure correct codes are in place
                codes = get_conservation_codes(state=state)
                codes = codes.replace({'Code': {1: 'P1', 2: 'P2', 3: 'P3', 4: 'P4'}})

                # replace numbers with correct codes
                temp = temp.replace({'WA Status': {1: 'P1', 2: 'P2', 3: 'P3', 4: 'P4'}})
                
                # replace 'T' with WA Rank value
                # temp['WA Status 2'] = [row[-1] if row[-2]=='T' else row[-2] for row in temp[['WA Status','WA Rank']].itertuples()]
                
                # merge codes and data
                temp2 = pd.merge(temp,codes,left_on='WA Status',right_on='Code')
                
                # rename columns
                temp2 = temp2.rename(columns={
                    'Taxon': 'scientificName',
                    'Family': 'family',
                    'Code': 'status',
                    'Category': 'sourceStatus'
                })

                # add a vernacular name column
                temp2['vernacularName'] = None
                temp2['kingdom'] = None

                # concat data
                df_wa = pd.concat([df_wa,temp2]).reset_index(drop=True)
        
        return df_wa[['scientificName','vernacularName','kingdom','family','status','sourceStatus']]
        
    elif state == "NSW":      
        
        # initialise data, then go through all the links to get all the data
        all_data = pd.DataFrame()
        another_url=True
        while another_url:
            data = requests.get(url).json()
            all_data = pd.concat([all_data,pd.json_normalize(data, record_path =['value'])])
            if '@odata.nextLink' not in data.keys():
                another_url = False
            else:
                url = data['@odata.nextLink']
            
        return all_data

    elif state == "VIC":

        return pd.read_csv(url) #data, sep=",")

    else:

        # need to write a new loop
        print("do separate webscrape function for {} for now".format(state))
        import sys
        sys.exit()
    
def format_data_for_post(list_data=None,
                         state=None,
                         list_type=None):
    '''
    Turn a pandas dataframe into a dictionary for posting to the lists test environment
    '''
    # Check which type of list is being passed and create the post_data dict accordingly
    if list_type == "C":
        post_data = {"listName": list_names_conservation_test[state],"listType": "TEST","listItems": [None for i in range(list_data.shape[0])]} 
    elif list_type == "S":
        post_data = {"listName": list_names_sensitive_test[state],"listType": "TEST","listItems": [None for i in range(list_data.shape[0])]} 
    else:
        raise ValueError("Only two values are needed: 'C' for Conservation, 'S' for Sensitive")

    # get all values needed for posting
    columns = list(list_data.columns)
    columns.remove('scientificName')
    
    # loop over each row to generate kvp values
    for i,row in list_data.iterrows():
        post_data["listItems"][i] = {"itemName": row['scientificName'],"kvpValues": []}
        for x in columns:
            post_data["listItems"][i]["kvpValues"].append({"key": x, "value": row[x]})
    
    # return data
    return post_data

def post_list_to_test(list_data=None,
                      druid=None,
                      state=None,
                      list_type=None,
                      args=None):
    '''
    Posts formatted data to test with authentication checks
    '''
    
    # format your data for posting to test
    auth=get_authentication_info(args=args,test=True)
    '''
    druid=None,
    filename=None,
    args=None

    # format headers
    headers = {#'X-ALA-userId': auth['profile']['email'],
               'Authorization': 'Bearer {}'.format(auth['access_token']),
               'Accept': 'application/json',
               'user-agent': 'authoritative-lists/1.0.0'}

    
    # create a binary string and data for file upload
    with open('data/temp-new-lists/{}'.format(filename), 'rb') as f:
        files = {
            'file': (filename, f.read(), 'text/csv')
        }

        data = {
			'description': 'CSV data upload',
			'format': 'csv'
		}

    # first, upload the list
    try:
        response_upload = requests.post(upload_listsTest,data=data,files=files,headers=headers) 
    except requests.exceptions.RequestException as e:  
        print(e)
    finally:
        if response_upload.status_code != 200:
            print("There was an error uploading the csv file.")
            print(response_upload)
            print(response_upload.text)

    # second, trigger an ingestion of a list
    upload_filename = response_upload.json()['localFile']
    try:
        response_ingest = requests.post('{}{}?file={}'.format(ingest_listsTest,druid,upload_filename),headers=headers)
    except requests.exceptions.RequestException as e:  
        print(e)
    finally:
        if response_ingest.status_code != 200 and response_ingest.status_code != 201:
            print("There was an error uploading the csv file.")
            print(response_ingest)
            print(response_ingest.text)

    # check progress of ingest; exit when done
    id = response_ingest.json()['id']
    response_test = requests.get(progress_listsTest.replace('{speciesListID}',id),headers=headers)
    if response_test.status_code != 200 and response_test.status_code != 201:
        raise ValueError("There was an error posting the data.  Error code {}: {}".format(response_test.status_code,response_test.text))
    completed = response_test.json()['completed']
    while not completed:
        time.sleep(15)
        response_test = requests.get(progress_listsTest.replace('{speciesListID}',id),headers=headers)
        completed = response_test.json()['completed']
    '''
    # format your data for posting to test
    data_for_post = format_data_for_post(list_data=list_data,state=state,list_type=list_type)
    auth=get_authentication_info(args=args,test=True)
    
    # create headers with authentication
    headers = {'Content-Type': 'application/json', 
               'X-ALA-userId': auth['profile']['email'], # unsure between this and userId
               'Authorization': 'Bearer {}'.format(auth['access_token'])}
    
    # post the data to test
    response = requests.post("https://lists-test.ala.org.au/ws/speciesList/{}?".format(druid),data=json.dumps(data_for_post),headers=headers)
    if response.status_code != 200 and response.status_code != 201:
        raise ValueError("There was an error posting the data.  Error code {}: {}".format(response.status_code,response.text))
    return None # was response   

def get_authentication_info(args=None,test=False,prod=False):

    # get authentication for server
    auth = read_authentication(args=args,test=test,prod=prod)

    # get client ID and secret ID
    client_id,client_secret = get_client_id_secret(args=args)
    
    # check if access token is expired
    test = is_access_token_expired(expires_at = auth['expires_at'])
    
    # if it is expired, run the following loop
    if test is not None:
        if test:

            # refresh tokens
            new_access_token, new_expires_in = refresh_access_token(refresh_token=auth['refresh_token'],
                                                                    client_id=client_id,
                                                                    client_secret=client_secret)
            auth['access_token'] = new_access_token
            auth['expires_at'] = time.time() + new_expires_in

            # Serializing json
            auth_json = json.dumps(auth, indent=4)
            
            # Writing to sample.json
            if test:
                with open(args.authentication_test, "w") as out_file:
                    out_file.write(auth_json)
                out_file.close()
            if prod:
                with open(args.authentication_test, "w") as out_file:
                    out_file.write(auth_json)
                out_file.close()
    
    return auth

def read_authentication(args=None,test=False,prod=False):
    '''
    Get relevant authentication information from json downloaded from website
    '''
    if test:
        with open(args.authentication_test) as f:
            return json.load(f)
    if prod:
        with open(args.authentication_test) as f:
            return json.load(f)
    return None
    
def get_client_id_secret(args=None):
    '''
    Get client ids and secret for posting data
    '''

    f = open(args.client_ids)
    for line in f:
        if 'client_id' in line:
            client_id = line.strip().split(" = ")[1]
        if 'client_secret' in line:
            client_secret = line.strip().split(" = ")[1]

    return client_id,client_secret
    
def is_access_token_expired(expires_at=None):
    '''
    Check if your JWT token is expired
    '''
    return expires_at is None or time.time() > expires_at

def refresh_access_token(refresh_token=None,
                         client_id = None,
                         client_secret = None):
    '''
    If the JWT token needs to be refreshed, this function refreshes the access token
    '''
    
    # set up payload
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    # get response
    response = requests.post(token_url, data=data, headers={'Accept': 'application/json'})
    
    # set new tokens in json
    if response.status_code == 200:
        auth_response = response.json()
        new_access_token = auth_response['access_token']
        new_expires_in = auth_response['expires_in']
        return new_access_token, new_expires_in
    else:
        print(response.status_code)
        print(response.text)
        raise ValueError("It is likely you need to manually regenerate JWT token - try this")
    
def get_s3_information(args=None):

    # initialise dict
    s3_info = {}

    # open file containing s3 bucket information
    f = open(args.s3_info)

    # get all values
    for line in f:
        key,value = line.strip().split(" = ")
        s3_info[key] = value

    return s3_info

def add_change_delete_list_values(list_type = None,
                                  list_data = None,
                                  state = None):
    
    if list_data is None:
        raise ValueError("Please provide a list for checking.")
    
    if list_type is None or list_type not in ['Sensitive','Conservation']:
        raise ValueError("Only Sensitive and Conservation are accepted for list_type values")
    
    if state is None:
        raise ValueError("Please provide a state.")
    
    # read in additions, changes, deletions
    for dir in ['Changes','Additions','Deletions']:
        df = pd.read_csv("{}/{}-{}-{}.csv".format(dir,state,list_type,dir))
        df = df.fillna('')
        if not df.empty:
            if dir == 'Additions':
                list_data = pd.concat([list_data,df]).reset_index(drop=True)
            elif dir == 'Changes':
                df = df.set_index('raw_scientificName')
                for name,row in df.iterrows():
                    if name in list(list_data['raw_scientificName']):
                        index = list_data.loc[list_data['raw_scientificName'] == name].index[0]
                        list_data.at[index,row['field']] = row['value']
            else:
                for i,row in df.iterrows():
                    index = list_data.loc[list_data['raw_scientificName'] == row['raw_scientificName']].index[0]
                    list_data.drop(index)

    return list_data