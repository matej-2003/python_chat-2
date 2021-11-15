# server side
# 1. listen for clients
# 2. accept clients
# 3. auth clients (and give it a token)
# 4. wait for messages
# 5. save messages to messages=[]
# 6. disconect clients
# 7. on connect and disconect update clients on user status

# client side
# 1. establish connection
# 2. supply auth data (connect/disconnect)
# 3. download messages from server
# 4. submit message
# 5. disconnect

# client
import json
from datetime import datetime

CONNECT = "connect"
GET = "get"
GET_MESSAGES = "messages"
GET_USER_DATA = "user_data"
SEND = "send"
DISCONNECT = "disconnect"

AUTH = "auth"
NEW_MESSAGE = "new_message"
USERS_UPDATE = "users_update"
ERROR = "error"
AUTHORIZED = 1
UNAUTHORIZED = 0

class client:
    connect_request = {"method": CONNECT, "data": {"username": None, "password": None}}
    messages_request = {"method": GET, "data": {"type": GET_MESSAGES}}
    user_data_request = {"method": GET, "data": {"type": GET_USER_DATA}}
    send_message_request = {"method": SEND, "data": {"message": None}}
    disconnect_request = {"method": DISCONNECT}
    message_format = {"from": None, "time": None, "content": None}
    PARSE_ERROR = 10

    @classmethod
    def parse(cls, msg, logger=None):
        try:
            message_formated = json.loads(msg)
            if "type" in message_formated:
                if message_formated["type"] in (AUTH, GET, NEW_MESSAGE, USERS_UPDATE, ERROR, DISCONNECT):
                    return message_formated
            if not not logger:
                logger(f"'{msg}' invalid message")
            return cls.PARSE_ERROR
        except json.JSONDecodeError:
            if not not logger:
                logger(f"'{msg}' invalid message")
            return cls.PARSE_ERROR

    @staticmethod
    def connect(username, password):
        return json.dumps({"method": CONNECT, "data": {"username": username, "password": password}})

    @staticmethod
    def disconnect():
        return json.dumps({"method": DISCONNECT})

    @staticmethod
    def send(msg):
        return json.dumps({"method": SEND, "data": {"message": msg}})

    @staticmethod
    def new_message(sender, content, timestamp_pattern='%H:%M:%S'):
        return {"from": sender, "time": datetime.now().strftime(timestamp_pattern), "content": content}

    @staticmethod
    def get(type):
        return json.dumps({"method": GET, "data": {"type": type}})

    @classmethod
    def get_messages(cls):
        return json.dumps(cls.messages_request)

    @classmethod
    def get_users(cls):
        return json.dumps(cls.user_data_request)

class server:
    # server puts the Client in the client_list
    # and returns the accept_response
    # server returns the deny_response and closes the connection
    PARSE_ERROR = 10
    PARSE_OK = 9

    @classmethod
    def parse(cls, msg, logger=None):
        try:
            message_formated = json.loads(msg)
            if "method" in message_formated:
                if message_formated["method"] in (CONNECT, SEND, GET, DISCONNECT, NEW_MESSAGE, USERS_UPDATE):
                    return (cls.PARSE_OK, message_formated)
            if not not logger:
                logger(f"'{msg}' invalid message")
            return (cls.PARSE_ERROR, message_formated)
        except json.JSONDecodeError:
            if not not logger:
                logger(f"'{msg}' invalid message")
            return (cls.PARSE_ERROR, f'json error {msg}')

    accept_response = {"type": AUTH, "response": AUTHORIZED}
    deny_response = {"type": AUTH, "response": UNAUTHORIZED, "desc": "invalid credentials"}
    messages_response = {"type": GET, "response": {"type": GET_USER_DATA, "data": None}}
    user_data_response = {"type": GET, "response": {"type": GET_MESSAGES, "data": None}}
    new_message = {"type": NEW_MESSAGE, "response": {"from": None, "time": None, "content": None}}
    user_update = {"type": USERS_UPDATE, "response": None}
    disconnect_response = {"type": DISCONNECT}
    error_response = {"type": ERROR, "response": "invalid request"}

    @staticmethod
    def accept():
        return json.dumps({"type": AUTH, "response": AUTHORIZED})

    @staticmethod
    def deny():
        return json.dumps({"type": AUTH, "response": UNAUTHORIZED, "desc": "invalid credentials"})

    @staticmethod
    def data(data, type):
        return json.dumps({"type": GET, "response": {"type": type, "data": data}})

    # @staticmethod
    # def new_message(username, content):
        # return json.dumps({"type": NEW_MESSAGE, "response": {"from": username, "time": datetime.now().strftime('%H:%M:%S'), "date": content}})

    @staticmethod
    def new_message(msg):
        return json.dumps({"type": NEW_MESSAGE, "response": msg})

    @staticmethod
    def user_update(users):
        users_formated = [(i["username"], i["status"]) for i in users]
        return json.dumps({"type": USERS_UPDATE, "response": users_formated})

    @classmethod
    def disconnect(cls):
        return json.dumps(cls.disconnect_response)

    @staticmethod
    def error(type="invalid request", desc=""):
        return json.dumps({"type": ERROR, "response": type, "desc": desc})
