##############################################################################################
#
# SDS List Information Report
# Extract SDS Information for each state
# Output report
# Output information files to : ..\authoritative-lists\analysis\reports
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

projectdir = "/Users/oco115/PycharmProjects/authoritative-lists/"
outdir = projectdir + "Monitoring/"
sys.path.append(os.path.abspath(projectdir + "source-code/includes"))
import list_functions as lf
import configuration as cfg


def download_from_url(url: str):
    print("download from: ", url)
    with urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as url:
        if url.status == 200:
            data = json.loads(url.read().decode())
            data = pd.json_normalize(data)
        else:
            # Handle the error
            print('Error in download_ala_list:', url.status)
    return data

monthStr = datetime.datetime.now().strftime('%Y%m%d')
# state = ''
url = 'https://api.ala.org.au/occurrences/occurrences/search?q=q%3Dspecies_list_uid%253Adr487&fq=state%253A%2522New%2BSouth%2BWales&qualityProfile=ALA&im=false'
statedf = download_from_url(url)



##############################################################################################

# print('Writing report to markdown')
# pmdfile = outdir + "Authoritative-lists-prod.md"
# tmdfile = outdir + "Authoritative-lists-test.md"
# lf.list_to_markdown("P", pconsdf, psensdf, pmdfile)
# lf.list_to_markdown("T", tconsdf, tsensdf, tmdfile)
print('Finished Processing')



