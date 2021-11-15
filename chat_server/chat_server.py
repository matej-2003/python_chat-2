import socket
import threading
from protocol.messages import *
from protocol import check_password
from cryptography import Crypto
import cryptography
import csv

class ChatServer:
    EXIT_MSG = "connection closed..."
    ERROR = "error {}"
    def __init__(self, host='127.0.0.1', port=8888, encryption=None):
        self.host = host
        self.port = port
        self.s = None
        self.client_sockets = set()
        self.users = []
        self.messages = []

        self.encryption = Crypto()
        if encryption:
            self.encryption = encryption
        self.encryption.encode = True
    
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
                enc_msg = client_socket.recv(1024).decode()
                encription_status, dec_msg = self.encryption.decrypt(enc_msg)

                if encription_status != cryptography.DECRYPTION_ERROR:
                    parse_status, msg = server.parse(dec_msg)
                    if parse_status != server.PARSE_ERROR:
                        if msg['method'] == CONNECT:
                            if self.handle_connect(msg):
                                self.client_sockets.add(client_socket)
                                client_socket.sendall(self.encryption.encrypt(server.accept()))
                                print(f"\u001b[31m[client]\u001b[0m -> DEC:{msg}\n\u001b[36mENC{enc_msg.encode()}\u001b[0m")
                                t = threading.Thread(target=self.main_loop, args=(client_socket, msg["data"]["username"]))
                                t.daemon = True
                                t.start()
                                continue    #skip the rest of the code to avoid triping close connection
                print(f"[error] -> {dec_msg}")
                client_socket.sendall(self.encryption.encrypt(server.deny()))
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
                enc_msg = cs.recv(1024).decode()
                encription_status, dec_msg = self.encryption.decrypt(enc_msg)
                if encription_status != cryptography.DECRYPTION_ERROR:
                    parse_status, msg = server.parse(dec_msg)
                    if parse_status != server.PARSE_ERROR:
                        print(f"\u001b[31m[client]\u001b[0m -> DEC:{msg}\n\u001b[36mENC:{enc_msg.encode()}\u001b[0m")
                        method = msg["method"]
                        if method == DISCONNECT:
                            self.handle_disconnect(cs, username)
                            break
                        elif method == GET:
                            self.handle_get(cs, msg)
                            continue
                        elif method == SEND:
                            self.handle_send(msg, username)
                            continue
                print(f"[error] -> {dec_msg}")
                cs.sendall(self.encryption.encrypt(server.error()))
            except Exception as e:
                cs.sendall(self.encryption.encrypt(server.error()))
                print(f"[!] Error: {e}")
                break
        print(ChatServer.EXIT_MSG)
        for i in self.users:
            if username == i["username"]:
                i["status"] = 0
                break
        self.client_sockets.remove(cs)

    def handle_disconnect(self, cs, username):
        cs.sendall(self.encryption.encrypt(server.disconnect()))
        for i in self.users:
            if username == i["username"]:
                i["status"] = 0
        for s in self.client_sockets:
            if s != cs:
                s.sendall(self.encryption.encrypt(server.user_update(self.users)))

    def handle_connect(self, msg):
        if "data" in msg:
            if ("username" in msg["data"]) and ("password" in msg["data"]):
                tmp = self.handle_authentication(msg["data"]["username"], msg["data"]["password"])
                if tmp:
                    for cs in self.client_sockets:
                        cs.sendall(self.encryption.encrypt(server.user_update(self.users)))
                return tmp
        return False

    def handle_get(self, cs, msg):
        if "data" in msg:
            if ("type" in msg["data"]):
                type = msg["data"]["type"]
                if type == GET_MESSAGES:
                    cs.sendall(self.encryption.encrypt(server.data(self.messages, GET_MESSAGES)))
                    return
                elif type == GET_USER_DATA:
                    cs.sendall(self.encryption.encrypt(server.data(ChatServer.parse_users(self.users), GET_USER_DATA)))
                    return
        cs.sendall(self.encryption.encrypt(server.error()))

    def handle_send(self, msg, username):
        if "data" in msg:
            if ("message" in msg["data"]):
                message_formated = client.new_message(username, msg["data"]["message"])
                self.messages.append(message_formated)
                for cs in self.client_sockets:
                    cs.sendall(self.encryption.encrypt(server.new_message(message_formated)))

    def handle_authentication(self, username, password):
        for i in self.users:
            if username == i["username"] and check_password(password, i["password"]) and i["status"] == 0:
                i["status"] = 1
                return True
        return False
    
    @staticmethod
    def parse_users(users):
        return [(i["username"], i["status"]) for i in users]