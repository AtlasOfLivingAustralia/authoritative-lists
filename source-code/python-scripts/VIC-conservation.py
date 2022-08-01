# VIC - Conservation List
# Conservation list source: https://vba.dse.vic.gov.au/vba/downloadVSC.do

#%%
import pandas as pd

# top level directory
# projectDir = "/Users/new330/IdeaProjects/authoritative-lists/"
projectDir = "/Users/oco115/PycharmProjects/authoritative-lists/"
dataDir = "current-lists/conservation-lists/"
conservationlisturl = "https://vba.dse.vic.gov.au/vba/downloadVSC.do" # gets a csv
conservationList = pd.read_csv(projectDir + "source-data/VIC/Species-Checklist.csv",encoding='cp1252')


# Drop columns
conservationList = conservationList.drop(['PARENT_TAXON_LEVEL_CDE','PARENT_TAXON_ID','ALL_DISCIPLINE_CODES',
                                          'TREATIES','SHORT_NAME','NVIS_GROWTHFORM','SCIENTIFIC_NME_SYNONYM',
                                          'COMMON_NME_SYNONYM','PRINT_ORDER_NUM'],axis=1)
# Rename columns
conservationList = conservationList.rename(columns=
{
    'TAXON_ID':'taxonID',
    'SCIENTIFIC_NAME':'scientificName',
    'VIC_ADVISORY_STATUS':'status',
    'TAXON_TYPE':'speciesGroup',
    'FFG_ACT_STATUS':'ffgactStatus',
    'EPBC_ACT_STATUS': 'epbcactStatus',
    'TAXON_LEVEL_CDE': 'taxonRank',
    'ORIGIN': 'establishmentMeans',
    'COMMON_NME_SYNONYM': 'taxonRemarks',
    'COMMON_NAME':'vernacularName',
    'AUTHORITY':'scientificNameAuthority',
    'PRIMARY_DISCIPLINE': 'primaryDiscipline',
    'RESTRICTED_FLAG' : 'restrictedFlag',
    'EXTRACT_DATE': 'extractDate',
    'LAST_MOD':'modified'
})
conservationList['taxonRank'] = 'species'
# conservationList.columns = conservationList.columns.str.replace(r"[().: ]", "", regex=True) # remove all spaces and : () from column names
# conservationList.columns = conservationList.columns.str.replace(r"[_ ]", "", regex=True) # remove all spaces and : () from column names
# conservationList=conservationList.drop(['Unnamed65'],axis=1)

conservationList = conservationList[conservationList["ffgactStatus"].notna()]
conservationList.to_csv(projectDir + dataDir + "VIC-new-conservation.csv",index=False)