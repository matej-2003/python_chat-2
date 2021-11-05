from json.decoder import JSONDecodeError
import socket
import sys
from threading import Thread
import time
import json
from protocol.messages import *

messages = []

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002

if len(sys.argv) == 3:
    SERVER_HOST = str(sys.argv[1])
    SERVER_PORT = int(sys.argv[2])
elif len(sys.argv) == 2:
    SERVER_HOST = str(sys.argv[1])
else:
    print("""
    Correct ussage:
        'script IP PORT'
        'script IP'
        default port is 5002
    """)

prompt = "> "

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

time.sleep(0.5)
print("sending connect request")
s.send(client.connect("matej", "kodermac"))

message = s.recv(1024).decode()
message = client.parse(message)
print(message)
if message != client.PARSE_ERROR:
    if message["response"] == UNAUTHORIZED:
        print("closing connection ...")
        time.sleep(0.5)
        s.close()
        exit()
else:
    print("closing connection ...")
    time.sleep(0.5)
    s.close()
    exit()

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        try:
            print('\r[server] -> {}\n\n{}'.format(json.loads(message), prompt), end='')
            
        except JSONDecodeError:
            pass

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()


time.sleep(0.5)
print("sending messages request")
s.send(client.get_messages())

time.sleep(0.5)
print("sending user data request")
s.send(client.get_users())

time.sleep(0.5)
print("sending message")
s.send(client.send("test..."))

while True:
    msg = input(prompt)
    if msg.lower() == 'q':
        break
    else:
        s.send(client.send(msg))

time.sleep(0.5)
print("sending disconnect request")
s.send(client.disconnect())

time.sleep(0.1)
s.close()