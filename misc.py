import os
import re
import json

def create_directory_file():
    # Get the home directory of the user (cross-platform)
    home_dir = os.path.expanduser("~")
    
    # Path for the new directory
    directory_path = os.path.join(home_dir, ".ssh_client_manager")

    # Check if the directory already exists
    if not os.path.exists(directory_path):
        try:
            # Create the directory
            os.makedirs(directory_path)
            print(f"Directory '{".ssh_client_manager"}' created successfully at {directory_path}")
        except Exception as e:
            print(f"Error creating directory: {e}")
    else:
        print(f"Directory '{".ssh_client_manager"}' already exists at {directory_path}")

    # path for mega config file
    file_path = os.path.join(directory_path, "drop_box_config.json")
    
    # Check if the file already exists
    if not os.path.exists(file_path):
        # If not, create the file
        try:
            # Example data to write to the file (can be customized)
            drop_box_config_data = {
                "token" : ""
            }
            
            with open(file_path, 'w') as f:
                json.dump(drop_box_config_data, f, indent=4)
                print(f"'drop_box_config.json' created at {file_path}")
        except Exception as e:
            print(f"Error creating drop_box_config.json file: {e}")
            return None
    else:
        print(f"'drop_box_config.json' already exists at {file_path}")
    
    return directory_path

def get_drop_box_config_path():
    drop_box_config_path = os.path.join(folder_path, "drop_box_config.json")
    return drop_box_config_path

def get_enc_ssh_config_path():
    enc_ssh_config_path = os.path.join(folder_path, "enc_ssh_config.json")
    return enc_ssh_config_path

def get_salt_bin_path():
    salt_bin_path = os.path.join(folder_path, "salt.bin")
    return salt_bin_path

def get_token_file_path():
    token_file_path = os.path.join(folder_path, "token.json")
    return token_file_path

def get_credential_file_path():
    credentials_file_path = os.path.join(folder_path, "credentials.json")
    return credentials_file_path

def get_non_empty_input(prompt, default=None):
    """Prompts the user for input and ensures it's not empty."""
    while True:
        user_input = input(prompt).strip()
        if not user_input and default:
            return default  # If no input is given, return the default value
        elif user_input:
            return user_input  # Return the user input if it's not empty
        else:
            print("This field cannot be empty. Please try again.")

def is_valid_ip(host):
    """Validates if the provided host is a valid IP address."""
    # Regex pattern to check for valid IP address (IPv4 format)
    pattern = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
    return bool(pattern.match(host))

def clean_output(output):
    # print(f"Output with escape characters: {repr(output)}")
    
    # Remove backspace characters
    cleaned_output_1 = re.sub(r'\x08', '', output)
    # Remove ANSI escape sequences
    ansi_escape = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
    cleaned_output_2 = ansi_escape.sub('', cleaned_output_1)
    # Remove null bytes
    cleaned_output_3 = re.sub(r'\x00', '', cleaned_output_2)
    # Remove other control characters
    control_escape = re.compile(r'[\x00-\x1F\x7F]')
    cleaned_output_final = control_escape.sub('', cleaned_output_3)

    # print(repr(cleaned_output_final))

    return cleaned_output_final.strip()

folder_path = create_directory_file()