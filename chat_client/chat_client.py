from json.decoder import JSONDecodeError
import threading
from protocol.messages import *
from cryptography import Crypto
import cryptography
import socket
import time

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5002, username="", password="", encryption=None):
        self.host = host
        self.port = port
        self.messages = []
        self.messages_response = False
        self.users = []
        self.user_data_response = False
        self.username = username
        self.password = password
        self.s = None
        self.on_new_message = None
        self.on_user_update = None
        self.conn_status = 0
        self.t = None

        self.encryption = Crypto()
        if encryption:
            self.encryption = encryption
        self.encryption.encode = True

    def action_func(self, on_new_message, on_user_update):
        self.on_new_message = on_new_message
        self.on_user_update = on_user_update

    def connect(self, username=None, password=None):
        if not not username:
            self.username = username
        if not not password:
            self.password = password

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(f"[*] Connecting to {self.host}:{self.port}...")
        self.s.connect((self.host, self.port))
        # print("[+] Connected.")
        # print("[+] sending connect request")
        self.s.sendall(self.encryption.encrypt(client.connect(self.username, self.password)))

        encription_status, dec_msg = self.encryption.decrypt(self.s.recv(1024).decode())
        if encription_status != cryptography.DECRYPTION_ERROR:
            msg = client.parse(dec_msg)
            # print(f"[server] -> {dec_msg}")
            if msg != client.PARSE_ERROR:
                if msg["response"] != UNAUTHORIZED:
                    self.conn_status = 1
                    print("[+] successful authentication")

                    self.t = threading.Thread(target=self.listen_for_messages)
                    self.t.deamon = True
                    self.t.start()
                    time.sleep(0.01)
                    self.request_messages()
                    time.sleep(0.01)
                    self.request_user_data()
                else:
                    print("[!] UNAUTHORIZED closing connection ...")
                    time.sleep(0.5)
                    self.s.close()
                    exit()
            else:
                print("[!] INVALID REQUEST closing connection ...")
                time.sleep(0.5)
                self.s.close()
                # exit()
        else:
            print("[!] DECRYPTION ERROR closing connection ...")
            time.sleep(0.5)
            self.s.close()

    def listen_for_messages(self):
        while self.conn_status:
            encription_status, dec_msg = self.encryption.decrypt(self.s.recv(1024).decode())
            if encription_status != cryptography.DECRYPTION_ERROR:
                message = client.parse(dec_msg)
                # print(message)
                if message != client.PARSE_ERROR:
                    if message["type"] == GET:
                        self.handle_get(message)
                    elif message["type"] == NEW_MESSAGE:
                        self.handle_new_message(message)
                    elif message["type"] == USERS_UPDATE:
                        self.handle_user_update(message)
                    elif message["type"] == ERROR:
                        self.handle_error(message)
    
    def handle_get(self, message):
        if message["response"]["type"] == GET_MESSAGES:
            self.messages = message["response"]["data"]
            self.messages_response = True
        elif message["response"]["type"] == GET_USER_DATA:
            self.users = message["response"]["data"]
            self.user_data_response = True
    
    def send(self, msg):
        self.s.sendall(self.encryption.encrypt(client.send(msg)))

    def disconnect(self):
        """
            `time.sleep(0.05)` the purpuse of this line of code is to
            wait for the server to send another message to continue
            the blocking line 64 `message = client.parse(message)` (it doesent matter what message is as long as its sent)
            the line is stopping the `self.t` thread from checking the `self.conn_status` because it is a blocking peace
            of code and it is preventing the program to properly exit.
        """
        self.s.sendall(self.encryption.encrypt(client.disconnect()))
        self.conn_status = 0
        time.sleep(0.05)
        self.s.close()
    
    def request_messages(self):
        self.s.sendall(self.encryption.encrypt(client.get_messages()))
    
    def get_messages(self):
        while not self.messages_response:
            pass
        return self.messages

    def request_user_data(self):
        self.s.sendall(self.encryption.encrypt(client.get_users()))

    def get_user_data(self):
        while not self.user_data_response:
            pass
        return self.users

    def handle_new_message(self, message):
        self.messages.append(message["response"])
        if not not self.on_new_message:
            self.on_new_message()

    def handle_user_update(self, message):
        self.users = message["response"]
        if not not self.on_user_update:
            self.on_user_update()

    def handle_error(self, message):
        pass
        # print(f"[server] -> ERROR : {message}")