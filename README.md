# **SSH Client Manager**

## **Project Description**

SSH Client Manager is a **secure and efficient** tool designed to **manage, store, and retrieve SSH credentials** with strong encryption. It enables users to securely store SSH connection details locally or in cloud storage services like **Google Drive** and **Dropbox**, ensuring accessibility across multiple devices while maintaining high-security standards.

## **Key Features**

### 🔹 **Secure SSH Credential Management**

- Store SSH login details **locally** or upload them securely to **Google Drive** or **Dropbox**.
- Access saved credentials from encrypted files, ensuring data integrity.

### 🔹 **Advanced Encryption & Security**

- **AES-256-GCM Encryption** – Provides both encryption and authentication, preventing tampering.
- **Uses a 12-byte IV**, which is recommended for AES-GCM to ensure security and prevent nonce reuse attacks.
- **Argon2id Key Derivation** – Protects against brute-force attacks by securely deriving encryption keys from user-provided passwords.
- **Salt Protection** – Each encryption operation is hardened with a **32-byte salt**, stored securely in `Salt.bin`.

### 🔹 **Multiple Storage & Import Options**

- **Local Storage** – Save credentials in an encrypted JSON file (`enc_ssh_config.json`).
- **Google Drive Integration** – Seamlessly upload and retrieve encrypted SSH credentials via the **Google Drive API**.
- **Dropbox Integration** – Securely store and retrieve credentials using the **Dropbox API**.

### 🔹 **Flexible SSH Connection Management**

- **Use Credentials Without Saving** – Directly input SSH details for temporary use.
- **Securely Save New Credentials** – Store encrypted SSH configurations locally or in the cloud.
- **Import Existing Encrypted Credentials** – Retrieve and decrypt stored credentials from **local, Google Drive, or Dropbox storage**.

## **Why Use SSH Client Manager?**

✅ **Secure** – Uses modern encryption techniques to safeguard SSH credentials.  
✅ **Convenient** – Store SSH configurations locally or access them from the cloud.  
✅ **Reliable** – Prevents unauthorized access with built-in authentication and integrity verification.  
✅ **Easy to Use** – Simple command-line interface for seamless SSH credential management.

This project is ideal for **developers, system administrators, and cybersecurity professionals** who need a **secure and centralized** solution to manage multiple SSH connections efficiently.

---
## **What Motivated This Project?**

As a **cybersecurity professional**, I frequently manage multiple SSH connections across different environments, often requiring secure storage and easy retrieval of credentials. Traditional methods of storing SSH credentials—such as plaintext files, password managers, or environment variables—posed significant security risks, which became a growing concern.

During my search for a **free SSH client manager**, I quickly realized that most solutions failed to meet my needs. Many lacked **import functionality**, forcing me to manually re-enter credentials, while others didn't offer **cloud integration**, making remote access difficult. Additionally, several tools either stored credentials in **plaintext or used weak encryption**, leaving sensitive data vulnerable. Even more frustrating, many options were locked behind **paywalls**, limiting access to essential features unless I paid for a premium version.

This gap motivated me to **create my own solution**—an **SSH Client Manager** that addresses these issues and provides:  
✅ **Secure storage** by encrypting SSH credentials with **AES-256-GCM**, ensuring data confidentiality.  
✅ **Cloud accessibility** via **Google Drive** and **Dropbox**, while maintaining **end-to-end encryption**.  
✅ **Import functionality** for encrypted SSH credentials, eliminating the need for manual entry.  
✅ **Protection against brute-force attacks** using **Argon2id key derivation** with a **32-byte salt**.  
✅ **An open-source, completely free solution**, offering reliable and secure management for developers, system administrators, and security professionals.

By creating this tool, I sought to bridge the gap between **security** and **convenience**, ensuring that SSH credential management is **safe**, **efficient**, and **flexible**—without the limitations of paid alternatives.

---
## **Licensing Flexibility**
While this project is licensed under the GNU Affero General Public License (AGPL) v3.0, I am open to discussions for commercial licensing or special use cases. If you are interested in using this software in a commercial environment or need to modify it for proprietary use, please contact me directly to explore available options. This flexibility ensures that both individual users and organizations can benefit from the tool while maintaining the integrity and open-source nature of the project.

---
## **Disclaimer**
This software is provided "as-is," without any warranty of any kind, either express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, or non-infringement. In no event shall the author or contributors be held liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.

By using this software, you agree to take full responsibility for any consequences that may arise from its use, including any potential security, performance, or operational issues. Please use this tool in compliance with all relevant laws and regulations in your jurisdiction.

---
## Contact Information

For any inquiries related to commercial licensing, special use cases, or general questions, please feel free to contact me at:

- LinkedIn: [https://www.linkedin.com/in/mohamedazarudheen/]
  
I am open to discussions and look forward to collaborating with you!
