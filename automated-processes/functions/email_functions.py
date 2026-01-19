import sys
from datetime import datetime
from pathlib import Path

import markdown
from redmail import EmailSender

sys.path.append("../")


def send_email(
    conservation_lists=None,
    sensitive_lists=None,
    conservation_dict_changes=None,
    sensitive_dict_changes=None,
    args=None,
):

    # create list of attachments
    conservation_changes_states = process_changes(change_list=conservation_dict_changes)
    sensitive_changes_states = process_changes(change_list=sensitive_dict_changes)

    # initiate variables to send in email
    attachments = {}

    # create body of email here using markdown template
    with open("../functions/email_template.md", "r") as f:
        text = f.read()
        html = markdown.markdown(text)

    # denote changes in lists
    conservation_list_changes = ""
    sensitive_list_changes = ""

    # add attachments for lists and changes
    attachments, conservation_list_changes = add_attachments(
        list_to_check=conservation_changes_states,
        list_type="cc",
        attachments=attachments,
        changes=conservation_list_changes,
    )
    attachments, _ = add_attachments(
        list_to_check=conservation_lists, list_type="c", attachments=attachments
    )
    attachments, sensitive_list_changes = add_attachments(
        list_to_check=sensitive_changes_states,
        list_type="sc",
        attachments=attachments,
        changes=sensitive_list_changes,
    )
    attachments, _ = add_attachments(
        list_to_check=sensitive_lists, list_type="s", attachments=attachments
    )

    # if we are adding the compiled lists, add them here
    if args.compile:
        attachments, _ = add_attachments(list_type="allc", attachments=attachments)
        attachments, _ = add_attachments(list_type="alls", attachments=attachments)

    # add date and time to email
    html = html.replace("CONSERVATION_LIST_OF_CHANGES", conservation_list_changes)
    html = html.replace("SENSITIVE_LIST_OF_CHANGES", sensitive_list_changes)
    html = html.replace("TIME", str(datetime.now().time())[0:8])
    html = html.replace("DATE", str(datetime.now().date()))

    # set up email service
    email = EmailSender(host="smtp-relay.csiro.au", port=25)

    email.send(
        sender="amanda.buyan@csiro.au",
        receivers=["authoritative-list-updates@ala.org.au"],
        subject="Authoritative Species Lists Update Week of {}".format(datetime.now()),
        html=html,
        attachments=attachments,
    )


def get_username_password(args=None):
    """
    Get client ids and secret for posting data
    """

    f = open(args.email_id)
    for line in f:
        if "username" in line:
            username = line.strip().split(" = ")[1]
        if "password" in line:
            password = line.strip().split(" = ")[1]

    return username, password


def add_attachments(list_to_check=None, list_type=None, attachments=None, changes=None):
    """
    Add attachments to the email we send
    """

    # initialise all the different names and paths
    file_names = {
        "cc": "conservation-changes",
        "c": "conservation",
        "sc": "sensitive-changes",
        "s": "sensitive",
        "allc": "all-conservation",
        "alls": "all-sensitive",
    }

    file_paths = {
        "cc": "./data/temp-changes",
        "c": "./data/temp-new-lists",
        "sc": "./data/temp-changes",
        "s": "./data/temp-new-lists",
        "allc": "./data/temp-new-lists",
        "alls": "./data/temp-new-lists",
    }

    # check if we are adding the compiled conservation and sensitive lists
    if list_type in ["allc", "alls"]:

        name = "{}-{}.csv".format(
            file_names[list_type], datetime.now().strftime("%Y-%m-%d")
        )
        print(name)
        path = "{}/{}-{}.csv".format(
            file_paths[list_type],
            file_names[list_type],
            datetime.now().strftime("%Y-%m-%d"),
        )
        attachments[name] = Path(path)

    # if we are not, we are looping over lists
    else:

        for x in list_to_check:
            if list_type in ["cc", "sc"]:
                changes += "{}<br />\n".format(x)
            name = "{}-{}-{}.csv".format(
                x.replace(" ", "_"),
                file_names[list_type],
                datetime.now().strftime("%Y-%m-%d"),
            )
            path = "{}/{}-{}-{}.csv".format(
                file_paths[list_type],
                x.replace(" ", "_"),
                file_names[list_type],
                datetime.now().strftime("%Y-%m-%d"),
            )
            attachments[name] = Path(path)

    # return attachments and changes
    return attachments, changes


def process_changes(change_list=None):
    """
    Select only the items that are present and put them in a list; else, return an empty list
    """

    if change_list is not None:
        return [k for k, v in change_list.items() if v]
    else:
        return []
