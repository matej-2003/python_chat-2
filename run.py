# import protocol
from protocol import auth
import csv

# protocol.USERS_FILE = "users.csv"
# protocol.GROUPS_FILE = "groups.csv"
# protocol.update_users()

USERS_FILE = "users.csv"
users = []

def update_users():
    global users
    if not not USERS_FILE:
        with open(USERS_FILE, 'r') as file:
            users = list(csv.DictReader(file))

if __name__ == '__main__':
    update_users()
    print(auth('matej', 'kodermac', users=users))