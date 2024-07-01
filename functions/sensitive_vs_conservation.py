import pandas as pd
import math
from .vocab import generalisation_categories,codeMap,kingdomMap,conservation_columns_rename,sensitive_columns_rename,classMap
from .vocab import conservation_species_corrections,sensitive_species_corrections,statuses_rename
from . import list_functions as lf

def create_sensitive_list(list_data = None,
                          state = None):
    '''
    This function creates sensitive lists, and makes sure that the correct information is 
    returned, especially data on how to obscure coordinates.
    '''

    # check for conservation codes
    conservation_codes = lf.get_conservation_codes(state=state)

    # do as much renaming as you can 
    sensitive_species= list_data.rename(columns=sensitive_columns_rename[state])

    # set this just in case
    extra_columns = None

    # first, check for states whose lists we won't be updating automatically
    if state in ["Australian Capital Territory","South Australia","Northern Territory","Tasmania"]:

        return None

    # now, check NSW
    elif state == "New South Wales":

        # extra columns - test to see for NSW
        extra_columns = ["kingdom","order","genus"]

        # check for current status in new south wales
        if 'isCurrent' in sensitive_species:
            sensitive_species = sensitive_species[sensitive_species['isCurrent'] == "true"]

        # get sensitive species only with category attached 
        sensitive_species = sensitive_species[sensitive_species['sensitivityClass'].isin(["Category 1","Category 2","Category 3"])].reset_index(drop=True)

         # add a generalisation column
        sensitive_species['generalisation'] = sensitive_species['sensitivityClass']

        # add the category
        sensitive_species['category'] = sensitive_species['sensitivityClass']

        # replace the category names with generalisations, including witheld
        sensitive_species['generalisation'] = sensitive_species['generalisation'].replace(generalisation_categories)

        # some last-minute changes for certain species
        new = sensitive_species[sensitive_species.scientificName == "Calyptorhynchus lathami lathami"].copy()
        new[['scientificName']] = "Calyptorhynchus lathami" # replace the name
        new[['vernacularName']] = "Glossy Black-cockatoo"
        new2 = new.copy()
        for column in list(new2.columns):
            new2[column] = ''
        new2['generalisation'] = '10km'
        new2['category'] = 'Category 2'
        new2['scientificName'] = 'Liopholis whitii'
        new2['vernacularName'] = 'White\'s Skink'
        new2['family'] = 'Scincidae'
        sensitive_species = pd.concat([sensitive_species,new,new2])
    
    elif state == "Queensland":

        # NO TAXON RANK AVAILABLE - WHERE TO GET THIS
        extra_columns = ['WildNetTaxonID','taxonID']

        # merge category column with code
        sensitive_species = pd.merge(sensitive_species,conservation_codes,left_on=['category'],right_on=['Code'],how="left")
        
        # add generalisation
        sensitive_species['generalisation'] = "2km"

        # map sourceStatus to category and kingdom - also fill in category with 'UK' (unknown)
        # if not known
        sensitive_species['kingdom'] = sensitive_species['kingdom'].replace(kingdomMap)
        sensitive_species['category'] = sensitive_species['category'].replace(codeMap)
        sensitive_species['category'] = sensitive_species['category'].fillna('UK')

        # make the taxonID column
        sensitive_species['taxonID'] = "https://apps.des.qld.gov.au/species-search/details/?id=" + sensitive_species['WildNetTaxonID'].astype(str)
        sensitive_species['taxonRank'] = ''

    elif state == "Western Australia":

        # make sure the generalisation column is there
        sensitive_species = list_data
        sensitive_species['generalisation'] = "10km"
        sensitive_species['category'] = sensitive_species['status']
        sensitive_species['taxonRank'] = ''
        
        # Crendactylus tuberculatus instead of Crenadactylus tuberculatus
        sensitive_species = sensitive_species.replace('Crendactylus tuberculatus','Crenadactylus tuberculatus')
    
    elif state == "Victoria":

        # separate conservation and sensitive species
        sensitive_species = sensitive_species[~sensitive_species['RESTRICTED_FLAG'].isin([
            math.nan
        ])].reset_index(drop=True)
        sensitive_species['family'] = ""
        sensitive_species['generalisation'] = '1km'
        # 'TAXON_LEVEL_CDE' - replace 'spec' with 'species'
        sensitive_species['taxonRank'] = sensitive_species['vernacularName'].replace('spec','species')

    else:
        
        # data is good as is
        sensitive_species = list_data

    # replace all the NaNs with an empty string
    sensitive_species['vernacularName'] = sensitive_species['vernacularName'].replace(math.nan,"")
    sensitive_species['raw_scientificName'] = sensitive_species['scientificName'].copy()
    sensitive_species['scientificName'] = sensitive_species['scientificName'].replace(sensitive_species_corrections[state])

    # replace NaNs with empty string
    sensitive_species = sensitive_species.where((pd.notnull(sensitive_species)), '')

    if extra_columns:
        return sensitive_species[['raw_scientificName','scientificName', 'taxonRank','family', 'vernacularName', 'generalisation','category'] + extra_columns]
    else:
        return sensitive_species[['raw_scientificName','scientificName', 'taxonRank','family', 'vernacularName', 'generalisation','category']]

