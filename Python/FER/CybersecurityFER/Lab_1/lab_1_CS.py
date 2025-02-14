#!/usr/bin/env python3
# This line is needed to ensure that the code will be able to be run with Python 3

# Taghi Mammadov - LAB 1 Code
# This is the code for Password Manager which was needed. I have used AES-GCM mode for encryption and HMAC, SHA256 for additional verification.

# First I imported necessary libraries like HMAC, SHA256, AES, PBKDF2, json, os, sys, and get_random_bytes which I have read in a provided instructions for the assignment
from Crypto.Hash import HMAC, SHA256
# HMAC (Hash-based Message Authentication Code) - used for generating and verifying tags for message authenticity and integrity
# SHA256 is a cryptographic hash function used here as the underlying hash function for HMAC.
# Where I have found it -> https://pycryptodome.readthedocs.io/en/latest/src/hash/hmac.html#:~:text=%3E%3E%3E-,from%20Crypto.Hash%20import%20HMAC%2C%20SHA256,-%3E%3E%3E%0A%3E%3E%3E%20secret
from Crypto.Cipher import AES
# I have used Crypto.Cipher package because it contains algorithms for protecting the confidentiality of the data
# AES (Advanced Encryption Standard) - a symmetric encryption algorithm used to encrypt and decrypt data, with the ensurance of its confidentiality
# AES is used in GCM mode, which provides data authenticity / So mainly here is the mix of confidentiality and authencity
# Where I have found it -> https://pycryptodome.readthedocs.io/en/latest/src/cipher/cipher.html#:~:text=from%20Crypto.Cipher%20import
from Crypto.Protocol.KDF import PBKDF2
# PBKDF2 (Password-Based Key Derivation Function 2) - used to derive a secure cryptographic key from a passphrase
# Hashes algorithm multiple times, making it resistant to brute-force attacks
# Where I have found it -> https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html#:~:text=from%20Crypto.Protocol.KDF%20import%20PBKDF2
from Crypto.Random import get_random_bytes
# used to generate cryptographically secure random bytes.Here it is uded for generating salts for key derivation, nonces for AES encryption, and keys for HMAC.
# Where I have found it -> https://pycryptodome.readthedocs.io/en/latest/src/random/random.html#:~:text=Crypto.Random.get_random_bytes(N
import json # For reading from and writing to the password storage file
import os # For file paths
import sys # For read command-line arguments

def derive_key(passphrase: str, salt: bytes, output_bytes=64) -> bytes:
# This is the derive key function with 3 arguments which are passphrase(form where to derive the encryption key), salt(so that identical passwords do not generate the same key), and output_bytes(length of the key) which is by default set to 64
# The result of this function provides us with the derived cryptographic key
# PBKDF2 is used here for key derivation. It's a secure way to turn passwords into keys.
    return PBKDF2(passphrase, salt, dkLen=output_bytes, count=100000) # Key derivation function - for deriving the key from master pass
# The `dkLen` parameter is the length of the derived key and The `count` parameter specifies the number of iterations of the pseudorandom function. This is used to increase the difficulty of brute-force attacks so that attacker will find it difficult to encrypt the message

def hmac_tag(data: bytes, key: bytes) -> str: # Used to generate an HMAC tag for given data. Uses data and the secret key that are in bytes
    # The result of this function is a hexadecimal string representation of the HMAC tag
    h = HMAC.new(key, digestmod=SHA256) # digestmod=SHA256 because from Crypto.Hash import HMAC, SHA256
    # Where I have found it -> https://pycryptodome.readthedocs.io/en/latest/src/hash/hmac.html#:~:text=secret%20%3D%20b%27Swordfish%27%0A%3E%3E%3E-,h%20%3D%20HMAC.new(secret%2C%20digestmod%3DSHA256),-%3E%3E%3E%20h.update(b
    h.update(data)
    return h.hexdigest()
    # Where I have found it -> https://pycryptodome.readthedocs.io/en/latest/src/hash/hmac.html#:~:text=h.update(b%27Hello%27)%0A%3E%3E%3E%20print(h.hexdigest())

def verify_hmac(data: bytes, key: bytes, hex_tag: str) -> bool: # This function verifies if the given HMAC tag matches the one generated for the input data with the specified key.
    h = HMAC.new(key, digestmod=SHA256) # The same as in the hmac_tag function
    h.update(data)
    try:
        h.hexverify(hex_tag) # hex_tag has to be identical with the hmac tag
        return True
    except ValueError:
        return False
    # Where I have found it -> https://pycryptodome.readthedocs.io/en/latest/src/hash/hmac.html#:~:text=h%20%3D%20HMAC.new(secret%2C%20digestmod%3DSHA256)%0A%3E%3E%3E%20h.update(msg)%0A%3E%3E%3E%20try%3A%0A%3E%3E%3E%20%20%20h.hexverify(mac)%0A%3E%3E%3E%20%20%20print(%22The%20message%20%27%25s%27%20is%20authentic%22%20%25%20msg)%0A%3E%3E%3E%20except%20ValueError%3A%0A%3E%3E%3E%20%20%20print(%22The%20message%20or%20the%20key%20is%20wrong%22)

