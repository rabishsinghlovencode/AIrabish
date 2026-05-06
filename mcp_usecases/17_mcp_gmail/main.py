

from mcp.server.fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.readonly']

def get_credentials():
    creds = None
    if not os.path.exists('token.json'):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    else:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return creds

mcp =FastMCP("Gmail")

@mcp.tool()
def create_draft(subject: str, to: str, body: str, content_type: str = "text/plain"):
    """This tool is used to create a draft message in gmail.
    Args:subject :- Subject of the mail
                    to - recipient of the mail
                    body :- body of the draft
    return : response of Gmail API"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(body, _subtype=content_type.split('/')[-1])
    message['to'] = to
    message['from'] = "me"
    message['subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    send_result = service.users().drafts().create(userId="me", body={"message": {"raw": encoded_message}}).execute()

    return send_result

@mcp.tool()
def send_mail(subject: str, to: str, body: str, content_type: str = "text/plain"):
    """This tool is used to send mail from gmail to users .
    Args :  Subject - subject for the Email.
            To - recepient of the mail.
            Body - Body of the test .
    Return : response of the send mail"""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(body, _subtype=content_type.split('/')[-1])
    message['to'] = to
    message['from'] = "me"
    message['subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_result = service.users().messages().send(
        userId="me",
        body={'raw': encoded_message}
    ).execute()

    return send_result

@mcp.tool()
def read_labels():
    """this tool is used to read labels from gmail"""
    creds =get_credentials()
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    return results

if __name__ == "__main__":
    mcp.run()