import socket
import threading
from protocol.messages import *
from protocol import check_password
import csv

EXIT_MSG = "connection closed..."
ERROR = "error {}"

def parse_users(users):
    return [(i["username"], i["status"]) for i in users]

class ChatServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.s = None
        self.client_sockets = set()
        self.users = []
        self.messages = [client.new_message("matej", "lorem ipsum....") for _ in range(2)]
    
    def load_user_file(self, filename):
        with open(filename, 'r') as file:
            users = list(csv.reader(file))
            for i in users:
                self.users.append({
                    "username": i[0],
                    "password": i[1],
                    "status": 0,
                })

    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        print("Listening at", self.s.getsockname())

        while True:
            try:
                client_socket, client_address = self.s.accept()
                print(f"[+] {client_address} connected. {len(self.client_sockets)}")
                msg = server.parse(client_socket.recv(1024).decode())
                
                if msg != server.PARSE_ERROR:
                    if msg['method'] == CONNECT:
                        if self.handle_connect(msg):
                            self.client_sockets.add(client_socket)
                            client_socket.send(server.accept())
                            print(f"[client] -> {msg}")
                            t = threading.Thread(target=self.main_loop, args=(client_socket, msg["data"]["username"]))
                            t.daemon = True
                            t.start()
                            continue    #skip the rest of the code to avoid triping close connection

                client_socket.send(server.deny())
                client_socket.close()

            except KeyboardInterrupt:
                break

        print("\n[!]closing all sockets...")

        for cs in self.client_sockets:
            cs.close()
        self.s.close()

    def main_loop(self, cs, username):
        while True:
            try:
                msg = server.parse(cs.recv(1024).decode())
                print(f"[client] -> {msg}")
                if msg != server.PARSE_ERROR:
                    method = msg["method"]
                    if method == DISCONNECT:
                        self.handle_disconnect(username, cs)
                        break
                    elif method == GET:
                        self.handle_get(cs, msg)
                        continue
                    elif method == SEND:
                        self.handle_send(msg, username)
                        continue
                cs.send(server.error())
            except Exception as e:
                print(f"[!] Error: {e}")
                break
        print(EXIT_MSG)
        for i in self.users:
            if username == i["username"]:
                i["status"] = 0
                break
        self.client_sockets.remove(cs)

    def handle_disconnect(self, username, cs):
        for i in self.users:
            if username == i["username"]:
                i["status"] = 0
        for s in self.client_sockets:
            if s != cs:
                s.send(server.user_update(self.users))

    def handle_connect(self, msg):
        if "data" in msg:
            if ("username" in msg["data"]) and ("password" in msg["data"]):
                tmp = self.handle_authentication(msg["data"]["username"], msg["data"]["password"])
                if tmp:
                    for s in self.client_sockets:
                        s.send(server.user_update(self.users))
                return tmp
        return False

    def handle_get(self, cs, msg):
        if "data" in msg:
            if ("type" in msg["data"]):
                type = msg["data"]["type"]
                if type == GET_MESSAGES:
                    cs.send(server.data(self.messages, GET_MESSAGES))
                    return
                elif type == GET_USER_DATA:
                    cs.send(server.data(parse_users(self.users), GET_USER_DATA))
                    return
        cs.send(server.error())

    def handle_send(self, msg, username):
        if "data" in msg:
            if ("message" in msg["data"]):
                message_formated = client.new_message(username, msg["data"]["message"])
                self.messages.append(message_formated)
                for s in self.client_sockets:
                    s.send(server.new_message(message_formated))

    def handle_authentication(self, username, password):
        for i in self.users:
            if username == i["username"] and check_password(password, i["password"]) and i["status"] == 0:
                i["status"] = 1
                return True
        return False

if __name__ == '__main__':
    import sys

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
    chat_server = ChatServer(host=SERVER_HOST, port=SERVER_PORT)
    chat_server.load_user_file("users.csv")
    print(chat_server.users)
    chat_server.start()