def encrypt_data_hmac(data: str, passphrase: str) -> dict: # Function to encrypt data and generate HMAC tag
    salt = get_random_bytes(32) # 32-byte salt for key derivation, in default it is 12, but on demonstartion I was told that it is better to use 32. Create a new, random salt for this encryption
    # Found from -> https://pycryptodome.readthedocs.io/en/latest/src/random/random.html#:~:text=Crypto.Random.get_random_bytes(N,%C2%B6
    derived_key = derive_key(passphrase, salt) # Derive a 64-byte key from the passphrase and salt using PBKDF2
    encryption_key, hmac_key = derived_key[:32], derived_key[32:64] # For encryption and HMAC
    cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=get_random_bytes(16)) # Create a new cipher 16-byte nonce for AES GCM. Nonce - ensures that each cryptographic operations is unique and so that it does not repeat, because if it will, then the attack might happen
    # cipher from -> https://pycryptodome.readthedocs.io/en/latest/src/cipher/cipher.html#:~:text=cipher%20%3D%20Salsa20.new(key)
    ct_bytes, tag = cipher.encrypt_and_digest(data.encode())  # Encrypt and generate a 16-byte tag.
    hmac_hex_tag = hmac_tag(ct_bytes + cipher.nonce + tag, hmac_key)  # Generate HMAC tag, mix nonce and GCM tag in the HMAC, which gives HMAC verification process, and enchances security of the code
    # Return the encrypted data and associated items as a dictionary
    return {
        'ciphertext': ct_bytes.hex(), 'salt': salt.hex(),
        'nonce': cipher.nonce.hex(), 'tag': tag.hex(),
        'hmac_key': hmac_key.hex(), 'hmac_tag': hmac_hex_tag
    }

def decrypt_data_hmac(encrypted_data: dict, passphrase: str) -> str or None: # Function to decrypt data with the verification of its HMAC tag. Uses dictionary and master passphrase
    salt = bytes.fromhex(encrypted_data['salt'])
    derived_key = derive_key(passphrase, salt)
    encryption_key, hmac_key = derived_key[:32], derived_key[32:64]
    nonce = bytes.fromhex(encrypted_data['nonce'])
    ciphertext = bytes.fromhex(encrypted_data['ciphertext'])
    tag = bytes.fromhex(encrypted_data['tag'])
    hmac_hex_tag = encrypted_data['hmac_tag']
    if not verify_hmac(ciphertext + nonce + tag, hmac_key, hmac_hex_tag):  # We have to verify HMAC tag before proceeding with decryption, because if there will be problems with HMAC tga, it will give an attacker an opportunity.
        # Found from - https://pycryptodome.readthedocs.io/en/latest/src/hash/hmac.html#:~:text=chunk%20of%20data-,verify(mac_tag,-)
        return None  # Implicitly handles HMAC verification failure., # Return None if decryption fails
    cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=nonce) # Create a new cipher object
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag) # Decrypt and verify integrity of the data
        return plaintext.decode() # Return the decrypted data as a string
    except Exception:
        return None  # Handles decryption or tag verification failure.

def init_store(passphrase: str): #Initialize the password store. ./lab_1_CS.py init mAsterPasswrd. We use master passphrase used to derive encryption keys.
    store = {'passwords': {}} # Create an empty store in the way of dictionary to store data
    encrypted_store = encrypt_data_hmac(json.dumps(store), passphrase) # Encrypt the store
    with open("password_store.json", "w") as file: # Create a file named "password_store.json" in write mode and writes there
        json.dump(encrypted_store, file) # The JSON object that contains ciphertext, nonce, HMAC tag, and other necessary elements
    print("Password manager initialized.")

def store_password(address: str, password: str, passphrase: str): # Store a new password
    try: # Open the encrypted store and add a new password
        with open("password_store.json", "r") as file: # "r" for read of the file
            encrypted_store = json.load(file) # load it to the dictionaru of the password store
        decrypted_store = json.loads(decrypt_data_hmac(encrypted_store, passphrase))
        if decrypted_store is None:
            print("Master passphrase incorrect or integrity check failed.")
            return
        decrypted_store['passwords'][address] = encrypt_data_hmac(password, passphrase)
        with open("password_store.json", "w") as file:
            json.dump(encrypt_data_hmac(json.dumps(decrypted_store), passphrase), file)
        print(f"Stored password for {address}.")
    except Exception as e:
        print(f"Error storing password: {e}")

def get_password(address: str, passphrase: str): # Retrieve a stored password from store_password function
    try: # Open the encrypted store and retrieve a password
        with open("password_store.json", "r") as file:
            encrypted_store = json.load(file)
        decrypted_store_json = decrypt_data_hmac(encrypted_store, passphrase)
        if decrypted_store_json is None:
            print("Master passphrase incorrect or integrity check failed.")
            return
        decrypted_store = json.loads(decrypted_store_json)
        if address in decrypted_store['passwords']:
            encrypted_password = decrypted_store['passwords'][address]
            password = decrypt_data_hmac(encrypted_password, passphrase) # if encrypted password and the password are identical it will be correct
            if password:
                print(f"Password for {address} is: {password}.")
            else:
                print("Master passphrase incorrect or integrity check failed.")
        else:
            print("Master passphrase incorrect or integrity check failed.") # In the case when no password stored for the address. First I wanted to write like this, then understood that this is a lack of info for an attacker
    except Exception:
        print(f"Master passphrase incorrect or integrity check failed.")

if __name__ == "__main__": # Main function to process all 3 commands. My mistake when I first wrote the code was that I forgot to add the main function that will use all 3 commands
    if len(sys.argv) < 2: # For checking if at least one command-line argument is provided and if not it will give instrcution line
        print("Init, put, or get command is needed to proceed.")
    elif sys.argv[1] == "init" and len(sys.argv) == 3:
        init_store(sys.argv[2])
    elif sys.argv[1] == "put" and len(sys.argv) == 5:
        store_password(sys.argv[3], sys.argv[4], sys.argv[2])
    elif sys.argv[1] == "get" and len(sys.argv) == 4:
        get_password(sys.argv[3], sys.argv[2])
    else: # If nothing is met with the conditions it will just say Invalid
        print("Invalid command or number of arguments are not correct.")
