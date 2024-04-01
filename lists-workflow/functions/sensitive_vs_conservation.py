import pandas as pd
import requests
from vocab import generalisation_categories,sensitive_list_urls
from list_functions import get_conservation_codes

def create_sensitive_list(list_data = None,
                          state = None):

    # check for conservation codes
    conservation_codes = get_conservation_codes(state=state)

    # first, sensitive list
    if state == "New South Wales":

        # get sensitive species only with category attached 
        sensitive_species = list_data[list_data['sensitivityClass'].isin(["Category 1","Category 2","Category 3"])].reset_index(drop=True)

         # add a generalisation column
        sensitive_species['generalisation'] = sensitive_species['sensitivityClass']

        sensitive_species['category'] = sensitive_species['sensitivityClass']

        # replace the category names with generalisations, including witheld
        sensitive_species['generalisation'] = sensitive_species['generalisation'].replace(generalisation_categories)

    elif state in ["Australian Capital Territory","South Australia","Northern Territory"]:

        return None
    
    elif state == "Queensland":

        # get sensitive species codes
        species_codes = pd.read_csv("https://apps.des.qld.gov.au/data-sets/wildlife/wildnet/species-status-codes.csv")

        # figure out what this is
        
        nca_status_codes = species_codes[species_codes['Field'] == "NCA_status"][['Code', 'Code_description']]

        # change code description to be capitalized
        nca_status_codes.loc[
        nca_status_codes['Code_description'] == "Critically endangered", 'Code_description'] = "Critically Endangered"
        nca_status_codes.loc[nca_status_codes['Code_description'] == "Near threatened", 'Code_description'] = "Near Threatened"

        # get sensitive species list
        sensitive_species = list_data

        # nca status
        sensitive_species = pd.merge(sensitive_species,nca_status_codes,left_on=['NCA status'],right_on=['Code'],how="left")
        #sensitivelist = sensitivelist.rename(columns={'NCA status':'sourceStatus'})
        sensitive_species = sensitive_species[['Scientific name', 'Common name', 'NCA status','Taxon Id', 'Code_description','Kingdom','Family']]
        sensitive_species = sensitive_species.rename(columns= {'Scientific name':'scientificName',
                                                    'Common name': 'vernacularName',
                                                    'NCA status': 'category', 
                                                    'Taxon Id':'WildNetTaxonID',
                                                    'Code_description':'status',
                                                    'Kingdom':'kingdom',
                                                    'Family':'family'})
        
        # where is this from?
        sensitive_species['generalisation'] = "2 km"

        # map sourceStatus to category
        # more mapping?
        codeMap = {'C': 'LC', 'CR': 'CR', 'E': 'EN',
                'NT': 'NT','PE': 'EW', 'SL': 'SL',
                'V': 'VU'}
        kingdomMap = {'animals':'Animalia','plants':'Plantae','fungi':'Fungi'}
        sensitive_species['kingdom'] = sensitive_species['kingdom'].replace(kingdomMap)
        sensitive_species['category'] = sensitive_species['category'].replace(codeMap)
        sensitive_species['category'] = sensitive_species['category'].fillna('UK')

        return sensitive_species

    elif state == "Tasmania":

        # figure out what makes a sensitive species in Tasmania
        return None

    elif state == "Western Australia":

        sensitive_species = list_data
        sensitive_species['generalisation'] = "10km"
        print(sensitive_species)
 
        print("need to figure this out for WA")
        import sys
        sys.exit()

    else:
        
        sensitive_species = list_data
         
    if state == "New South Wales":

        new = sensitive_species[sensitive_species.scientificName == "Calyptorhynchus lathami lathami"].copy()
        new[['scientificName']] = "Calyptorhynchus lathami" # replace the name
        new[['vernacularName']] = "Glossy Black-cockatoo"
        sensitive_species = pd.concat([sensitive_species,new])

    ### TODO: check for external ID
    return sensitive_species[['scientificName', 'kingdom','family', 'vernacularName', 'generalisation','category']]

