import pandas as pd
from . import list_functions as lf
from .vocab import conservation_list_urls,sensitive_list_urls,list_ids_sensitive_test,list_ids_sensitive_prod
from .vocab import list_ids_conservation_test,list_ids_conservation_prod,get_listsProd,urlSuffix,all_sensitive_lists
from .vocab import get_listsTest
from .sensitive_vs_conservation import create_conservation_list,create_sensitive_list
from datetime import datetime
import boto3
import os

def ingest_lists(conservation_lists = None,
                 sensitive_lists = None,
                 upload = True,
                 args = None):
    '''
    This is the main function for part 1 of successful authoritative lists ingestion.  There 
    are four parts to this process:

    1. Gather the data for each list from each state
    2. Upload data to the test environment for verification of name matching
    3. Generate changelist to see updates to lists
    4. Email changes to relevant parties
    '''

    #'''
    # ---------------------------------------------------------------------------------------------
    # PART 0: Declaring variables for change lists and s3 bucket
    # ---------------------------------------------------------------------------------------------
    
    # initialise dictionaries
    conservation_dict_changes = {x:False for x in conservation_lists}
    sensitive_dict_changes = {x:False for x in sensitive_lists}

    # set up access to s3 bucket
    if upload:
        s3_session = boto3.Session(profile_name='prod-data-team-s3')
        s3_client = s3_session.client('s3') 
        s3_info = lf.get_s3_information(args=args)

    # make sure local directories exist for writing in
    local_dirs = ['data/temp-changes','data/temp-new-lists','data/temp-historical-lists']
    for ld in local_dirs:
        if not os.path.isdir(ld):
            os.mkdir(ld)

    # ---------------------------------------------------------------------------------------------
    # PART 1: Getting the data
    # PART 2: Uploading to the test environment
    # PART 3: Generating changelist to see if list has been updated
    # ---------------------------------------------------------------------------------------------
    if conservation_lists is not None:

        for state in conservation_lists:

            print(state)

            # initialise sensitive and conservation list data
            conservation_list_data = pd.DataFrame()

            # get all data
            for i in range(len(conservation_list_urls[state])):
                conservation_list_data = pd.concat([conservation_list_data,lf.read_list_url(url=conservation_list_urls[state][i],state=state)]).reset_index(drop=True)

            # create conservation list from raw data
            conservation_list = create_conservation_list(list_data=conservation_list_data,state=state).reset_index(drop=True)

            # add IUCN status
            conservation_list['IUCN_equivalent_status'] = conservation_list['status'].copy()

            # trim whitespace at end of strings
            conservation_list = conservation_list.replace(r"^ +| +$", r"", regex=True)
            
            # add, change or delete list values as appropriate
            conservation_list = lf.add_change_delete_list_values(list_type = 'Conservation',list_data=conservation_list,state=state)
        
            # write conservation list to csv (may change this later)
            temp_filename = "{}-conservation-{}.csv".format(state.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))
            conservation_list.to_csv('data/temp-new-lists/{}'.format(temp_filename),index=False)
            #os.system('ln -s data/temp-new-lists/{} {}'.format(temp_filename,temp_filename))

            # post list to test
            # lf.post_list_to_test(druid=list_ids_conservation_test[state],filename=temp_filename,args=args)
            lf.post_list_to_test(list_data=conservation_list,state=state,druid=list_ids_conservation_test[state],list_type="C",args=args)
 
            # get old and new list urls    
            oldListUrl = get_listsProd + list_ids_conservation_prod[state] + urlSuffix

            # download old list and turn it into pandas dataframe
            oldList = lf.download_ala_specieslist(oldListUrl)
            oldList = lf.kvp_to_columns(oldList)

            temp_filename = "{}-conservation-historical-{}.csv".format(state.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))
            oldList.to_csv('data/temp-historical-lists/{}'.format(temp_filename))

            # if specified, upload changes
            if upload:
                s3_client.upload_file(Filename = 'data/temp-historical-lists/{}'.format(temp_filename), 
                                    Bucket = s3_info['bucket'], 
                                    Key = '{}/{}'.format(s3_info['key_conservation_historical'],temp_filename))

            # generate difference report for conservation list
            conservation_changelist = lf.get_changelist(list_ids_conservation_test[state], list_ids_conservation_prod[state], "C")

            # # if there are changes, write them out to a csv for emailing
            if not conservation_changelist.empty:

                # write changes to csv
                conservation_dict_changes[state] = True
                temp_filename = "{}-conservation-changes-{}.csv".format(state.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))
                conservation_changelist.to_csv('data/temp-changes/{}'.format(temp_filename))

                # if specified, upload changes
                if upload:
                    s3_client.upload_file(Filename = 'data/temp-changes/{}'.format(temp_filename), 
                                        Bucket = s3_info['bucket'], 
                                        Key = '{}/{}'.format(s3_info['key_conservation_changes'],temp_filename))

            # check for uploading
            if upload:
                s3_client.upload_file(Filename = 'data/temp-new-lists/{}'.format(temp_filename), 
                                    Bucket = s3_info['bucket'], 
                                    Key = '{}/{}'.format(s3_info['key_conservation_lists'],temp_filename))

    print()
    
    if sensitive_lists is not None:
        for state in sensitive_lists:

            print(state)

            # initialise data
            sensitive_list_data = pd.DataFrame()

            # loop over all links present to get 
            for i in range(len(sensitive_list_urls[state])):
                sensitive_list_data = pd.concat([sensitive_list_data,lf.read_list_url(url=sensitive_list_urls[state][i],state=state)]).reset_index(drop=True)

            # create a processed sensitive list from the raw data
            sensitive_list = create_sensitive_list(list_data=sensitive_list_data,state=state).reset_index(drop=True)
            
            # trim whitespace at end of strings
            sensitive_list = sensitive_list.replace(r"^ +| +$", r"", regex=True)

            # add, change or delete list values as appropriate
            sensitive_list = lf.add_change_delete_list_values(list_type = 'Sensitive',list_data=sensitive_list,state=state)
            
            # write list to csv for upload (may change this later)
            temp_filename = "{}-sensitive-{}.csv".format(state.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))
            sensitive_list.to_csv("data/temp-new-lists/{}".format(temp_filename),index=False)
            #os.system('ln -s data/temp-new-lists/{} {}'.format(temp_filename,temp_filename))

            # post list to test
            # lf.post_list_to_test(druid=list_ids_sensitive_test[state],filename=temp_filename,args=args)
            lf.post_list_to_test(list_data=sensitive_list,state=state,druid=list_ids_sensitive_test[state],list_type="S",args=args)
            
            # get old and new list urls    
            oldListUrl = get_listsProd + list_ids_sensitive_prod[state] + urlSuffix
            oldList = lf.download_ala_specieslist(oldListUrl)

            oldList = lf.kvp_to_columns(oldList)
            temp_filename = "{}-sensitive-historical-{}.csv".format(state.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))
            oldList.to_csv('data/temp-historical-lists/{}'.format(temp_filename))

            # if specified, upload changes
            if upload:
                s3_client.upload_file(Filename = 'data/temp-historical-lists/{}'.format(temp_filename), 
                                    Bucket = s3_info['bucket'], 
                                    Key = '{}/{}'.format(s3_info['key_sensitive_historical'],temp_filename))

            # generate difference report for sensitive list
            sensitive_changelist = lf.get_changelist(list_ids_sensitive_test[state], list_ids_sensitive_prod[state], "S")

            # if there are changes, write them out to a csv for emailing
            if not sensitive_changelist.empty:

                # generate changelist and write to csv
                sensitive_dict_changes[state] = True
                temp_filename = "{}-sensitive-changes-{}.csv".format(state.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))
                sensitive_changelist.to_csv("data/temp-changes/{}".format(temp_filename),index=False)
                
                # upload file to s3
                if upload:
                    s3_client.upload_file(Filename = 'data/temp-changes/{}'.format(temp_filename), 
                                        Bucket = s3_info['bucket'], 
                                        Key = '{}/{}'.format(s3_info['key_sensitive_changes'],temp_filename))
                
            # upload file to s3
            if upload:
                s3_client.upload_file(Filename = 'data/temp-new-lists/{}'.format(temp_filename), 
                                    Bucket = s3_info['bucket'], 
                                    Key = '{}/{}'.format(s3_info['key_sensitive_lists'],temp_filename))
    
    '''
    # initialise the dataframe and column names for all sensitive lists compilation
    raw_sciName = ['raw_scientificName_{}'.format(state) for state in all_sensitive_lists]
    categories = ['category_{}'.format(state) for state in all_sensitive_lists]
    generalisation = ['generalisation_{}'.format(state) for state in all_sensitive_lists]
    columns = ['scientificName','family','kingdom'] + raw_sciName + categories + generalisation
    all_sensitive = pd.DataFrame(columns=columns)

    # loop over all sensitive lists
    for state in all_sensitive_lists:

        # download state/territory/birds sensitive
        url = get_listsTest + list_ids_sensitive_test[state] + urlSuffix
        kvps_sensitive = lf.download_ala_specieslist(url=url)
        sensitive_df = lf.kvp_to_columns(kvps_sensitive)

        # check for raw_scientificName
        if 'raw_scientificName' not in sensitive_df.columns:
            sensitive_df['raw_scientificName'] = sensitive_df['scientificName'].copy()

        # rename columns for 
        sensitive_df = sensitive_df.rename(columns={
            'raw_scientificName': 'raw_scientificName_{}'.format(state),
            'category': 'category_{}'.format(state),
            'generalisation': 'generalisation_{}'.format(state)
        })

        # find column names missing and add them
        headings_difference = [c for c in columns if c not in list(sensitive_df.columns)]
        for heading in headings_difference:
            sensitive_df[heading] = ['' for i in range(sensitive_df.shape[0])]

        # add sensitive lists to overall list
        all_sensitive = pd.concat([all_sensitive,sensitive_df[columns]]).reset_index(drop=True)

    # post list to test
    lf.post_list_to_test(list_data=sensitive_list,state=state,druid=list_ids_sensitive_test[state],list_type="S",args=args)  

    # write list to csv for upload (may change this later)
    temp_filename = "all-sensitive-lists-{}.csv".format(datetime.now().strftime("%Y-%m-%d"))
    all_sensitive.to_csv("data/temp-new-lists/{}".format(temp_filename),index=False)
    '''
    return conservation_dict_changes,sensitive_dict_changes   