#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import dropbox

class TransferData:
    """
    Class used for transfering data to and from the Air Partners Dropbox account.

    NOTES: The strings currently used in this file are for a test Dropbox made with a test email.
    Air Partners must make its own Dropbox account with its own email, and this setup will have to 
    be reproduced. The link below explains how to get the refresh token after an app has been 
    configured.

    Make sure that all these strings, after being created, are either locally stored on the virtual
    machine or are in a text document/JSON file and not in the Python files themselves. No need to risk
    putting this information on a public Github repository.

    https://stackoverflow.com/questions/70641660/how-do-you-get-and-use-a-refresh-token-for-the-dropbox-api-python-3-x/71794390#71794390
    """
    def __init__(self, access_token):
        self.access_token = access_token
        self.dbx = dropbox.Dropbox(
            app_key="mmjq6lg4l2r26ji",
            app_secret="giev935reiteb53",
            oauth2_refresh_token="sQsMlNWiaFUAAAAAAAAAAcqGo6p3GB4RBUwlcOYt0Bu66x8WY4wxkaQna3rksJaL"
        )

    def upload_file(self, file_from, file_to):
        """
        upload a file to Dropbox using API v2
        """

        with open(file_from, 'rb') as f:
            self.dbx.files_upload(f.read(), file_to)
        
    def delete_file(self, file):
        """
        delete a file from Dropbox using API v2
        """

        self.dbx.files_delete(file)

def upload_zip(year_month):
    """
    Uploads a zip specified by year_month to the Air Partners Dropbox account.
    """
    access_token = 'sl.BKlKBM7pMWcicziqGA2GFl8io_RNkBA4dnvkk0gcvxeZxMQCkuFiW0XqZmlWWaQ-h9lDQvqlQx87ElYwTvdkPp4WP1Zb0eDlbaMr620YJuVjND5jXzHDbUFFXJS-76MTBHjctVPr'
    transferData = TransferData(access_token)

    # zip file name
    zip_name = f'{year_month}.zip'

    # create file start and destination locations
    file_from = f'zips/{zip_name}'
    file_to = f'/Report_Zips/{zip_name}'  # The full path to upload the file to, including the file name

    # API v2 --> upload file to Dropbox
    transferData.upload_file(file_from, file_to)

def delete_zip(year_month_prev):
    """
    If it exists, deletes the zip file of reports from the previous month from
    the Air Partners Dropbox account.
    """
    access_token = 'sl.BKlKBM7pMWcicziqGA2GFl8io_RNkBA4dnvkk0gcvxeZxMQCkuFiW0XqZmlWWaQ-h9lDQvqlQx87ElYwTvdkPp4WP1Zb0eDlbaMr620YJuVjND5jXzHDbUFFXJS-76MTBHjctVPr'
    transferData = TransferData(access_token)

    # zip file name
    zip_name = f'{year_month_prev}.zip'

    file_to_delete = f'/Report_Zips/{zip_name}'  # The full path to upload the file to, including the file name

    # API v2 --> upload file to Dropbox
    transferData.delete_file(file_to_delete)


if __name__ == '__main__':
    year_month = sys.argv[1]
    upload_zip(year_month)
    if len(sys.argv) > 2:
        year_month_prev = sys.argv[1]
        # try deleting previous month; if it does not exist, throw exception and continue
        try:
            delete_zip(year_month_prev)
        except:
            print(f'No file from {year_month_prev} exists in Air Partners account.')
