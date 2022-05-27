#%%
import pandas as pd

# top level directory
projectDir = "/Users/oco115/PycharmProjects/authoritative-lists"
dataDir = "/current-lists/sensitive-lists/"


#%%  Function Definitions
# function Read sensitive data file
    def readData(state,stateFile):
        outData  = pd.read_csv(projectDir + dataDir + stateFile)
        return outData

#%% Define Mapping fields

mappings = {'Category 1':'C1','Category 2':'C2','Category 3': 'C3',
            ' WA Priority 4': 'P4', ' WA Priority 3': 'P3',
            ' WA Priority 2': 'P2',' WA Priority 1': 'P1',
            'Priority': 'PX',
            'Other Specially Protected': ' SP',
            'Vulnerable' : 'VU',
            'Extinct': 'X',
            'Endangered': 'EN',
            'Critically Endangered': 'CR',
            'Conservation Dependent': 'CD',
            'Near Threatened' : 'NT',
            'Least concern' : 'LC',
            'Special least concern' : 'LC',
            'Extinct in the wild' : 'EW'}

#%% Retrieve Data
# list was downloaded from
listData = [['WA','WA-sensitive.csv'],['NSW','NSW-sensitive.csv'],['QLD','QLD-sensitive.csv']]
dfList = pd.DataFrame(listData, columns=['State', 'Fname'])
for index, row in dfList.iterrows():
    outVals = readData(row['State'],row['Fname'])
    # newData = processState(row['State'], outVals)
    if row['State'] == 'NSW':
        status = outVals['sensitivityClass'].tolist()
    else:
        status = outVals['status'].tolist()
    outVals['category'] = list(map(mappings.get, status))
    outFname = "new_" + row['Fname']
    # xx= pd.DataFrame().assign(Category=outVals['category'],status=outVals['status'])
    outVals.to_csv(projectDir + dataDir + outFname,index=False)

