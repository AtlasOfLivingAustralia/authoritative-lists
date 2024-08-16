from functions.all_args import create_parser
from functions.ingest_lists import ingest_lists
import functions.email_functions as ef
from functions.vocab import conservation_lists,sensitive_lists

def main():
    
    # generate parser here and get args
    parser = create_parser()
    args = parser.parse_args()

    # First, check for sending email bool
    if type(args.send_email) is str:
        if args.send_email == "False":
            args.send_email = False
        elif args.send_email == "True":
            args.send_email = True
        else:
            raise ValueError("Only True and False values are accepted for sending email")

    # First, check for sending email bool
    if type(args.upload) is str:
        if args.upload == "False":
            args.upload = False
        elif args.upload == "True":
            args.upload = True
        else:
            raise ValueError("Only True and False values are accepted for sending email")

    # check to see if we are running this for all lists - if not, split lists separated by comma
    if args.conservation_lists != 'all' and args.conservation_lists != 'None':
        temp_list = args.conservation_lists.split(',')
        for i,t in enumerate(temp_list):
            if "_" in t:
                temp_list[i] = t.replace("_"," ")
        args.conservation_lists = temp_list
    elif args.conservation_lists == 'None':
        args.conservation_lists = []
    else:
        args.conservation_lists = conservation_lists

    # get list of all sensitive lists you want to generate
    if args.sensitive_lists != 'all' and args.sensitive_lists != 'None':
        temp_list = args.sensitive_lists.split(',')
        for i,t in enumerate(temp_list):
            if "_" in t:
                temp_list[i] = t.replace("_"," ")
        args.sensitive_lists = temp_list
    elif args.sensitive_lists == 'None':
        args.sensitive_lists = []
    else:
        args.sensitive_lists = sensitive_lists

    # # check if we are ingesting lists or not
    # if args.ingest_lists:

    # get changes from lists
    conservation_dict_changes,sensitive_dict_changes = ingest_lists(conservation_lists=args.conservation_lists,
                                                                    sensitive_lists=args.sensitive_lists,
                                                                    upload=args.upload,
                                                                    args=args)

    # send email to relevant parties
    if args.send_email:
        
        # Send email to relevant parties
        ef.send_email(conservation_dict_changes=conservation_dict_changes,
                      sensitive_dict_changes=sensitive_dict_changes,
                      args=args) 
            
    # post given lists to production
    # if args.post_lists_to_production:

if __name__ == '__main__':
    main()