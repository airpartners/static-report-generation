"""
Author: Andrew DeCandia
Project: Air Partners

Script for pulling form data from google drives.
"""
from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.refresh_google_token import refreshToken

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def pull_sensor_install_data():
    """
    Prints the names and ids of the first 10 files the user has access to.
    """
    # After authorization flow has run for the first time, token must be refreshed
    refreshToken()
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        items = {'maillist': '17GP7PlQYxr1A1_1srrSDpLjCplLztdHWG51XY2qZoVo',
                 'sensor_install_data': '15DDTqQkXqD16vCnOBBTz9mPUmVWnKywjxdNWF9N6Gcg'}

        print('Pulling sensor install data from google drive...')
        for key in items:
            # Call the Drive v3 API
            info = service.files().export(
                fileId=items[key], mimeType='text/csv').execute()
            with open(f'{key}.csv', 'wb') as f:
                f.write(info)

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    pull_sensor_install_data()
