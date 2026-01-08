import sys

from functions import email_functions as ef
from functions.all_args import create_parser
from functions.ingest_lists import ingest_lists
from functions.list_functions import set_bool_argument, set_lists_to_run
from functions.compile_conservation_lists import compile_conservation_lists
from functions.compile_sensitive_lists import compile_sensitive_lists

sys.path.append("../")


def main():

    # generate parser here and get args
    parser = create_parser()
    args = parser.parse_args()

    # First, check for sending email bool
    args.send_email = set_bool_argument(arg=args.send_email, name_arg="send_email")
    args.upload = set_bool_argument(arg=args.upload, name_arg="upload")
    args.compile = set_bool_argument(arg=args.compile, name_arg="compile")

    # set the lists we will check
    args.conservation_lists = set_lists_to_run(
        lists=args.conservation_lists, C=True, S=False
    )
    args.sensitive_lists = set_lists_to_run(lists=args.sensitive_lists, C=False, S=True)

    # get changes from lists
    conservation_dict_changes, sensitive_dict_changes = ingest_lists(
        conservation_lists=args.conservation_lists,
        sensitive_lists=args.sensitive_lists,
        upload=args.upload,
        args=args,
    )

    # create the compiled sensitive lists
    if args.compile:
        compile_conservation_lists(args=args)
        compile_sensitive_lists(args=args)

    # check to see if we are sending an email
    if args.send_email:

        # Send email to relevant parties
        ef.send_email(
            conservation_dict_changes=conservation_dict_changes,
            sensitive_dict_changes=sensitive_dict_changes,
            conservation_lists=args.conservation_lists,
            sensitive_lists=args.sensitive_lists,
            args=args,
        )


if __name__ == "__main__":
    main()
