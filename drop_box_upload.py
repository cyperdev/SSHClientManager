import json
import os
from misc import *
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Load the configuration file for Dropbox credentials
def load_drop_box_config():
    drop_box_path = get_drop_box_config_path()  # Get the path to the config file
    if os.path.exists(drop_box_path):
        with open(drop_box_path, 'r') as file:
            config_data = json.load(file)  # Load JSON data
            app_key = config_data.get('app_key', '') 
            app_secret = config_data.get('app_secret', '')
            oauth2_refresh_token = config_data.get('refresh_token', '') 
            return app_key, app_secret, oauth2_refresh_token
    else:
        raise FileNotFoundError(f"Config file not found at {drop_box_path}")

# Authenticate and get session cookie
def login_to_drop_box():
    app_key, app_secret, oauth2_refresh_token = load_drop_box_config()
    
    dbx = dropbox.Dropbox(
            app_key = app_key,
            app_secret = app_secret,
            oauth2_refresh_token = oauth2_refresh_token
        )

    return dbx

# Upload file to Dropbox
def upload_files_to_dropbox(file_names):
    dbx = login_to_drop_box()
    if dbx:  # Check if login was successful
        for file_path, file_name in zip([get_enc_ssh_config_path(), get_salt_bin_path()], file_names):
            with open(file_path, 'rb') as f:  # Open the file in binary read mode
                # Ensure the path starts with a slash, since Dropbox paths must be absolute
                drive_path = f"/{file_name}"
                dbx.files_upload(f.read(), drive_path, mode=WriteMode('overwrite'))
                print(f"uploaded - File {file_name}")


# Download file from Dropbox
def download_files_from_dropbox(file_names):
    dbx = login_to_drop_box()
    if dbx:  # Check if login was successful
        for file_path, file_name in zip([get_enc_ssh_config_path(), get_salt_bin_path()], file_names):
            drive_path = f"/{file_name}"
            result = dbx.files_search_v2(file_name)
            matches = result.matches  # The list of matched files
            if matches:
                dbx.files_download_to_file(file_path, drive_path)
                print(f"File {file_name} downloaded to {file_path}")
            else:
                print(f"No matches found for {file_name}.")
