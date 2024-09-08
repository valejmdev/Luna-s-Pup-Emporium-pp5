import os
import base64
from urllib.request import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def send_email(to, subject, body):
    service = get_gmail_service()
    message = {
        'raw': base64.urlsafe_b64encode(
            (
                f"From: your_email@gmail.com\n"
                f"To: {to}\n"
                f"Subject: {subject}\n\n"
                f"{body}"
            ).encode("utf-8")
        ).decode("utf-8")
    }
    service.users().messages().send(userId='me', body=message).execute()
