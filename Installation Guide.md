# **SSH Client Manager - Installation Guide**

## **1. Download and Setup**

### **Clone the GitHub Repository**

```bash
git clone https://github.com/cyperdev/SSHClientManager.git
cd SSHClientManager
```

### **Create and Activate a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## **2. Dropbox Integration Setup**

1. **Create a Dropbox Account** (if you don’t have one) at [Dropbox](https://www.dropbox.com/).
2. **Create an App**:
    - Go to [Dropbox App Console](https://www.dropbox.com/developers/apps).
    - Click **"Create App"**.
		![Screenshot](Images/dropbox1.png)
    - Choose **Scoped Access**.
    - Select **App Folder** – access is limited to a single folder created for your app.
    - Name the app: `ssh_client_manager`.
	    ![Screenshot](Images/dropbox2.png)
3. **Set Permissions**:
    - Navigate to **Permissions** under **Files and Folders**.
    - Enable:
        - `files.content.write`
        - `files.content.read`
        ![Screenshot](Images/dropbox3.png)
4. **Get AUTH CODE and Oauth Refresh Token**:
    - Go back to **Settings**.
      ![Screenshot](Images/dropbox4.png)
    - Replace the APPKEY and Visit- https://www.dropbox.com/oauth2/authorize?client_id=APPKEYHERE&response_type=code&token_access_type=offline
    - Click Continue
      ![Screenshot](Images/dropbox5.png)
    - Click Allow
      ![Screenshot](Images/dropbox6.png)
    - Copy the Auth Code
      ![Screenshot](Images/dropbox7.png)
        ```
        curl https://api.dropbox.com/oauth2/token \
	    -d code=AUTH_CODE \
	    -d grant_type=authorization_code \
	    -u APPKEYHERE:APPSECRETHERE​
       ```
    - Copy Refresh token ```refresh_token```
      ![Screenshot](Images/dropbox8.png)
    - Save the app_key, app_secret and refresh_token in `drop_box_config.json` under the `.ssh_client_manager` folder in your home directory.
    - _(If `.ssh_client_manager` is not found, simply run the application and exit; the folder will be created automatically.)_

---

## **3. Google Drive Integration Setup**

1. **Go to Google Cloud Console** at [Google Cloud Console](https://console.cloud.google.com/).
2. **Create a New Project**:
    - Click **Select a project ➝ New Project ➝ Create**.
	    ![Screenshot](Images/google1.png)
    - Name it **DriveAPI**.
      
	    ![Screenshot](Images/google2.png)
3. **Enable Google Drive API**:
    - Under **APIs & Services**, select **Enable APIs and Services**.
	    ![Screenshot](Images/google3.png)
    - Click **ENABLE APIS AND SERVICES**
	    ![Screenshot](Images/google4.png)
    - Under **Google Workspace**, search for **Google Drive API** and click **Enable**.
	    ![Screenshot](Images/google5.png)
	    ![Screenshot](Images/google6.png)
4. **Set Up OAuth Consent Screen and Create OAuth Credentials**:
    - Navigate to **OAuth consent screen**.
	    ![Screenshot](Images/google7.png)
    - Click **Get Started**.
	    ![Screenshot](Images/google8.png)
    - Provide **App Name**, select your email for **User Support Email**, and click **Next**.
	    ![Screenshot](Images/google9.png)
    - Under **Audience**, select **External** and click **Next**.
	    ![Screenshot](Images/google10.png)
    - Under **Contact Information**, enter your email address and click **Next**.
	    ![Screenshot](Images/google11.png)
    - Under **Finish**, tick the **Terms of Service** checkbox and click **Continue**.
	    ![Screenshot](Images/google12.png)
    - Click **Create** → Click **Create OAuth Client**.
		![Screenshot](Images/google13 1.png)
	    ![Screenshot](Images/google14.png)
    - Under **Application Type**, select **Desktop App**.
	    - Provide a name: `ssh_client_manager` and click **Create**.
		![Screenshot](Images/google15.png)
    - Under **Publishing Status**, click **Publish App**.
	    ![Screenshot](Images/google18.png)
5. **Download and Save Credentials**:
    - Download the `client_secret_SOME_RANDOM_CHAR.json` file.
    - Rename it to `credentials.json` and move it to the `.ssh_client_manager` folder in your home directory.
	    ![Screenshot](Images/google16 1.png)
	    ![Screenshot](Images/google17.png)
    - _(If `.ssh_client_manager` is not found, simply run the application and exit; the folder will be created automatically.)_
6. **Authenticate and Generate Token**:
    - Run the application; it will open a browser for authentication.
    - Alternatively, copy the URL shown in the terminal and visit it manually to authenticate.
	    ![Screenshot](Images/google19.png)
    - Once authentication is completed, the `token.json` file will be automatically downloaded into the `.ssh_client_manager` folder.

---
## Run the script
```bash
python SSHClientManager.py
```
