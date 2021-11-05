import socket
import sys
import threading
from protocol.messages import *

SERVER_HOST = "0.0.0.0"     # server's IP address
SERVER_PORT = 5002

if len(sys.argv) == 3:
    SERVER_HOST = str(sys.argv[1])
    SERVER_PORT = int(sys.argv[2])
elif len(sys.argv) == 2:
    SERVER_PORT = int(sys.argv[1])
else:
    print("""
    Correct ussage:
        'script IP PORT'
        'script IP'
        default port is 5002
    """)

client_sockets = set()
EXIT_MSG = "connection closed..."
ERROR = "error {}"
PROMPT = "server{}: "

user_names = ["liam", "noah", "oliver", "william", "elijah", "james", "benjamin", "lucas", "john"]
users = []
users = [{
    "username": name,
    "password": "passwd",
    "status": 0,
} for name in user_names]
users.append({
    "username": "matej",
    "password": "kodermac",
    "status": 0,
})

def parse_users():
    return [(i["username"], i["status"]) for i in users]

messages = [client.new_message("matej", "lorem ipsum....") for _ in range(2)]

def auth(username, password):
    for i in users:
        if username == i["username"] and password == i["password"] and i["status"] == 0:
            i["status"] = 1
            return True

def connect(msg):
    if "data" in msg:
        if ("username" in msg["data"]) and ("password" in msg["data"]):
            return auth(msg["data"]["username"], msg["data"]["password"])
    return False

def get(cs, msg):
    if "data" in msg:
        if ("type" in msg["data"]):
            type = msg["data"]["type"]
            if type == GET_MESSAGES:
                cs.send(server.data(messages))
                return
            elif type == GET_USER_DATA:
                cs.send(server.data(parse_users()))
                return
    cs.send(server.error())

def send(msg, username):
    global client_sockets
    if "data" in msg:
        if ("message" in msg["data"]):
            message_formated = client.new_message(username, msg["data"]["message"])
            messages.append(message_formated)
            for s in client_sockets:
                s.send(server.new_message(message_formated))

def main_loop(cs, username):
    while True:
        try:
            msg = server.parse(cs.recv(1024).decode())
            print(f"[client] -> {msg}")
            if msg != server.PARSE_ERROR:
                method = msg["method"]
                if method == DISCONNECT:
                    break
                elif method == GET:
                    get(cs, msg)
                    continue
                elif method == SEND:
                    send(msg, username)
                    continue
            cs.send(server.error())
        except Exception as e:
            print(f"[!] Error: {e}")
            break
    print(EXIT_MSG)
    for i in users:
        if username == i["username"]:
            i["status"] = 0
            break
    client_sockets.remove(cs)

s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

while True:
    try:
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected. {len(client_sockets)}")
        msg = server.parse(client_socket.recv(1024).decode())
        
        if msg != server.PARSE_ERROR:
            if msg['method'] == CONNECT:
                if connect(msg):
                    client_sockets.add(client_socket)
                    client_socket.send(server.accept())
                    print(f"[client] -> {msg}")
                    t = threading.Thread(target=main_loop, args=(client_socket, msg["data"]["username"]))
                    t.daemon = True
                    t.start()
                    continue    #skip the rest of the code to avoid triping close connection

        client_socket.send(server.deny())
        client_socket.close()

    except KeyboardInterrupt:
        break

print("\n[!]closing all sockets...")

for cs in client_sockets:
    cs.close()
s.close()
