import pandas as pd
import list_functions as lf
import email_functions as ef
from vocab import conservation_list_urls,sensitive_list_urls,list_ids_sensitive_test,list_ids_sensitive_prod
from vocab import list_ids_conservation_test,list_ids_conservation_prod
from sensitive_vs_conservation import create_conservation_list,create_sensitive_list
from datetime import datetime
import boto3
import os

def ingest_lists(conservation_lists = None,
                 sensitive_lists = None,
                 upload = True):
    '''
    This is the main function for part 1 of successful authoritative lists ingestion.  There 
    are four parts to this process:

    1. Gather the data for each list from each states
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
        s3_info = lf.get_s3_information()

    # make sure local directories exist for writing in
    local_dirs = ['../temp-changes','../temp-new-lists']
    for ld in local_dirs:
        if not os.path.isdir(ld):
            os.mkdir(ld)

    # ---------------------------------------------------------------------------------------------
    # PART 1: Getting the data
    # PART 2: Uploading to the test environment
    # PART 3: Generating changelist to see if list has been updated
    # ---------------------------------------------------------------------------------------------
    for state in conservation_lists:

        # initialise sensitive and conservation list data
        conservation_list_data = pd.DataFrame()

        # get all data
        for i in range(len(conservation_list_urls[state])):
            conservation_list_data = pd.concat([conservation_list_data,lf.read_list_url(url=conservation_list_urls[state][i],state=state)]).reset_index(drop=True)

        # create conservation list from raw data
        conservation_list = create_conservation_list(list_data=conservation_list_data,state=state).reset_index(drop=True)

        # post list to test
        lf.post_list_to_test(list_data=conservation_list,state=state,druid=list_ids_conservation_test[state],list_type="C")
        
        # generate difference report for conservation list
        conservation_changelist = lf.get_changelist(list_ids_conservation_test[state], list_ids_conservation_prod[state], "C")

        # # if there are changes, write them out to a csv for emailing
        if not conservation_changelist.empty:

            # write changes to csv
            conservation_dict_changes[state] = True
            temp_filename = "{}-conservation-changes-{}.csv".format(state.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))
            conservation_changelist.to_csv('../temp-changes/{}'.format(temp_filename))

            # if specified, upload changes
            if upload:
                s3_client.upload_file(Filename = '../temp-changes/{}'.format(temp_filename), 
                                    Bucket = s3_info['bucket'], 
                                    Key = '{}/{}'.format(s3_info['key_conservation_changes'],temp_filename))
    
            # write conservation list to csv (may change this later)
            temp_filename = "{}-conservation-{}.csv".format(state.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))
            conservation_list.to_csv('../temp-new-lists/{}'.format(temp_filename),index=False)

            # check for uploading
            if upload:
                s3_client.upload_file(Filename = '../temp-new-lists/{}'.format(temp_filename), 
                                    Bucket = s3_info['bucket'], 
                                    Key = '{}/{}'.format(s3_info['key_conservation_lists'],temp_filename))

    for state in sensitive_lists:

        # initialise data
        sensitive_list_data = pd.DataFrame()

        # loop over all links present to get 
        for i in range(len(sensitive_list_urls[state])):
            sensitive_list_data = pd.concat([sensitive_list_data,lf.read_list_url(url=sensitive_list_urls[state][i],state=state)]).reset_index(drop=True)

        # create a processed sensitive list from the raw data
        sensitive_list = create_sensitive_list(list_data=sensitive_list_data,state=state).reset_index(drop=True)
        
        # post list to test
        lf.post_list_to_test(list_data=sensitive_list,state=state,druid=list_ids_sensitive_test[state],list_type="S")
        
        # generate difference report for sensitive list
        sensitive_changelist = lf.get_changelist(list_ids_sensitive_test[state], list_ids_sensitive_prod[state], "S")
        
        # if there are changes, write them out to a csv for emailing
        if not sensitive_changelist.empty:

            # generate changelist and write to csv
            sensitive_dict_changes[state] = True
            temp_filename = "{}-sensitive-changes-{}.csv".format(state.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))
            sensitive_changelist.to_csv("../temp-changes/{}".format(temp_filename),index=False)
            
            # upload file to s3
            if upload:
                s3_client.upload_file(Filename = '../temp-changes/{}'.format(temp_filename), 
                                    Bucket = s3_info['bucket'], 
                                    Key = '{}/{}'.format(s3_info['key_sensitive_changes'],temp_filename))
            
            # write list to csv for upload (may change this later)
            temp_filename = "{}-sensitive-{}.csv".format(state.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))
            sensitive_list.to_csv("../temp-new-lists/{}".format(temp_filename),index=False)

            # upload file to s3
            if upload:
                s3_client.upload_file(Filename = '../temp-new-lists/{}'.format(temp_filename), 
                                    Bucket = s3_info['bucket'], 
                                    Key = '{}/{}'.format(s3_info['key_sensitive_lists'],temp_filename))
        
    return conservation_dict_changes,sensitive_dict_changes   