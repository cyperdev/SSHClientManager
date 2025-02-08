import paramiko
import sys
import select
import termios
import tty
import json
import getpass
from misc import *
from google_drive_upload import *
from file_encryption import *
from drop_box_upload import *
import os

class SSHClientManager:
    def __init__(self):
        self.ENC_CONFIG_FILE = os.path.basename(get_enc_ssh_config_path())
        self.SALT_FILE = os.path.basename(get_salt_bin_path())
        self.TOKEN_FILE = os.path.basename(get_token_file_path())
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.nickname = None
        self.key = None
        self.GDrive_upload = False
        self.DBox_upload = False
        self.password_attempts = 0 # Counter for password attempts
    
    def save_encrypted_config(self):
        """Loads, updates, and securely re-encrypts the SSH configuration file."""
        attempts = 0  # Track password attempts
        while attempts < 3:  # Limit number of attempts for password entry
            # Load existing configurations or initialize an empty list if the file is empty or doesn't exist
            self.key = derive_key(getpass.getpass("Enter encryption password: "))
            existing_configs = self.load_encrypted_config() or []

            if existing_configs != "incorrect_password":
                if not existing_configs:
                    print("No existing configurations found. Starting fresh.")
                else:
                    print(f"Existing configurations loaded.")

                # Flag to track whether the nickname was found and updated
                nickname_found = False

                # Check if the nickname already exists to update it instead of duplicating
                for config in existing_configs:
                    if config["nickname"] == self.nickname:
                        config.update({
                            "host": self.host,
                            "port": self.port,
                            "username": self.username,
                            "password": self.password
                        })
                        nickname_found = True
                        break

                # If no existing entry, add a new one
                if not nickname_found:
                    existing_configs.append({
                        "nickname": self.nickname,
                        "host": self.host,
                        "port": self.port,
                        "username": self.username,
                        "password": self.password
                    })

                # Encrypt and save the entire updated list of configurations
                encrypted_data = encrypt_data(json.dumps(existing_configs).encode(), self.key)
                
                if self.GDrive_upload:
                    with open(get_enc_ssh_config_path(), "w") as file:
                        file.write(encrypted_data)

                    file_names_to_upload = [self.ENC_CONFIG_FILE, self.SALT_FILE]

                    upload_files_to_google_drive(file_names_to_upload)

                    print(f"Encrypted '{self.nickname}' credentials uploaded to Google Drive.")

                    # Remove files locally after successful upload
                    for file_path in [get_enc_ssh_config_path(), get_salt_bin_path()]:
                        if os.path.exists(file_path):  # Ensure the file exists before deletion
                            os.remove(file_path)
                            print(f"Deleted the file locally: {file_path}")
                            self.GDrive_upload = False
                elif self.DBox_upload:
                    with open(get_enc_ssh_config_path(), "w") as file:
                        file.write(encrypted_data)

                    file_names_to_upload = [self.ENC_CONFIG_FILE, self.SALT_FILE]

                    upload_files_to_dropbox(file_names_to_upload)

                    print(f"Encrypted '{self.nickname}' credentials uploaded to Drop Box.")

                    # Remove files locally after successful upload
                    for file_path in [get_enc_ssh_config_path(), get_salt_bin_path()]:
                        if os.path.exists(file_path):  # Ensure the file exists before deletion
                            os.remove(file_path)
                            print(f"Deleted the file locally: {file_path}")
                            self.DBox_upload = False
                else:
                    with open(get_enc_ssh_config_path(), "w") as file:
                        file.write(encrypted_data)

                    print(f"Encrypted '{self.nickname}' credentials saved.")
                break  # Exit the loop after saving successfully
            
            else:
                attempts += 1
                print(f"Failed to decrypt. Incorrect password. Attempt {attempts}/3.")
                if attempts == 3:
                    print("Too many failed attempts. Exiting...")
                    break  # Exit after 3 failed attempts

    def load_encrypted_config(self):
        if os.path.exists(get_enc_ssh_config_path()):
            with open(get_enc_ssh_config_path(), "r") as file:
                encrypted_data = file.read()
            try:
                return json.loads(decrypt_data(encrypted_data, self.key).decode())
            except Exception:
                print("Failed to decrypt. Incorrect password?")
                return "incorrect_password"
        return None

    def select_saved_session(self):
        """Prompts the user to select a saved SSH Credentials."""
        configs = self.load_encrypted_config()

        if configs != "incorrect_password":
            if len(configs) == 1:
                # Automatically load if only one Credentials is saved
                selected_config = configs[0]
                self.host = selected_config["host"]
                self.port = selected_config["port"]
                self.username = selected_config["username"]
                self.nickname = selected_config["nickname"]
                self.password = selected_config["password"]

                print(f"Only one credentials found. Credential for '{self.nickname}' loaded.")

                return True
            else:
                while True:
                    # Multiple saved credentials, show the choices
                    print("Multiple saved credentials found. Please select one to load:")
                    for index, config in enumerate(configs):
                        print(f"{index + 1}. {config['nickname']} ({config['host']}) ({config['username']})")

                    choice = get_non_empty_input("Enter the number of the credential you want to load: ")
                    # if chice is other than the loaded it need to say invalid input and start again
                    try:
                        selected_config = configs[int(choice) - 1]
                        self.host = selected_config["host"]
                        self.port = selected_config["port"]
                        self.username = selected_config["username"]
                        self.nickname = selected_config["nickname"]
                        self.password = selected_config["password"]

                        print(f"Credential '{self.nickname}' loaded.")
                        return True
                    except (IndexError, ValueError):
                        print("Invalid choice. Please try again.")
                        
        elif configs == "incorrect_password":
            print("Failed to decrypt. Incorrect password?")
            return False
        else:
            print("No saved credentials found.")
        return False

    def interactive_ssh(self, save_choice):
        """Starts an interactive SSH session."""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)

                self.password_attempts = 0
                if save_choice == "yes":
                    self.save_encrypted_config()
            except paramiko.ssh_exception.AuthenticationException as e:
                self.password_attempts += 1
                print(f"Password verification failed! Attempt {self.password_attempts}/3. Please try again.")
                if self.password_attempts == 3:
                    print("Too many failed attempts. Exiting...")
                    sys.exit(1)
                return "WRONG"

            channel = ssh.invoke_shell()
            print(f"Connected to {self.host}. Press Ctrl+C to interrupt commands, type 'exit' to quit.")

            old_tty = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin)
                tty.setcbreak(sys.stdin)

                while True:
                    # Check for data from the SSH channel
                    rlist, _, _ = select.select([sys.stdin, channel], [], [], 1)
                    if sys.stdin in rlist:  # User input
                        char = sys.stdin.read(1)
                        if char == "\x03":  # Ctrl + C
                            channel.send("\x03")
                        else:
                            channel.send(char)

                    if channel in rlist:  # Output from the channel
                        if channel.recv_ready():
                            output = channel.recv(4096).decode()
                            sys.stdout.write(output)
                            sys.stdout.flush()

                            # Check if output is 'exit' or 'logout'
                            if output.lower().strip() == "exit" or output.lower().strip() == "logout":
                                print("Logout detected. Closing connection.")
                                break

                        # Handle error messages from the server
                        while channel.recv_stderr_ready():
                            sys.stderr.write(channel.recv_stderr(4096).decode())
                            sys.stderr.flush()

            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)
        
        except KeyboardInterrupt as ke:
            print(f"Key board interrupt found: {ke}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            ssh.close()

    def run(self):
        """Main entry point for running the SSH client manager."""
        try:
            while True:
                print("1. Import saved credentials locally (Requires Salt.bin and enc_ssh_config.json files)")
                print("2. Import saved credentials from Google Drive (Requires Salt.bin and enc_ssh_config.json files)")
                print("3. Import saved credentials from Drop Box (Requires Salt.bin and enc_ssh_config.json files)")
                print("4. Enter new SSH details without saving")
                print("5. Enter new SSH details and save credentials in encrypted files locally")
                print("6. Enter new SSH details and save credentials in encrypted files and upload to Google Drive")
                print("7. Enter new SSH details and save credentials in encrypted files and upload to Drop Box")

                choice = input("Choose an option (1, 2, 3, 4, 5, 6, or 7): ")

                if choice == "1":
                    if os.path.exists(get_enc_ssh_config_path()):
                        attempts = 0
                        while attempts < 3:  # Limit the number of attempts
                            self.key = derive_key(getpass.getpass("Enter encryption password: "))
                            if self.select_saved_session():
                                self.interactive_ssh(save_choice="No")
                                break  # Exit the loop after successful connection
                            else:
                                attempts += 1
                                print(f"Incorrect password. Attempt {attempts}/3")
                                if attempts == 3:
                                    print("Too many failed attempts. Exiting...")
                                    break  # Exit the inner loop after 3 failed attempts
                        break # exit outer loop
                    else:
                        print("No Config file found")
                elif choice == "2":
                    # Download multiple files
                    file_names_to_download = [self.ENC_CONFIG_FILE, self.SALT_FILE]

                    download_files_from_google_drive(file_names_to_download)
                    if os.path.exists(get_enc_ssh_config_path()):
                        attempts = 0
                        while attempts < 3:  # Limit the number of attempts
                            self.key = derive_key(getpass.getpass("Enter encryption password: "))
                            if self.select_saved_session():
                                self.interactive_ssh(save_choice="No")
                                break  # Exit the loop after successful connection
                            else:
                                attempts += 1
                                print(f"Incorrect password. Attempt {attempts}/3")
                                if attempts == 3:
                                    print("Too many failed attempts. Exiting...")
                                    break  # Exit the inner loop after 3 failed attempts
                        break # exit outer loop
                    else:
                        print("No Config file Downloaded from Google Drive")
                elif choice == "3":
                    # Download multiple files
                    file_names_to_download = [self.ENC_CONFIG_FILE, self.SALT_FILE]

                    download_files_from_dropbox(file_names_to_download)
                    if os.path.exists(get_enc_ssh_config_path()):
                        attempts = 0
                        while attempts < 3:  # Limit the number of attempts
                            self.key = derive_key(getpass.getpass("Enter encryption password: "))
                            if self.select_saved_session():
                                self.interactive_ssh(save_choice="No")
                                break  # Exit the loop after successful connection
                            else:
                                attempts += 1
                                print(f"Incorrect password. Attempt {attempts}/3")
                                if attempts == 3:
                                    print("Too many failed attempts. Exiting...")
                                    break  # Exit the inner loop after 3 failed attempts
                        break # exit outer loop
                    else:
                        print("No Config file Downloaded from Drop Box")
                elif choice == "4":
                    while True:
                        self.host = get_non_empty_input("Enter the SSH server address (IP only): ")
                        if is_valid_ip(self.host):
                            break
                        else:
                            print("Invalid IP address. Please enter a valid IP address (e.g., 192.168.1.1).")

                    self.port = int(input("Enter the SSH port (default 22): ") or 22)
                    self.username = get_non_empty_input("Enter your username (default 'root'): ", default="root")

                    while self.password_attempts < 3:
                        # Use getpass to securely input the password
                        self.password = getpass.getpass("Enter your password: ")

                        # Perform SSH connection after validating the password
                        res_ssh = self.interactive_ssh(save_choice="No")
                        if res_ssh != "WRONG":
                            break  # Exit the loop after successful connection
                        
                    break  # Exit the loop after successful connection
                elif choice == "5":
                    save_choice = input("Credentials will be saved in an encrypted file (default: yes) (yes/no): ").lower() or "yes"
                    while True:
                        self.host = get_non_empty_input("Enter the SSH server address (IP only): ")
                        if is_valid_ip(self.host):
                            break
                        else:
                            print("Invalid IP address. Please enter a valid IP address (e.g., 192.168.1.1).")

                    self.nickname = get_non_empty_input("Enter a name for this server (e.g., 'Work Server', 'Home Server'): ")
                    self.port = int(input("Enter the SSH port (default 22): ") or 22)
                    self.username = get_non_empty_input("Enter your username (default 'root'): ", default="root")

                    while self.password_attempts < 3:
                        # Use getpass to securely input the password
                        self.password = getpass.getpass("Enter your password: ")

                        # Perform SSH connection after validating the password
                        res_ssh = self.interactive_ssh(save_choice)
                        if res_ssh != "WRONG":
                            break  # Exit the loop after successful connection

                    break  # Exit the loop after successful connection
                elif choice == "6":
                    self.GDrive_upload = True
                    if not os.path.exists(get_enc_ssh_config_path()):
                        print("Try Fetching files from Drive to avoid losing already stored credentials.")
                        file_names_to_download = [self.ENC_CONFIG_FILE, self.SALT_FILE]
                        download_files_from_google_drive(file_names_to_download)
                    save_choice = input("Credentials will be saved in an encrypted file uploaded to Google Drive (default: yes) (yes/no): ").lower() or "yes"
                    while True:
                        self.host = get_non_empty_input("Enter the SSH server address (IP only): ")
                        if is_valid_ip(self.host):
                            break
                        else:
                            print("Invalid IP address. Please enter a valid IP address (e.g., 192.168.1.1).")

                    self.nickname = get_non_empty_input("Enter a name for this server (e.g., 'Work Server', 'Home Server'): ")
                    self.port = int(input("Enter the SSH port (default 22): ") or 22)
                    self.username = get_non_empty_input("Enter your username (default 'root'): ", default="root")

                    while self.password_attempts < 3:
                        # Use getpass to securely input the password
                        self.password = getpass.getpass("Enter your password: ")

                        # Perform SSH connection after validating the password
                        res_ssh = self.interactive_ssh(save_choice)
                        if res_ssh != "WRONG":
                            break  # Exit the loop after successful connection

                    break  # Exit the loop after successful connection
                elif choice == "7":
                    self.DBox_upload = True
                    if not os.path.exists(get_enc_ssh_config_path()):
                        print("Try Fetching files from Drop Box to avoid losing already stored credentials.")
                        file_names_to_download = [self.ENC_CONFIG_FILE, self.SALT_FILE]
                        download_files_from_dropbox(file_names_to_download)
                    save_choice = input("Credentials will be saved in an encrypted file uploaded to Drop Box (default: yes) (yes/no): ").lower() or "yes"
                    while True:
                        self.host = get_non_empty_input("Enter the SSH server address (IP only): ")
                        if is_valid_ip(self.host):
                            break
                        else:
                            print("Invalid IP address. Please enter a valid IP address (e.g., 192.168.1.1).")

                    self.nickname = get_non_empty_input("Enter a name for this server (e.g., 'Work Server', 'Home Server'): ")
                    self.port = int(input("Enter the SSH port (default 22): ") or 22)
                    self.username = get_non_empty_input("Enter your username (default 'root'): ", default="root")

                    while self.password_attempts < 3:
                        # Use getpass to securely input the password
                        self.password = getpass.getpass("Enter your password: ")

                        # Perform SSH connection after validating the password
                        res_ssh = self.interactive_ssh(save_choice)
                        if res_ssh != "WRONG":
                            break  # Exit the loop after successful connection

                    break  # Exit the loop after successful connection
                else:
                    print("Invalid option selected.")
        except KeyboardInterrupt as ke:
            print(f"\nKey board interrupt found")
            print("Closing Application")

if __name__ == "__main__":
    client_manager = SSHClientManager()
    client_manager.run()