# EPBC - List
# Source: Manual download to CSV from https://www.environment.gov.au/sprat-public/action/report


#%% import essential libraries
import pandas as pd
import numpy as np
from skimpy import clean_columns


#%% top level directory
# projectDir = "/Users/new330/IdeaProjects/authoritative-lists/"
projectDir = "/Users/oco115/PycharmProjects/authoritative-lists/"
dataDir = "current-lists/conservation-lists/"

# list was downloaded from
epbcreport = pd.read_csv(projectDir + "source-data/EPBCA/10052022-123645-report.csv",skiprows=1)
epbcreport.columns

#%% to do - including all columns
# DWC where obvious, otherwise retain fieldnames in camelCase

epbcreport = epbcreport.rename(columns=
{
    'Taxon ID':'taxonID',
    'TaxonGroup':'taxonRemarks',
    'Scientific Name':'scientificName',
    'Common Name':'vernacularName',
    'EPBC Threat Status':'status',
    'IUCN Red List': 'iucn Red List',
    'IUCN Red List Listed Names' : 'iucn Red List Listed Names',
    'CAMBA': 'Camba',
    'JAMBA': 'Jamba',
    'ROKAMBA': 'Rokamba',
    'Kingdom':'kingdom',
    'Phylum':'phylum',
    'Class': 'class',
    'Order': 'order',
    'Family': 'family',
    'Genus': 'genus'
})
epbcreport=epbcreport.drop(['Unnamed: 65',
                'Listed Name Bonn', 'Listed Name Camba',
                'Listed Name Jamba', 'Listed Name Rokamba',
                'ACT NC Act', 'Listed Name', 'NSW TSC Act and FM Act', 'Listed Name.1',
                'NT TPWC Act', 'Listed Name.2', 'Qld NC Act', 'Listed Name.3',
                'SA NPW Act', 'Listed Name.4', 'Tas. TSP Act', 'Listed Name.5',
                'Vic. FFG Act (Advisory Lists)', 'Listed Name.6', 'WA WC Act',
                'Listed Name.7',
               ],axis=1)
epbcreport.columns = epbcreport.columns.str.replace("  ", "", regex=True) # remove multiple spacesfrom column names
epbcreport.columns = epbcreport.columns.str.replace(r"[().: ]", " ", regex=True) # remove : () from column names
epbcreport.columns = epbcreport.columns.str.replace("EPBC","", regex=True)
epbcreport.columns = epbcreport.columns.str.replace("FPAL","", regex=True)
epbcreport.columns = epbcreport.columns.str.strip()

#%% create an epbc list: should be 1955 species (with EPBC Threat Status)
# epbc = epbcreport[epbcreport[\"EPBC Threat Status\"].notna()]
epbc= epbcreport[epbcreport["status"].notna()]
epbc.to_csv(projectDir + dataDir + "EPBC-new-conservation.csv",index=False)

#%% create Bonn list
bonn = epbcreport[epbcreport["Bonn"].notna()]
bonn.to_csv(projectDir + dataDir + "BONN-new-conservation.csv",index=False)

#%% create CAMBA list
camba = epbcreport[epbcreport["Camba"]=="Listed"]
camba.to_csv(projectDir + dataDir + "CAMBA-new-conservation.csv",index=False)

#%% create JAMBA list
jamba = epbcreport[epbcreport["Jamba"]=="Listed"]
jamba.to_csv(projectDir + dataDir + "JAMBA-new-conservation.csv",index=False)

#%% create ROKAMBA list
rokamba = epbcreport[epbcreport["Rokamba"]=="Listed"]
rokamba.to_csv(projectDir + dataDir + "ROKAMBA-new-conservation.csv",index=False)
