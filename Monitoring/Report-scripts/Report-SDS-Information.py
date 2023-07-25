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

def download_url(url: str):
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
    # mdf = lf.df_to_markdown(df)
    # Add headers and description
    blist = [
        "Generalised",
        "Already Generalised",
        "Not Supplied \n"
    ]
    mheader = "### State Sensitive Species Lists Sensitive Data Assertions" + "  \n"
    # Convert the list to a Markdown-formatted string with bullets
    bliststr = "\n".join([f"* {item}" for item in blist])
    description = f"\n The table below summarises assertions:\n\n{bliststr}\n"

    # Update the Markdown content in the first row
    mdf = lf.df_to_markdown(df)
    mdf = mheader + description + mdf

    return mdf

def get_sds_info(state,dr):
    urlprefix = 'https://api.ala.org.au/occurrences/occurrences/search?q=species_list_uid%3A'
    # Generalised count
    # urlgen = 'https://api.ala.org.au/occurrences/occurrences/search?q=species_list_uid%3Adr2627&fq=sensitive%3Ageneralised&im=false'
    urlgen = urlprefix + dr + '&fq=sensitive%3Ageneralised&im=false'
    data = download_url(urlgen)
    genCt = data['totalRecords'][0]
    # Already Generalised
    urlagen = urlprefix + dr + '&fq=sensitive%3AalreadyGeneralised&im=false'
    data = download_url(urlagen)
    aGenCt = data['totalRecords'][0]
    # Not supplied
    urlns = urlprefix + dr + '&fq=-sensitive%3A*'
    data = download_url(urlns)
    nsCt = data['totalRecords'][0]
    totCt = genCt + aGenCt
    values = [[state, dr, genCt, aGenCt, nsCt, totCt]]

    return values

##############################################################################################
# Production Sensitive Lists
drList = {"ACT":"dr2627", "NSW":"dr487", "NT":"dr492",
          "QLD":"dr493", "SA":"dr884","TAS":"dr491",
          "VIC":"dr490", "WA":"dr467"}

cols = ['State', 'ListID', 'Generalised', 'Already Generalised', ' Not Supplied', 'Total Occurrences']
summarydf = pd.DataFrame(columns=cols)
for state, dr in drList.items():
    summarydf = summarydf.append(pd.DataFrame(get_sds_info(state, dr), columns=cols), ignore_index=True)

# Write Summary report to markdown
mdsdf = build_markdown(summarydf)
# mfile = outDir + 'SDS-Information-' + monthStr + '.md'
mfile = outDir + 'SDS-Assertions-Information' + '.md'
with open(mfile, 'w') as f:
    f.write(mdsdf)
print('Writing report to markdown')
print('Finished Processing')



