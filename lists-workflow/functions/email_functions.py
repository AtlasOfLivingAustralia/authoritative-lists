# import smtplib
from redmail import outlook
from smtplib import SMTP
from datetime import datetime
from pathlib import Path

def send_email(conservation_dict_changes = None,
               sensitive_dict_changes = None):
    
    # smtp = SMTP()
    # smtp.set_debuglevel(2)

    # password_file = open('login.txt')
    # for line in password_file:
    #     if "password" in line:
    #         password = line.strip().split(" = ")[1]
    #     if "username" in line:
    #         username = line.strip().split(" = ")[1]

    # 
    # outlook.username = username
    # outlook.password = password

    # create attachments
    conservation_states = [k for k,v in conservation_dict_changes.items() if v]
    sensitive_states = [k for k,v in sensitive_dict_changes.items() if v]

    attachments = {}
    message_body = "Hi Cam and Tania,\n\nAttached are changes from the following lists:\n\n"

    
    for cs in conservation_states:
        message_body += "{}\n".format(cs)
        attachments["{}-conservation-changes-{}.csv".format(cs,datetime.now().strftime("%Y-%m-%d"))] = Path("../temp-changes/{}-conservation-changes-{}.csv".format(cs,datetime.now().strftime("%Y-%m-%d")))

    for ss in sensitive_states:
        message_body += "{}\n".format(ss)
        attachments["{}-sensitive-changes-{}.csv".format(ss,datetime.now().strftime("%Y-%m-%d"))] = Path("../temp-changes/{}-sensitive-changes-{}.csv".format(cs,datetime.now().strftime("%Y-%m-%d")))
    
    print(attachments)
    print(message_body)

    # print("sending email")
    # outlook.send(
    #     receivers=["amanda.buyan@csiro.au"],
    #     subject="Authoritative Species Lists Update Week of {}".format(datetime.now()),
    #     text=message_body,
    #     attachments = {

    #     }
    # )
    # print("email sent")