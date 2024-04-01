# merge this with the main.py when I automate uploading data via API

import list_functions as lf
from vocab import lists,list_ids_sensitive_test,list_ids_sensitive_prod,list_ids_conservation_test,list_ids_conservation_prod

def main():

    changes_dict = {x:None for x in lists}

    conservation_changelist = lf.get_changelist(list_ids_conservation_test["EPBC"], list_ids_conservation_prod["EPBC"], "C").reset_index(drop=True)
    print("conservation")
    print(conservation_changelist.columns)
    print(conservation_changelist.shape)
    print(conservation_changelist)
    conservation_changelist.to_csv("")
    import sys
    sys.exit()

    for state in lists:
        
        # generate difference report for sensitive list
        sensitive_changelist = lf.get_changelist(list_ids_sensitive_test[state], list_ids_sensitive_prod[state], "S")
        print(sensitive_changelist)
        import sys
        sys.exit()

        # generate difference report for conservation list
        conservation_changelist = lf.get_changelist(list_ids_conservation_test[state], list_ids_conservation_prod[state], "C")


if __name__ == "__main__":
    main()