# import smtplib
from redmail import outlook
from smtplib import SMTP

def send_email(conservation_changes = None,
               sensitive_changes = None):
    
    smtp = SMTP()
    smtp.set_debuglevel(2)

    password_file = open('login.txt')
    for line in password_file:
        if "password" in line:
            password = line.strip().split(" = ")[1]
        if "username" in line:
            username = line.strip().split(" = ")[1]

    outlook.username = username
    outlook.password = password
    
    print("sending email")
    outlook.send(
        receivers=["amanda.buyan@csiro.au"],
        subject="An example",
        text="Hi, this is an example."
    )
    print("email sent")

# attachments =  attachments={
    #     'data.csv': Path('path/to/file.csv'),
    #     'data.xlsx': pd.DataFrame(...),
    #     'raw_file.html': '<h1>Just some HTML</h1>',
    # }
    

    # sensitive_changelist.to_csv("../temp-changes/{}-sensitive-changes-{}.csv".format(state,datetime.now().strftime("%Y-%m-%d")))

    '''
    import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


def send_mail(send_from, send_to, subject, text, files=None,
              server="127.0.0.1"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
    '''