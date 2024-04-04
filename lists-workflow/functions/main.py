import pandas as pd
import list_functions as lf
import email_functions as ef
from vocab import conservation_list_urls,sensitive_list_urls
from vocab import conservation_lists,sensitive_lists,list_ids_sensitive_test,list_ids_sensitive_prod
from vocab import list_ids_conservation_test,list_ids_conservation_prod
from sensitive_vs_conservation import create_conservation_list,create_sensitive_list
from datetime import datetime

# need xlrd???

def main():
    '''
    add comments
    '''

    # ---------------------------------------------------------------------------------------------
    # PART 1: Getting the data
    # 
    # AND
    # 
    # PART 2: Uploading to the test environment
    # ---------------------------------------------------------------------------------------------
    # '''
    for state in conservation_lists:

        print(state)

        # initialise sensitive and conservation list data
        conservation_list_data = pd.DataFrame()

        # get all data
        for i in range(len(conservation_list_urls[state])):
            conservation_list_data = pd.concat([conservation_list_data,lf.read_list_url(url=conservation_list_urls[state][i],state=state)]).reset_index(drop=True)

        # create conservation list from raw data
        conservation_list = create_conservation_list(list_data=conservation_list_data,state=state).reset_index(drop=True)

        # post list to test
        lf.post_list_to_test(list_data=conservation_list,state=state,druid=list_ids_conservation_test[state],list_type="C")
        
        # write conservation list to csv (may change this later)
        # conservation_list.to_csv("../temp-new-lists/{}-conservation-{}.csv".format(state,datetime.now().strftime("%Y-%m-%d")),index=False)

    import sys
    sys.exit()

    for state in sensitive_lists:

        # initialise data
        sensitive_list_data = pd.DataFrame()

        # loop over all links present to get 
        for i in range(len(sensitive_list_urls[state])):
            sensitive_list_data = pd.concat([sensitive_list_data,lf.read_list_url(url=sensitive_list_urls[state][i],state=state)]).reset_index(drop=True)

        # create a processed sensitive list from the raw data
        sensitive_list = create_sensitive_list(list_data=sensitive_list_data,state=state).reset_index(drop=True)

        # post list to test
        # lf.post_list_to_test(list_data=sensitive_list,state=state,druid=list_ids_sensitive_test[state],list_type="S")
        
        # write list to csv for upload (may change this later)
        sensitive_list.to_csv("../temp-new-lists/{}-sensitive-{}.csv".format(state,datetime.now().strftime("%Y-%m-%d")),index=False)
    # '''
    # ---------------------------------------------------------------------------------------------
    # PART 3: Determining changes
    # ---------------------------------------------------------------------------------------------
    # dictionaries of changes
    conservation_dict_changes = {x:False for x in conservation_lists}
    sensitive_dict_changes = {x:False for x in sensitive_lists}

    # loop over sensitive lists
    for state in sensitive_lists:

        print("Sensitive: {}".format(state))
        
        # generate difference report for sensitive list
        sensitive_changelist = lf.get_changelist(list_ids_sensitive_test[state], list_ids_sensitive_prod[state], "S")
        if not sensitive_changelist.empty:
            sensitive_dict_changes[state] = False
            sensitive_changelist.to_csv("../temp-changes/{}-sensitive-changes-{}.csv".format(state,datetime.now().strftime("%Y-%m-%d")))

    # loop over conservation lists
    for state in conservation_lists:

        print("Conservation: {}".format(state))

        # generate difference report for conservation list
        conservation_changelist = lf.get_changelist(list_ids_conservation_test[state], list_ids_conservation_prod[state], "C")
        if not conservation_changelist.empty:
            conservation_dict_changes[state] = "Yes"
            conservation_changelist.to_csv("../temp-changes/{}-conservation-changes-{}.csv".format(state,datetime.now().strftime("%Y-%m-%d")))
    
    # ---------------------------------------------------------------------------------------------
    # PART 4: Send email to Cam
    # ---------------------------------------------------------------------------------------------
    # send email here
    ef.send_email(conservation_dict_changes=conservation_dict_changes,sensitive_dict_changes=sensitive_dict_changes)

if __name__ == "__main__":
    main()