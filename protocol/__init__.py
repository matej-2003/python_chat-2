import csv
import json
import hashlib
import hmac
import os

PASSWD_SALT_LEN = 32
PSWD_ITERATIONS = 10

def hash_password(password, salt=None):
    global PASSWD_SALT_LEN, PSWD_ITERATIONS
    password = password.encode()
    if salt == None:
        salt = os.urandom(PASSWD_SALT_LEN)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", 
        password, 
        salt, 
        PSWD_ITERATIONS
    )

    return salt + password_hash

def check_password(password, password_hash):
    global PASSWD_SALT_LEN
    password_hash = bytes().fromhex(password_hash)
    salt = password_hash[:PASSWD_SALT_LEN]
    return (hmac.compare_digest(password_hash, hash_password(password, salt=salt)))

def auth(username, password, users):
    for i in users:
        if username == i["username"] and check_password(password, i["password"]) and i["status"] == 0:
            return True
    return False


USERS_FILE = None   # "users.csv"
GROUPS_FILE = None   # "groups.csv"
user_fieldnames = ['username','password']
users = []

def update_users():
    global users
    if not not USERS_FILE:
        with open(USERS_FILE, 'r') as file:
            users = list(csv.reader(file))

def new_user(username, password):
    return {'username': username, 'password': hash_password(password).hex()}

def create_user(filename, username, password):
    if not not filename:
        # with open(filename, 'r') as file:
        #     users = list(csv.reader(file))
        #     for i in users:
        #         if username == i["username"]:
        #             print(f"username taken")
        #             return
        with open(filename, 'a', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow([username, hash_password(password).hex()])
    else:
        print(f"USERS_FILE not defined")

def create_group(name, admin_users, members, status):
    if not not GROUPS_FILE:
        with open(GROUPS_FILE, 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow([name, json.dumps(admin_users), json.dumps(members), status])