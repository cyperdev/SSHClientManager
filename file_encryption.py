import os
import secrets
from misc import *
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def load_or_generate_salt():
    """Loads an existing salt or generates a new one if not found."""
    if os.path.exists(get_salt_bin_path()):
        with open(get_salt_bin_path(), "rb") as file:
            return file.read()
    else:
        salt = secrets.token_bytes(32)  # Generate a secure random 32-byte salt
        with open(get_salt_bin_path(), "wb") as file:
            file.write(salt)
        return salt

def derive_key(password: str):
    """Derives a 256-bit key using Argon2."""
    # Initialize the Argon2id key derivation function
    kdf = Argon2id(
        iterations=2,  # Number of iterations (time cost)
        memory_cost=2**16,  # Memory cost in KB
        lanes=2,  # Number of parallel lanes (parallelism)
        length=32,  # Length of the derived key (in bytes)
        salt=load_or_generate_salt()  # The salt value
    )
    return kdf.derive(password.encode())

def encrypt_data(data: bytes, key):
    """Encrypts data using AES-256-GCM."""
    iv = secrets.token_bytes(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data) + encryptor.finalize()
    return base64.b64encode(iv + encryptor.tag + encrypted).decode()

def decrypt_data(data: str, key):
    """Decrypts AES-256-GCM encrypted data."""
    raw_data = base64.b64decode(data)
    iv, tag, encrypted = raw_data[:12], raw_data[12:28], raw_data[28:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted) + decryptor.finalize()