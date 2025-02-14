#!/usr/bin/env python3

from Crypto.Cipher import AES  # Import AES for encryption
from Crypto.Protocol.KDF import PBKDF2  # Import PBKDF2 for key derivation
from Crypto.Random import get_random_bytes  # For random bytes
import json  # JSON Module
import os  # For files management inside the code
import argparse  # Argparse module for command-line argument parsing

class PasswordManager:
    def __init__(self):
        self.master_passphrase = None  # Initialize master passphrase to None
        self.key = None  # Initialize encryption key to None
        self.salt = None  # Initialize salt value to None
        self.passwords = {}  # Passwords dictionary created for storing data
        self.passwords_file = 'passwords.enc'  # Set default filename for encrypted passwords storage

    def set_master_passphrase(self, master_passphrase, new_init=False): # Set master passphrase and derive encryption key
        self.master_passphrase = master_passphrase.encode()  # Encode passphrase to bytes
        if new_init or not os.path.exists(self.passwords_file):  # Check initializing
            self.salt = get_random_bytes(AES.block_size)  # Generate random salt
        else:
            with open(self.passwords_file, 'rb') as file:
                self.salt = file.read(AES.block_size)  # Read salt from existing file
        self.key = PBKDF2(self.master_passphrase, self.salt, dkLen=32)  # Derive key using PBKDF2

    def save_passwords(self): #Encrypt and save passwords to file
        cipher = AES.new(self.key, AES.MODE_GCM)  # Create AES cipher object
        nonce = cipher.nonce  # Get nonce
        ciphertext, tag = cipher.encrypt_and_digest(json.dumps(self.passwords).encode())  # Encrypt passwords
        with open(self.passwords_file, 'wb') as file:  # Open file for writing because 'wb'
            for item in (self.salt, nonce, tag, ciphertext):  # Writing salt, nonce, tag, and ciphertext to file
                file.write(item)

    def load_passwords(self): #Load and decrypt passwords from file
        if not os.path.exists(self.passwords_file):  # Check if file doesn't exist
            return None
        with open(self.passwords_file, 'rb') as file:  # Open file for reading because 'rb'
            salt, nonce, tag = [file.read(x) for x in (AES.block_size, AES.block_size, 16)]  # Read salt, nonce, tag
            ciphertext = file.read()  # Read ciphertext
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)  # Create AES cipher object with the usage of nonce
            try:
                decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)  # Decrypt ciphertext
                self.passwords = json.loads(decrypted_data)  # Load decrypted data to get passwords
                return True  # Return True if successful
            except (ValueError, KeyError):
                print("Master passphrase incorrect or integrity check failed.")
                return False  # Return False if decryption fails

    def add_password(self, address, password): #Putting password to the store
        if self.load_passwords() is None:  # Check if passwords are loaded
            print("Initializing new password store.")
        self.passwords[address] = password  # Add password to passwords dictionary
        self.save_passwords()  # Save passwords to file
        print(f"Stored password for {address}.")

    def get_password(self, address): # Retrieve a password from the store
        if self.load_passwords() is True:  # Ensure passwords were successfully loaded
            password = self.passwords.get(address)  # Get password related to the address
            if password:
                print(f"Password for {address} is: {password}.")  # Print password if found
            else:
                print(f"Could not load passwords. Check your master passphrase.")  # Print error if password was not found

def parse_arguments(): #Parse command-line arguments
    parser = argparse.ArgumentParser(description='Password Manager')  # Create ArgumentParser object
    subparsers = parser.add_subparsers(dest='command')  # Create subparsers for different commands

    init_parser = subparsers.add_parser('init', help='Initialize the password store with a master passphrase')
    init_parser.add_argument('master_passphrase', type=str, help='Master passphrase for the password store')

    put_parser = subparsers.add_parser('put', help='Store a password')
    put_parser.add_argument('master_passphrase', type=str, help='Master passphrase for the password store')
    put_parser.add_argument('address', type=str, help='Address (e.g., website) for the password')
    put_parser.add_argument('password', type=str, help='Password to store')

    get_parser = subparsers.add_parser('get', help='Retrieve a password')
    get_parser.add_argument('master_passphrase', type=str, help='Master passphrase for the password store')
    get_parser.add_argument('address', type=str, help='Address (e.g., website) for retrieving the password')

    return parser.parse_args()  # Parse arguments and return

def main():
    args = parse_arguments()  # Parse command-line arguments
    password_manager = PasswordManager()  # Create PasswordManager object

    if args.command == 'init':
        password_manager.set_master_passphrase(args.master_passphrase, new_init=True)
        password_manager.save_passwords()
        print("Password manager initialized.")
    elif args.command == 'put':
        password_manager.set_master_passphrase(args.master_passphrase)
        password_manager.add_password(args.address, args.password)
    elif args.command == 'get':
        password_manager.set_master_passphrase(args.master_passphrase)
        password_manager.get_password(args.address)

if __name__ == "__main__":
    main()  # Call main function