def create_conservation_list(list_data = None,
                             state = None):
    '''
    This function creates conservation lists, and makes sure that the correct information is 
    returned, especially the status of species.
    '''

    # check for conservation codes
    conservation_codes = lf.get_conservation_codes(state=state)
    
    # do all the renaming possible here
    conservation_list = list_data.rename(columns=conservation_columns_rename[state])

    # set this just in case
    extra_columns = None
    
    # now, check state
    if state == "New South Wales":

        # make conservation list
        conservation_list= list_data[(list_data['stateConservation'] !='Not Listed') & (list_data['isCurrent'] == 'true')].reset_index(drop=True)
        conservation_list['status'] = conservation_list['stateConservation']
        conservation_list = conservation_list.rename(columns={"stateConservation": "sourceStatus"})
        
    elif state == "Queensland":

        extra_columns = ['WildNetTaxonID','taxonID']

        # get conservation list
        conservation_list = pd.merge(conservation_list,conservation_codes,left_on=['NCA_status'],right_on=['Code'],how="left")
        
        # second rename
        conservation_list = conservation_list.rename(columns={'Code_description':'sourceStatus'})
        
        # only return things that we need?
        conservation_list['taxonID'] = 'https://apps.des.qld.gov.au/species-search/details/?id=' + conservation_list['WildNetTaxonID'].astype(str)
        
        # making sure we don't have NaNs in status and remove least concern species
        conservation_list = conservation_list[(conservation_list['sourceStatus'].notna())]
        conservation_list = conservation_list[~conservation_list['sourceStatus'].str.contains('Special least concern', case=False)]
        conservation_list = conservation_list[~conservation_list['sourceStatus'].str.contains('Least concern', case=False)]

        # manual additions
        adds = conservation_list[conservation_list['scientificName'].isin(['Cacatua leadbeateri leadbeateri','Eclectus polychloros macgillivrayi'])]
        adds.loc[adds['scientificName'] == "Cacatua leadbeateri leadbeateri",'scientificName'] = "Cacatua leadbeateri"
        adds.loc[adds['scientificName'] == "Eclectus polychloros macgillivrayi",'scientificName'] = "Eclectus polychloros"
        conservation_list = pd.concat([conservation_list,adds])

        # make the taxonID column
        conservation_list['taxonID'] = "https://apps.des.qld.gov.au/species-search/details/?id=" + conservation_list['WildNetTaxonID'].astype(str)

        # add rank column
        conservation_list['taxonRank'] = ''
    
    elif state == "Northern Territory":
        
        # edit some of the codes
        conservation_list['status'] = conservation_list['status'].replace({
            "CR-PE": "CR",
            "EN-EXNT": "EN",
            "EN-EWNT": "EN",
            "VU-EXNT": "VU",
        })

        # remove the things we aren't concerned with
        conservation_list = conservation_list[~conservation_list['status'].isin([
            "LC-EXNT",
            "LC",
            "NE",
            "(NL)",
            "(Int)",
            "INFRA",
            "NL",
            math.nan
        ])].reset_index(drop=True)

        # change classification to status and make sure they have correct capitalization
        conservation_list = conservation_list.applymap(lambda s: s.capitalize() if type(s) == str else s)
        conservation_list['status'] = conservation_list['status'].str.upper()
        
        # merge list with statuses
        conservation_list = pd.merge(conservation_list,conservation_codes,left_on=['status'],right_on=['Code'],how="left").drop(['Code'],axis=1)
        conservation_list = conservation_list.rename(columns={'Categories for classification':'sourceStatus'})

        # add taxon rank
        conservation_list['taxonRank'] = ''

    elif state == "Tasmania":

        # get conservation codes
        conservation_list = pd.merge(conservation_list,conservation_codes,
                                     left_on=['status'],
                                     right_on=['Category code'],how="left")
        conservation_list['sourceStatus'] = conservation_list['Category'].copy()

        # remove empty statuses
        conservation_list = conservation_list[~conservation_list['status'].isna()].reset_index(drop=True)

        # add rank
        conservation_list['taxonRank'] = ''

    elif state == "Victoria":

        # remove all nans (and maybe 'Poorly known')
        conservation_list = conservation_list[~conservation_list['status'].isin([
            math.nan
        ])].reset_index(drop=True)

        # separate conservation and sensitive species
        conservation_list = conservation_list[~conservation_list['RESTRICTED_FLAG'].isin([
            'rest',
            'breed'
        ])].reset_index(drop=True)

        # add family column
        conservation_list['family'] = ''
        conservation_list['taxonRank'] = ''

        # replace all the NaNs with an empty string
        conservation_list['vernacularName'] = conservation_list['vernacularName'].replace(math.nan,"")


    elif state == "Western Australia":

        conservation_list['taxonRank'] = ''

    elif state == "Australian Capital Territory":

        pass

    elif state == "EPBC":

        extra_columns = ['genus']
        conservation_list['taxonRank'] = ''
        # print(conservation_list.columns)
        # print(conservation_list[['scientificName','sourceStatus']])
        # import sys
        # sys.exit()

    else:

        print("Another state needs to be taken into account")
        print(state)
        print(conservation_list.columns)
        import sys
        sys.exit()

    # preserve the original name
    conservation_list['raw_scientificName'] = conservation_list['scientificName'].copy()
    conservation_list['scientificName'] = conservation_list['scientificName'].replace(conservation_species_corrections[state])

    # remove nans from the status column
    if 'status' in conservation_list:
        conservation_list = conservation_list[((conservation_list['status'].notna()))]
    if 'sourceStatus' in conservation_list and 'status' not in conservation_list:
        conservation_list['status'] = conservation_list['sourceStatus'].copy()
    if 'status' in conservation_list and 'sourceStatus' not in conservation_list: 
        conservation_list['sourceStatus'] = conservation_list['status'].copy()

    # make sure the statuses are IUCN compliant
    conservation_list['status'] = conservation_list['status'].replace(statuses_rename[state])

    # replace NaNs with empty string
    conservation_list = conservation_list.where((pd.notnull(conservation_list)), '')

    # returned the cleaned conservation list
    if extra_columns:
        return conservation_list[['raw_scientificName','scientificName', 'taxonRank', 'family', 'vernacularName', 'status','sourceStatus'] + extra_columns]
    else:
        return conservation_list[['raw_scientificName','scientificName', 'taxonRank', 'family', 'vernacularName', 'status','sourceStatus',]]