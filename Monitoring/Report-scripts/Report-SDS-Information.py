##############################################################################################
#
# SDS List Information Report
#  Extract SDS Information for each state
# For each sensitive species list:
# - Extract counts for Sensitive Assertions: generalised, alreadyGeneralised, not supplied
# - Extract species count for each
# - Write to markdown file
#
# Output information files to : ..\authoritative-lists\Monitoring\SDS-Information-<date>.md
##############################################################################################
#
import sys
import os
import urllib.request
import json
import certifi
import ssl
import datetime
import pandas as pd

projectDir = "/Users/oco115/PycharmProjects/authoritative-lists/"
outDir = projectDir + "Monitoring/"
sys.path.append(os.path.abspath(projectDir + "source-code/includes"))
monthStr = datetime.datetime.now().strftime('%Y%m%d')
import list_functions as lf
import configuration as cfg

##############################################################################################

def download_url(urlprefix: str, urlsuffix: str, dr: str):
    url = urlprefix + dr + urlsuffix
    print("download from: ", url)
    with urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as url:
        if url.status == 200:
            data = json.loads(url.read().decode())
            data = pd.json_normalize(data)

        else:
            # Handle the error
            print('Error in download_ala_list:', url.status)
    return data

def build_markdown(df):
    # Create markdown from dataframe
    # Add headers and description
    mheader = "## State Sensitive Species Lists - Occurrence Assertions Summary \n"
    mfooter = "\n"
    # Bulleted list text
    # blist = [
    #     "Generalised",
    #     "Already Generalised",
    #     "Not Supplied \n"
    # ]
    # Convert the list to a Markdown-formatted string with bullets
    # bliststr = "\n".join([f"* {item}" for item in blist])
    # description = f"\n The tables below summarise assertions:\n\n{bliststr}\n"
    description = "\n The table below summarises the occurrence record count for sensitive species \
                   within each of the states respectively.  \n The location of each occurrence should be generalised within the state\
                   and the value of **Not Supplied** should always be zero. \n\n"
    mdf = lf.df_to_markdown(df)
    # mdf = mheader + mdf + mfooter
    mdf = mheader + description + mdf + mfooter

    return mdf

def get_sds_info(state, sName, dr):
    # Get number of records in Species list
    urlprefix = 'https://api.ala.org.au/specieslist/ws/speciesList/'
    urlsuffix = ''
    data = download_url(urlprefix, urlsuffix, dr)
    splCt = data['itemCount'][0]

    # Generalised count
    urlprefix = 'https://api.ala.org.au/occurrences/occurrences/search?q=species_list_uid%3A'
    urlsuffix = '&fq=sensitive%3Ageneralised&fq=state%3A%22' + sName + '%22'
    data = download_url(urlprefix, urlsuffix, dr)
    genCt = data['totalRecords'][0]

    # Already Generalised
    urlsuffix = '&fq=sensitive%3AalreadyGeneralised&fq=state%3A%22' + sName + '%22'
    data = download_url(urlprefix, urlsuffix, dr)
    aGenCt = data['totalRecords'][0]

    # Not supplied
    urlsuffix =  '&fq=-sensitive%3A*&fq=state%3A%22' + sName + '%22'
    data = download_url(urlprefix, urlsuffix, dr)
    nsCt = data['totalRecords'][0]

    # Species count
    urlprefix = 'https://api.ala.org.au/occurrences/occurrences/facets?q=species_list_uid%3A'
    urlsuffix = '&facets=species'
    data = download_url(urlprefix, urlsuffix, dr)
    spCt = data['count'][0]
    totCt = genCt + aGenCt + nsCt
    values = [[state, dr, splCt, totCt, spCt, genCt, aGenCt, nsCt]]

    return values

##############################################################################################
# Production Sensitive Lists
drDict = {"ACT":"dr2627", "NSW":"dr487", "NT":"dr492",
          "QLD":"dr493", "SA":"dr884","TAS":"dr491",
          "VIC":"dr490", "WA":"dr467"}

stateNames = {"ACT":"Australian+Capital+Territory", "NSW":"New+South+Wales", "NT":"Northern+Territory",
          "QLD":"Queensland", "SA":"South+Australia","TAS":"Tasmania",
          "VIC":"Victoria", "WA": "Western+Australia"}

# drList = {"VIC":"dr490"}

cols = ['State', 'ListID', '#Species in list', 'Total Occurrences', 'Species count',
        'Generalised', 'Already Generalised', ' Not Supplied']

# Create dataframe of summary information
summarydf = pd.DataFrame(columns=cols)
for state, dr in drDict.items():
    sName = stateNames[state]
    summarydf = summarydf.append(pd.DataFrame(get_sds_info(state, sName, dr), columns=cols), ignore_index=True)

# Build markdown
mdsdf = build_markdown(summarydf)
mfile = outDir + 'SDS-Assertions-Information' + '.md'
print('Writing report to markdown file')
with open(mfile, 'w') as f:
    f.write(mdsdf)
print('Finished Processing')



