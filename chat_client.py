from json.decoder import JSONDecodeError
import threading
from protocol.messages import *
import socket
import time

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5002, username="", password=""):
        self.host = host
        self.port = port
        self.messages = []
        self.users = []
        self.username = username
        self.password = password
        self.s = None
        self.on_new_message = None
        self.on_user_update = None
        self.conn_status = 0
    
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
        self.s.send(client.connect(self.username, self.password))

        msg = self.s.recv(1024).decode()
        msg = client.parse(msg)
        # print(f"[server] -> {msg}")
        if msg != client.PARSE_ERROR:
            if msg["response"] == UNAUTHORIZED:
                # print("[!] UNAUTHORIZED closing connection ...")
                time.sleep(0.5)
                self.s.close()
                exit()
        else:
            # print("[!] INVALID REQUEST closing connection ...")
            time.sleep(0.5)
            self.s.close()
            exit()
        self.conn_status = 1
        # print("[+] successful authentication")

        t = threading.Thread(target=self.listen_for_messages)
        t.deamon = True
        t.start()

        self.get_messages()
        self.get_users()

    def listen_for_messages(self):
        while self.conn_status:
            message = self.s.recv(1024).decode()
            try:
                message = client.parse(message)
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

                    # print('[server] -> {}\n'.format(message), end='')
            except JSONDecodeError:
                pass
    
    def handle_get(self, message):
        if message["response"]["type"] == GET_MESSAGES:
            self.messages = message["response"]["data"]
        elif message["response"]["type"] == GET_USER_DATA:
            self.users = message["response"]["data"]
    
    def send(self, msg):
        self.s.send(client.send(msg))

    def disconnect(self):
        self.s.send(client.disconnect())
        self.conn_status = 0
        time.sleep(0.1)
        self.s.close()
    
    def get_messages(self):
        self.s.send(client.get_messages())

    def get_users(self):
        self.s.send(client.get_users())

    def handle_new_message(self, message):
        self.messages.append(message.response)
        if not not self.on_new_message:
            self.on_new_message()

    def handle_user_update(self, message):
        self.users = message.response.data
        if not not self.on_user_update:
            self.on_user_update()

    def handle_error(self, message):
        # print(f"[server] -> ERROR : {message}")


# if __name__ == '__main__':
#     SERVER_HOST = "127.0.0.1"
#     SERVER_PORT = 5002

#     if len(sys.argv) == 3:
#         SERVER_HOST = str(sys.argv[1])
#         SERVER_PORT = int(sys.argv[2])
#     elif len(sys.argv) == 2:
#         SERVER_HOST = str(sys.argv[1])
#     else:
#         print("""
#         Correct ussage:
#             'script IP PORT'
#             'script IP'
#             default port is 5002
#         """)
    
#     app = ChatClient(host=SERVER_HOST, port=SERVER_PORT, username="matej", password="kodermac")
#     app.connect()

#     time.sleep(1)
#     app.disconnect()