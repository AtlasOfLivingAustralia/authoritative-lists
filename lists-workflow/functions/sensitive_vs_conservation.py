import pandas as pd
import math
from vocab import generalisation_categories,codeMap,kingdomMap,conservation_columns_rename,sensitive_columns_rename
import list_functions as lf

def create_sensitive_list(list_data = None,
                          state = None):

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

        # taxonRank

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
        sensitive_species = pd.concat([sensitive_species,new])
    
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


    elif state == "Western Australia":

        # make sure the generalisation column is there
        sensitive_species = list_data
        sensitive_species['generalisation'] = "10km"
    
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

    if extra_columns:
        return sensitive_species[['scientificName', 'family', 'vernacularName', 'generalisation','category'] + extra_columns]
    else:
        return sensitive_species[['scientificName', 'family', 'vernacularName', 'generalisation','category']]

def create_conservation_list(list_data = None,
                             state = None):

    # check for conservation codes
    conservation_codes = lf.get_conservation_codes(state=state)
    
    # do all the renaming possible here
    conservation_list = list_data.rename(columns=conservation_columns_rename[state])

    # set this just in case
    extra_columns = None
    
    # now, check state
    if state == "New South Wales":

        conservation_list= list_data[(list_data['stateConservation'] !='Not Listed') & (list_data['isCurrent'] == 'true')].reset_index(drop=True)
        conservation_list['status'] = conservation_list['stateConservation']
        conservation_list = conservation_list.rename(columns={"stateConservation": "sourceStatus"})

    elif state == "Queensland":

        extra_columns = ['WildNetTaxonID','taxonID']

        # get conservation list
        conservation_list = pd.merge(conservation_list,conservation_codes,left_on=['sourceStatus'],right_on=['Code'],how="left")

        # second rename
        conservation_list = conservation_list.rename(columns={'Code_description':'status'})
        
        # only return things that we need?
        conservation_list['taxonID'] = 'https://apps.des.qld.gov.au/species-search/details/?id=' + conservation_list['WildNetTaxonID'].astype(str)
        
        # making sure we don't have NaNs in status and remove least concern species
        conservation_list = conservation_list[(conservation_list['status'].notna())]
        conservation_list = conservation_list[~conservation_list['status'].str.contains('Special least concern', case=False)]
        conservation_list = conservation_list[~conservation_list['status'].str.contains('Least concern', case=False)]

        # manual additions
        adds = conservation_list[conservation_list['scientificName'].isin(['Cacatua leadbeateri leadbeateri','Eclectus polychloros macgillivrayi'])]
        adds.loc[adds['scientificName'] == "Cacatua leadbeateri leadbeateri",'scientificName'] = "Cacatua leadbeateri"
        adds.loc[adds['scientificName'] == "Eclectus polychloros macgillivrayi",'scientificName'] = "Eclectus polychloros"
        conservation_list = pd.concat([conservation_list,adds])

        # make the taxonID column
        conservation_list['taxonID'] = "https://apps.des.qld.gov.au/species-search/details/?id=" + conservation_list['WildNetTaxonID'].astype(str)
    
    elif state == "Northern Territory":

        # only select statuses that are threatened species (these are ones to exclude)
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
        conservation_list = conservation_list.applymap(lambda s: s.lower() if type(s) == str else s)
        conservation_list['status'] = conservation_list['status'].str.upper()
        
        # merge list with statuses
        conservation_list = pd.merge(conservation_list,conservation_codes,left_on=['status'],right_on=['Code'],how="left").drop(['Code'],axis=1)

    elif state == "Tasmania":

        # get conservation codes
        conservation_list = pd.merge(conservation_list,conservation_codes,
                                     left_on=['status'],
                                     right_on=['Category code'],how="left")
        
        # remove empty statuses
        conservation_list = conservation_list[~conservation_list['status'].isna()].reset_index(drop=True)
    
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
        conservation_list['family'] = ""

    # replace all the NaNs with an empty string
        conservation_list['vernacularName'] = conservation_list['vernacularName'].replace(math.nan,"")

    # remove nans from the status column
    if 'status' in conservation_list:
        conservation_list = conservation_list[((conservation_list['status'].notna()))]
    if 'sourceStatus' in conservation_list and 'status' not in conservation_list:
        conservation_list['status'] = conservation_list['sourceStatus']
    if 'status' in conservation_list and 'sourceStatus' not in conservation_list: 
        conservation_list['sourceStatus'] = conservation_list['status']

    # returned the cleaned conservation list
    if extra_columns:
        return conservation_list[['scientificName', 'family', 'vernacularName', 'status','sourceStatus'] + extra_columns]
    else:
        return conservation_list[['scientificName', 'family', 'vernacularName', 'status','sourceStatus']]