import argparse

def create_parser():

    # create parser
    parser = argparse.ArgumentParser(
        description='Remove records in delete csv list from darwin core archive. Specify the type of content to '
                    'determine if extension type or core'
    )

    # add arguments to parser
    parser.add_argument('-cl', '--conservation-lists',help='Conservation lists to process',default='all')
    parser.add_argument('-sl', '--sensitive-lists',help='Sensitive lists to process',default='all')    
    parser.add_argument('-auth', '--authentication',help='Filename with authentication for POST APIs',default='auth-confidential.json')    
    parser.add_argument('-eid', '--email-id',help='Filename with Username and password for email',default='login.txt')    
    parser.add_argument('-cids', '--client-ids',help='Filename with client_id and client_secret_id',default='ids.txt')   
    parser.add_argument('-s3', '--s3-info',help='Filename with s3 bucket and key information',default='s3_info.txt')   
    parser.add_argument('-s3up', '--s3-upload',help='Whether or not to upload lists to AWS',default=True)
    parser.add_argument('-sem', '--send-email',help='Whether or not to send email',default=True)    
    parser.add_argument('-up', '--upload',help='Whether or not to upload lists to AWS',default=True)    
    parser.add_argument('-il', '--ingest-lists',help='Whether to ingest list or edit existing list',default=True) 
    parser.add_argument('-pl', '--post-lists-to-production',help='Whether to post lists to production environment',default=False) 

    parser.add_argument('-v', '--verbose', help='Verbose logging', action='store_true', default=False)

    return parser