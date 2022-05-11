#import essential libraries
import pandas as pd
import numpy as np

projectDir = "/Users/oco115/PycharmProjects/authoritative-lists/"
dataDir = "current-lists/conservation-lists/"


# list was downloaded from
epbcreport = pd.read_csv(projectDir + "source-data/EPBCA/10052022-123645-report.csv",skiprows=1)

# create an epbc list: should be 1955 species (with EPBC Threat Status)
epbc = epbcreport[epbcreport["EPBC Threat Status"].notna()]

# to do - including all columns
# DWC where obvious, otherwise retain fieldnames in camelCase
epbc = epbc.rename(columns=
{
    'Taxon ID':'taxonID',
    'Scientific Name':'scientificName',
    'Common Name':'vernacularName',
    'EPBC Threat Status':'status'
})
epbc.columns = epbc.columns.str.replace(r"[().: ]", "", regex=True) # remove all spaces and : () from column names
epbc.drop(['Unnamed65'],axis=1)
coltuple = np.where(epbc.columns.str.contains(r'ListedName\d'))
colIdx = coltuple[0]
epbc.columns.values[colIdx] = epbc.columns.values[colIdx] + epbc.columns.values[colIdx-1]
# epbc.to_csv("./data/EPBCA-new-conservation.csv",index=False)

# create Bonn list - retain these fields
bonn = epbcreport[epbcreport["Bonn"].notna()]
#bonn = bonn[["Bonn","Listed Name Bonn","Common Name","Kingdom","Phylum","Class","Order","Family","Genus","Taxon Group"]]
bonn
# q for cam - what's the status of these?

bonn = bonn.rename(columns=
{
    # 'Taxon ID':'taxonID',
    'Taxon Group':'taxonRemarks',
    'Scientific Name':'scientificName',
    'Common Name':'vernacularName',
    'EPBC Threat Status':'status'
})

bonn.columns = bonn.columns.str.replace(r"[().: ]", "", regex=True) # remove all spaces and : () from column names
bonn = bonn.drop(['Unnamed65'],axis=1)
coltuple = np.where(bonn.columns.str.contains(r'ListedName\d'))
colIdx = coltuple[0]
bonn.columns.values[colIdx] = bonn.columns.values[colIdx] + bonn.columns.values[colIdx-1]
# bonn.to_csv(projectDir + dataDir + "BONN-new-conservation.csv",index=False)

# Above code repeated in notebook for CAMBA,JAMBA and ROKAMBA