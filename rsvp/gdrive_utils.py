# Standard library
import json
import os

# 3rd party
from apiclient.discovery import build
from google.oauth2 import service_account
import requests

# Local library
SERVICE_ACCOUNT_FILE = 'service_account_file.json'


def download_service_account_file():
    url = os.environ['GOOGLE_SERVICE_ACCOUNT_FILE_URL']
    with open(SERVICE_ACCOUNT_FILE, 'w') as f:
        json.dump(requests.get(url).json(), f)


def create_service():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        download_service_account_file()
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=credentials)
    return service


def update_permissions(service, file_id, emails):
    permissions = service.permissions().list(
        fileId=file_id, fields='permissions(id, emailAddress, role)'
    ).execute()
    permissions = [
        permission
        for permission in permissions.get('permissions', [])
        if 'emailAddress' in permission
    ]
    permission_emails = {
        permission['emailAddress'].lower() for permission in permissions
    }
    delete_permissions = [
        permission
        for permission in permissions
        if permission['emailAddress'].lower() not in emails
        and permission['role'] != 'owner'
        and 'gserviceaccount.com' not in permission['emailAddress']
    ]
    new_emails = [email for email in emails if email not in permission_emails]
    print('Adding {} permissions'.format(len(new_emails)))
    print('\n'.join(new_emails))
    for email in new_emails:
        body = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': email,
            'sendNotificationEmail': False,
        }
        service.permissions().create(fileId=file_id, body=body).execute()
    print('Deleting {} permissions'.format(len(delete_permissions)))
    print(
        '\n'.join(
            permission['emailAddress'] for permission in delete_permissions
        )
    )
    for permission in delete_permissions:
        service.permissions().delete(
            fileId=file_id, permissionId=permission['id']
        ).execute()
