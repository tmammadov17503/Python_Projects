#!/usr/bin/env python3
# This line is needed to ensure that the code will be able to be run with Python 3

# Taghi Mammadov Lab 2 login part

import getpass
import sys # For read command-line arguments
import bcrypt # Used for hashing passwords. It mainly provides a secure way to store and verify passwords
import json # For reading from and writing to the password storage file

user_database = 'user_db.json'  # Ensure this matches the filename used in lab_2_usermgmt_CS.py


def load_user_db(): # So this is the function for loading the data from the file
    try:
        with open(user_database, 'r') as f: # Reads the file
            return json.load(f) # File is read in the file format
    except FileNotFoundError:
        return {}


def login_user(username, password): # the main part of the code
    user_db = load_user_db() # Load the dictionary again here
    if username not in user_db:
        print('Username or password incorrect.')
        return # if username not in the file it will not be able to access it

    user_info = user_db[username]
    hashed_password = user_info['password'].encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        if user_info.get('forcepass'): # if there is a forecepass from the usermgmt file then the password has to be changes because the flag is in True
            print('Password must be changed.')
            new_password = getpass.getpass('New password: ')
            repeat_password = getpass.getpass('Repeat new password: ')
            if new_password != repeat_password:
                print('Password mismatch. Login failed.')
                return
            # Updates the database with the new password and remove the forcepass flag ad puts it again to 0 or False
            hashed_new = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user_db[username] = {'password': hashed_new.decode('utf-8'), 'forcepass': False}
            with open(user_database, 'w') as f:
                json.dump(user_db, f, indent=4)
            print('Password changed successfully. Welcome!') # opens the dictionary file and writes there
        else:
            print(f'Welcome {username}!') # if there is no need for change it will just welcome the user
        # Simulate launching a command
        print('bash$')
    else:
        print('Username or password incorrect.')


def main():
    if len(sys.argv) != 2:
        print('Please, insert arguments to continue.') # is not enough arguments then the message
        return
    username = sys.argv[1]
    password = getpass.getpass('Password: ')
    login_user(username, password)


if __name__ == '__main__':
    main()
