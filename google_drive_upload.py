import os
import io
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from misc import *

def authenticate_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    
    if os.path.exists(get_token_file_path()):
        creds = Credentials.from_authorized_user_file(get_token_file_path(), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                get_credential_file_path(), SCOPES)
            creds = flow.run_local_server(port=0)

        # Ensure token is saved in the correct directory
        with open(get_token_file_path(), 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_files_to_google_drive(file_names):
    service = authenticate_google_drive()
    
    # Upload each file
    for file_path, file_name in zip([get_enc_ssh_config_path(), get_salt_bin_path()], file_names):
        file_metadata = {'name': file_name}
        results = service.files().list(
        q=f"name = '{file_name}' and trashed = false",  # Search query for file name
        spaces='drive',  # Search within Google Drive
        fields="files(id, name)").execute()
    
        items = results.get('files', [])
        
        # If file exists, update (overwrite it)
        if items:
            file_id = items[0]['id']
            file_metadata = {'name': file_name}
            media = MediaFileUpload(file_path, mimetype='application/json')
            updated_file = service.files().update(
                fileId=file_id,
                body=file_metadata,
                media_body=media
            ).execute()
            print(f"File {file_name} updated on Google Drive, ID: {updated_file['id']}")
        else:
            # If file doesn't exist, create a new file
            file_metadata = {'name': file_name}
            media = MediaFileUpload(file_path, mimetype='application/json')
            new_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"File {file_name} uploaded to Google Drive, ID: {new_file['id']}")

def download_files_from_google_drive(file_names):
        service = authenticate_google_drive()
        
        # Download each file by name
        for file_name, destination_path in zip(file_names, [get_enc_ssh_config_path(), get_salt_bin_path()]):
            # Search for the file by name
            results = service.files().list(
                q=f"name = '{file_name}' and trashed = false", # Search query for file name
                spaces='drive',  # Search within Google Drive
                fields="files(id, name)").execute()
            
            items = results.get('files', [])
            
            if not items:
                print(f"No file found with the name: {file_name} in Google Drive")
                continue
            
            # Get the file ID of the first matching file
            file_id = items[0]['id']
            
            # Request the file using its ID
            request = service.files().get_media(fileId=file_id)
            
            # Open a local file to store the downloaded content
            fh = io.FileIO(destination_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            
            # Download the file in chunks
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}% for {file_name}.")
            
            print(f"File {file_name} downloaded to {destination_path}")
