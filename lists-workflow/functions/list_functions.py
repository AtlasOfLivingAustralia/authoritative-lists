# Common functions for Authoritative Lists
#
import pandas as pd
import urllib.request
import json
import certifi
import ssl
import requests
import datetime
from vocab import api_values,conservation_list_urls
from bs4 import BeautifulSoup

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

# def df_to_markdown(df, y_index=False):
#     from tabulate import tabulate
#     blob = tabulate(df, headers='keys', tablefmt='pipe')
#     if not y_index:
#         # Remove the index with some creative splicing and iteration
#         return '\n'.join(['| {}'.format(row.split('|', 2)[-1]) for row in blob.split('\n')])
#     return blob

# def create_markdown_link(row, col, colurl):
#     # return markdown_text
#     return f"[{row[col]}]({row[colurl]})"

def wrap_text(text, width):
    return ' '.join([text[i:i + width] for i in range(0, len(text), width)])

# def list_to_markdown(ltype, cdf, sdf, mfile):
#     # Output dataframe to markdown
#     today = datetime.datetime.now().strftime('%Y-%m-%d')
#     if ltype=='P':
#         fheader = "## Authoritative Lists - Production:   " + today + "  \n"
#     else:
#         fheader = "## Authoritative Lists - Test:   " + today + "  \n"

#     # Conservation List
#     ltypeheader = "### Conservation Lists" + "  \n"
#     mdcdf = df_to_markdown(cdf)
#     mdcdf = fheader + ltypeheader + mdcdf

#     # Sensitive List
#     ltypeheader = "### Sensitive Lists" + "  \n"
#     mdsdf = df_to_markdown(sdf)
#     mdsdf = fheader + ltypeheader + mdsdf
#     with open(mfile, 'w') as f:
#         f.write(mdcdf)
#         f.write(mdsdf)

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
            print("has xls but not url")
            print(url)
            xls = pd.ExcelFile(url,engine='openpyxl')
            print(xls.sheet_names)
            import sys
            sys.exit()
            df = pd.read_excel(url)
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
    
def post_list_to_test(list_data=None,
                      druid=None):
    
    response = requests.post("https://api.test.ala.org.au/specieslist/ws/speciesListPost/{}".format(druid))

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
                'WA listing': 'Code',
                'WA listing.1': 'Category'
            })
            temp2['family'] = None
            return temp2[['scientificName','vernacularName','family','Code','Category']]
        elif 'flora' in url:
            codes = get_conservation_codes(state=state)
            temp2 = pd.merge(temp,codes,left_on='WA Status',right_on='Code')
            temp2 = temp2.rename(columns={
                'Taxon': 'scientificName',
                'Family': 'family'
            })
            temp2['vernacularName'] = None
            return temp2[['scientificName','vernacularName','family','Code','Category']]
        else:
            raise ValueError("There is a case that is not considered, or list doesn't contain 'flora' or 'fauna':\n\n{}\n".format(url))
        
    elif state == "New South Wales":      
        
        # figure out what this does....
        with urllib.request.urlopen(url,context=ssl._create_unverified_context()) as new_url:
            data = json.loads(new_url.read().decode())
        return pd.json_normalize(data, record_path =['value'])

    else:

        # need to write a new loop
        print("do separate webscrape function for {} for now".format(state))
        import sys
        sys.exit()