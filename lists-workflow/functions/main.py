import requests
import pandas as pd
import list_functions as lf
from vocab import lists,conservation_list_urls,sensitive_list_urls
from sensitive_vs_conservation import create_conservation_list,create_sensitive_list
from datetime import datetime
# need xlrd???

def main():

    for state in lists:

        print(state)
        # initialise sensitive and conservation list data
        sensitive_list_data = pd.DataFrame()
        conservation_list_data = pd.DataFrame()

        # check if state is in sensitive list urls
        if state in sensitive_list_urls.keys():

            # loop over all links present to get 
            for i in range(len(sensitive_list_urls[state])):
                sensitive_list_data = pd.concat([sensitive_list_data,lf.read_list_url(url=sensitive_list_urls[state][i],state=state)]).reset_index(drop=True)

            sensitive_list_data = sensitive_list_data.rename(columns={'scientificname': 'scientificName', 
                                                                'vernacularname': 'vernacularName',
                                                                'sourcestatus': 'sourceStatus'})
            
            # check for current status in new south wales
            if 'isCurrent' in sensitive_list_data:
                sensitive_list_data = sensitive_list_data[sensitive_list_data['isCurrent'] == "true"]

            # create a processed sensitive list from the raw data
            sensitive_list = create_sensitive_list(list_data=sensitive_list_data,state=state)

            # write list to csv for upload (may change this later)
            sensitive_list.to_csv("{}-sensitive-{}.csv".format(state,datetime.now().strftime("%Y-%m-%d")),index=False)

        # then, check if state is in conservation URLs
        if state in conservation_list_urls.keys():

            for i in range(len(conservation_list_urls[state])):
                conservation_list_data = pd.concat([conservation_list_data,lf.read_list_url(url=conservation_list_urls[state][i],state=state)]).reset_index(drop=True)

            # do renaming of columns
            conservation_list_data = conservation_list_data.rename(columns={'scientificname': 'scientificName', 
                                                                            'vernacularname': 'vernacularName',
                                                                            'sourcestatus': 'sourceStatus'})
    
            # specific to New South Wales - check if there is a current thing
            if 'isCurrent' in conservation_list_data:
                conservation_list_data = conservation_list_data[conservation_list_data['isCurrent'] == "true"]

            # create conservation list from raw data
            conservation_list = create_conservation_list(list_data=conservation_list_data,state=state)

            # write conservation list to csv (may change this later)
            conservation_list.to_csv("{}-conservation-{}.csv".format(state,datetime.now().strftime("%Y-%m-%d")),index=False)

    # EPBC separately
    EPBC_df = lf.webscrape_list_url(url="https://data.gov.au/data/dataset/threatened-species-state-lists/resource/78401dce-1f40-49d3-92c4-3713d6e34974",
                                    state="EPBC")

    # keep these?
    # 'Listed SPRAT TaxonID', 'Current SPRAT TaxonID'
    EPBC_new = EPBC_df.rename(columns={
        'Scientific Name': 'scientificName', 
        'Common Name': 'vernacularName',        
        'Threatened status': 'sourceStatus',
        'Family': 'family',
        'Genus': 'genus',
        'Species': 'species'
    })

    # "EPBC Act Threatened Species": "dr656",
    EPBC_new['status'] = EPBC_new['sourceStatus']

    EPBC_new[['scientificName', 
              'vernacularName', 
              'sourceStatus',
              'family', 
              'genus', 
              'species',
              'status'
              ]].to_csv("{}-conservation-{}.csv".format("EPBC",datetime.now().strftime("%Y-%m-%d")),index=False)

    # upload lists to the test environment <<=== CHANGE THIS

if __name__ == "__main__":
    main()