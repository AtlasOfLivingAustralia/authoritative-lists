# Northern Territory Conservation Lists

#%% import essential libraries 
import pandas as pd
import numpy as np
import dateutil.parser as parser
import json as json

#%% Import Data
data = pd.read_excel("/Users/cha801/Documents/UpdateLists/Excels/northernTerritoryConservationStatusList-Plants.xlsx")
#%%
#rename the DwC terms
data = data.rename(columns=
{
#'Scientific name':'scientificName',
'Plant family':'family',
'Status':'status',
#'Animal Group':'taxonRemarks'
})

#%% Process Data
data['sourceStatus'] = data['status'].copy()
data['status'] = data['status'].str.split('(').str[0]
data['vernacularName'] = data['Scientific name'].str.split('\n').str[1]
data['scientificName'] = data['Scientific name'].str.split('\n').str[0]
data = data.drop(['Scientific name'], axis=1)
#data.to_csv('/northernTerritoryConservationStatusList-Plants.csv',index = False,encoding='utf-8-sig')
data1 = pd.read_csv("/northernTerritoryConservationStatusList-Animals.csv")
print ("data is ",data.shape)
print ("data 1 is ",data1.shape)

result = pd.concat([data, data1])

result.to_csv('/northernTerritoryConservationStatusList.csv',index = False,encoding='utf-8-sig')