def create_conservation_list(list_data = None,
                             state = None):

    # check for conservation codes
    conservation_codes = get_conservation_codes(state=state)

    # then, conservation list
    ### THIS IS FOR NSW
    if state == "New South Wales":

        conservation_list= list_data[(list_data['stateConservation'] !='Not Listed') & (list_data['isCurrent'] == 'true')].reset_index(drop=True)
        conservation_list = conservation_list[['scientificName', 'vernacularName', 'kingdom','family', 'stateConservation','sensitivityClass']] 
        conservation_list['status'] = conservation_list['stateConservation']
        conservation_list = conservation_list.rename(columns={"stateConservation": "sourceStatus"})

    # Queensland - comment this
    elif state == "Queensland":

        # get conservation list
        conservation_list = pd.merge(list_data,conservation_codes,left_on=['NCA_status'],right_on=['Code'],how="left")

        # rename columns to be Darwin Core compliant
        conservation_list = conservation_list.rename(columns={   
            'Scientific_name':'scientificName',
            'Common_name': 'vernacularName',
            'Taxon_author':'scientificNameAuthorship',
            'Family': 'family',
            'NCA_status':'sourceStatus',
            'Code_description':'status',
            'Taxon_Id':'WildNetTaxonID'}
        )
        
        # only return things that we need?
        conservation_list['taxonID'] = 'https://apps.des.qld.gov.au/species-search/details/?id=' + conservation_list['WildNetTaxonID'].astype(str)
        conservation_list = conservation_list.loc[:, ['scientificName', 'vernacularName', 'family', 'WildNetTaxonID','taxonID','status', 'sourceStatus']]

        # this...? What is this?
        conservation_list = conservation_list[(conservation_list['status'].notna())]
        conservation_list = conservation_list[~conservation_list['status'].str.contains('Special least concern', case=False)]
        conservation_list = conservation_list[~conservation_list['status'].str.contains('Least concern', case=False)]

        # manual additions
        adds = conservation_list[conservation_list['scientificName'].isin(['Cacatua leadbeateri leadbeateri','Eclectus polychloros macgillivrayi'])]
        adds.loc[adds['scientificName'] == "Cacatua leadbeateri leadbeateri",'scientificName'] = "Cacatua leadbeateri"
        adds.loc[adds['scientificName'] == "Eclectus polychloros macgillivrayi",'scientificName'] = "Eclectus polychloros"
        conservation_list = pd.concat([conservation_list,adds])

        return conservation_list
    
    elif state == "Northern Territory":

        # check that this is correct for all lists
        conservation_list = list_data.dropna(subset = ['TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION'], inplace=True)
        conservation_list = list_data[~list_data['TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION'].isin([
            "LC-EXNT",
            "LC",
            "NE",
            "(NL)",
            "(Int)",
            # "DD",
            # "NT",
            "INFRA",
            "NL"
        ])].reset_index(drop=True)

        # change classification to status and make sure they have correct capitalization
        conservation_list = conservation_list.rename(columns={'TERRITORY PARKS AND WILDLIFE ACT CLASSIFICATION': 'status'})
        conservation_list = conservation_list.applymap(lambda s: s.lower() if type(s) == str else s)
        conservation_list['status'] = conservation_list['status'].str.upper()
        
        # merge list with statuses
        conservation_list = pd.merge(conservation_list,conservation_codes,left_on=['status'],right_on=['Code'],how="left").drop(['Code'],axis=1)
        
        # rename columns
        conservation_list = conservation_list.rename(columns={
            'COMMON NAME': 'vernacularName',
            'FAMILY': 'family', 
            'GENUS': 'genus', 
            'SPECIES': 'species',
            'Categories for classification': 'sourceStatus'
        })

    elif state == "Tasmania":

        conservation_list = pd.merge(list_data,conservation_codes,
                                     left_on=['Current TSPA schedule classification'],
                                     right_on=['Category code'],how="left")
        
        conservation_list = conservation_list[~conservation_list['Current TSPA schedule classification'].isna()].reset_index(drop=True)

        conservation_list = conservation_list.rename(columns={
            'Scientific name': 'scientificName', 
            'Common name': 'vernacularName',
            'Current TSPA schedule classification': 'status',
            'Category': 'sourceStatus',
            'Family': 'family'
        })

    elif state == "Western Australia":

        print("in conservation for WA")
        print(list_data)
        import sys
        sys.exit()

    else:
        conservation_list = list_data

    # remove nans from the status column
    if 'status' in conservation_list:
        conservation_list = conservation_list[((conservation_list['status'].notna()))]
    if 'sourceStatus' in conservation_list and 'status' not in conservation_list:
        conservation_list['status'] = conservation_list['sourceStatus']
    if 'status' in conservation_list and 'sourceStatus' not in conservation_list: 
        conservation_list['sourceStatus'] = conservation_list['status']

    return conservation_list[['scientificName', 'family', 'vernacularName', 'status','sourceStatus']]