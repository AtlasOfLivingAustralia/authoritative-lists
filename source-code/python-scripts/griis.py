#Global Register of Introduced and Invasive Species - Australia (GRIIS)

import pandas as pd
import requests
import os
import zipfile
from pathlib import Path
import ftfy
from ftfy import fix_encoding

#%%Download the Darwin Core Archive and read the species list into a dataframe

url = "https://cloud.gbif.org/griis/archive.do?r=griis-australia&v=1.9"
basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"
sourcedir = basedir+"source-data/griis/"
targetdir = basedir+"current-lists/griis/"
print("Downloading dwca")
r = requests.get(url)

#%% Retrieve the filename from the headers. Download and unzip the file

basedir = "/Users/oco115/PycharmProjects/authoritative-lists/"
sourcedir = basedir+"source-data/griis/"
targetdir = basedir+"current-lists/griis/"
dwca = sourcedir + r.headers['content-disposition'].split("=")[1].replace('"','')

if Path(dwca).exists():
  os.remove(dwca)
unzipdirname = dwca[:-len(".zip")]
if not Path(unzipdirname):
  os.mkdir(unzipdirname)

#%% Open file and write to directory
with open(dwca, "wb") as output_file:
    output_file.write(r.content)

# Unzip and extract
with zipfile.ZipFile(dwca, 'r') as z:
   z.extractall(unzipdirname)

#Explore the list, looking especially for encoding issues.
taxondf = pd.read_csv(unzipdirname + os.sep + "taxon.txt",sep="\t",lineterminator="\n")

#%% fix encoding issues using ftfy
taxondf['scientificName'] = taxondf['scientificName'].apply(fix_encoding)
taxondf[['taxonID','scientificName','acceptedNameUsage']]

#%% Write to CSV
# taxondf.to_csv(targetdir+"griis-1.9.csv",index=False)
# os.remove(dwca)
