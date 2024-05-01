from all_args import create_parser
from ingest_lists import ingest_lists
import email_functions as ef
from vocab import conservation_lists,sensitive_lists

def main():
    
    # generate parser here and get args
    parser = create_parser()
    args = parser.parse_args()

    # check to see if we are running this for all lists - if not, split lists separated by comma
    if args.conservation_lists != 'all':
        args.conservation_lists = args.conservation_lists.split(',')
    else:
        args.conservation_lists = conservation_lists
    if args.sensitive_lists != 'all':
        args.sensitive_lists = args.sensitive_lists.split(',')
    else:
        args.sensitive_lists = sensitive_lists

    # check if we are ingesting lists or not
    if args.ingest_lists:

        # get changes from lists
        conservation_dict_changes,sensitive_dict_changes = ingest_lists(conservation_lists=args.conservation_lists,
                                                                        sensitive_lists=args.sensitive_lists,
                                                                        upload=args.upload)

        # send email to relevant parties
        if args.send_email:
            
            # Send email to relevant parties
            ef.send_email(conservation_dict_changes=conservation_dict_changes,
                        sensitive_dict_changes=sensitive_dict_changes) 
            
    if args.post_lists_to_production:

        print("Amanda write this if interest is there")

if __name__ == '__main__':
    main()