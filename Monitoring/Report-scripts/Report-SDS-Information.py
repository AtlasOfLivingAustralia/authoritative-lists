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

def build_markdown(df, mheader: str, mfooter: str):
    # Create markdown from dataframe
    # Add headers and description
    blist = [
        "Generalised",
        "Already Generalised",
        "Not Supplied \n"
    ]
    # Convert the list to a Markdown-formatted string with bullets
    bliststr = "\n".join([f"* {item}" for item in blist])
    description = f"\n The tables below summarise assertions:\n\n{bliststr}\n"
    mdf = lf.df_to_markdown(df)
    mdf = mheader + mdf + mfooter
    # mdf = mheader + description + mdf + mfooter

    return mdf

def get_sds_info(state, dr, alaProfile):
    # Get number of records in Species list
    urlprefix = 'https://api.ala.org.au/specieslist/ws/speciesList/'
    urlsuffix = ''
    data = download_url(urlprefix, urlsuffix, dr)
    splCt = data['itemCount'][0]

    drProfile = dr + alaProfile
    urlprefix = 'https://api.ala.org.au/occurrences/occurrences/search?q=species_list_uid%3A'
    # Generalised count
    urlsuffix = '&fq=sensitive%3Ageneralised&im=false'
    data = download_url(urlprefix, urlsuffix, drProfile)
    genCt = data['totalRecords'][0]

    # Already Generalised
    urlsuffix = '&fq=sensitive%3AalreadyGeneralised&im=false'
    data = download_url(urlprefix, urlsuffix, drProfile)
    aGenCt = data['totalRecords'][0]

    # Not supplied
    urlsuffix =  '&fq=-sensitive%3A*'
    data = download_url(urlprefix, urlsuffix, drProfile)
    nsCt = data['totalRecords'][0]

    # Species count
    urlprefix = 'https://api.ala.org.au/occurrences/occurrences/facets?q=species_list_uid%3A'
    urlsuffix = '&facets=species'
    data = download_url(urlprefix, urlsuffix, drProfile)
    spCt = data['count'][0]
    totCt = genCt + aGenCt + nsCt
    values = [[state, dr, splCt, totCt, spCt, genCt, aGenCt, nsCt]]

    return values

##############################################################################################
# Production Sensitive Lists
drList = {"ACT":"dr2627", "NSW":"dr487", "NT":"dr492",
          "QLD":"dr493", "SA":"dr884","TAS":"dr491",
          "VIC":"dr490"}
# drList = {"VIC":"dr490"}

cols = ['State', 'ListID', '#Sp.in list', 'Total Occurrences', 'Species count',
        'Generalised', 'Already Generalised', ' Not Supplied']

summarydf = pd.DataFrame(columns=cols)
rsummarydf = pd.DataFrame(columns=cols)


for state, dr in drList.items():
    alaProfile = ""
    rsummarydf = rsummarydf.append(pd.DataFrame(get_sds_info(state, dr, alaProfile), columns=cols), ignore_index=True)
    alaProfile = "&qualityProfile=ALA"
    summarydf = summarydf.append(pd.DataFrame(get_sds_info(state, dr, alaProfile), columns=cols), ignore_index=True)

# need to do this for ALA profile also

# Write Summary report to markdown
mheader = "## State Sensitive Species Lists - Occurrence Assertions Summary" + "  \n" + "### **No ALA Profile** \n"
mfooter = "\n"
# Raw data no ALA profile
rdsdf = build_markdown(rsummarydf, mheader, mfooter)

# Data with ALA profile
mheader = "### **Including ALA Profile**" + "  \n"
mfooter = " "
mdsdf = build_markdown(summarydf, mheader, mfooter)

mfile = outDir + 'SDS-Assertions-Information' + '.md'
with open(mfile, 'w') as f:
    f.write(rdsdf)
    f.write(mdsdf)
print('Writing report to markdown')
print('Finished Processing')



