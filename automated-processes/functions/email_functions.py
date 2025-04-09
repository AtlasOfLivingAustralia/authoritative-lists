import sys
sys.path.append('../')

from redmail import EmailSender
from datetime import datetime
from pathlib import Path
import markdown

def send_email(conservation_lists = None,
               sensitive_lists = None,
               conservation_dict_changes = None,
               sensitive_dict_changes = None,
               args=None):

    # create list of attachments
    if conservation_dict_changes is not None:
        conservation_changes_states = [k for k,v in conservation_dict_changes.items() if v]
    else: 
        conservation_changes_states = []

    if sensitive_dict_changes is not None:
        sensitive_changes_states = [k for k,v in sensitive_dict_changes.items() if v]
    else:
        sensitive_changes_states = []

    # initiate variables to send in email
    attachments = {}

    # create body of email here using markdown template
    with open('../functions/email_template.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text)

    # denote changes in lists
    conservation_list_changes = ""
    sensitive_list_changes = ""

    # add attachments - first, changelists, then 
    for cs in conservation_changes_states:
        conservation_list_changes+="{}<br />\n".format(cs)
        attachments["{}-conservation-changes-{}.csv".format(cs.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))] = Path("./data/temp-changes/{}-conservation-changes-{}.csv".format(cs.replace(' ','_'),datetime.now().strftime("%Y-%m-%d")))

    if conservation_lists is not None:
        for cs in conservation_lists:    
            attachments["{}-conservation-{}.csv".format(cs.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))] = Path("./data/temp-new-lists/{}-conservation-{}.csv".format(cs.replace(' ','_'),datetime.now().strftime("%Y-%m-%d")))

    for ss in sensitive_changes_states:
        sensitive_list_changes+="{}<br />\n".format(ss)
        attachments["{}-sensitive-changes-{}.csv".format(ss.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))] = Path("./data/temp-changes/{}-sensitive-changes-{}.csv".format(ss.replace(' ','_'),datetime.now().strftime("%Y-%m-%d")))

    if sensitive_lists is not None:    
        for ss in sensitive_lists:
            attachments["{}-sensitive-{}.csv".format(ss.replace(' ','_'),datetime.now().strftime("%Y-%m-%d"))] = Path("./data/temp-new-lists/{}-sensitive-{}.csv".format(ss.replace(' ','_'),datetime.now().strftime("%Y-%m-%d")))

    # add date and time to email
    html = html.replace('CONSERVATION_LIST_OF_CHANGES',conservation_list_changes)
    html = html.replace('SENSITIVE_LIST_OF_CHANGES',sensitive_list_changes)
    html = html.replace('TIME',str(datetime.now().time())[0:8])
    html = html.replace('DATE',str(datetime.now().date()))

    # set up email service
    email = EmailSender(host='smtp-relay.csiro.au',
                        port=25)
    
    email.send(
        sender = "amanda.buyan@csiro.au",
        receivers= ["authoritative-list-updates@ala.org.au"], 
        subject="Authoritative Species Lists Update Week of {}".format(datetime.now()),
        html=html,
        attachments = attachments
    )
    
def get_username_password(args=None):
    '''
    Get client ids and secret for posting data
    '''

    f = open(args.email_id)
    for line in f:
        if 'username' in line:
            username = line.strip().split(" = ")[1]
        if 'password' in line:
            password = line.strip().split(" = ")[1]

    return username,password