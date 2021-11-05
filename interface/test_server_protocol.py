import json
from datetime import datetime

EXIT_MSG = "connection closed..."
ERROR = "error {}"
PROMPT = "server{}: "

# methods
CONNECT = "connect"
SEND = "send"
GET = "get"
DISCONNECT = "disconnect"

GET_MESSAGES = "messages"
GET_USER_DATA = "user_data"
GET_USER_STATUS = "user_status"

users = [
    {
        "username": "matej",
        "password": "kodermac",
    },
    {
        "username": "john",
        "password": "denver",
    }
]

messages = [
    {
        "from": "matej",
        "time": datetime.now().strftime('%H:%M:%S'),
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce laoreet erat pharetra, fringilla enim non, dignissim erat.",
    } for _ in range(5)
]

def format_message(message):
    try:
        message_formated = json.loads(message)
        if "method" in message_formated.keys():
            if message_formated["method"] in (CONNECT, SEND, GET, DISCONNECT):
                return message_formated
        print(ERROR.format(" invalid message"))
        return False
    except json.JSONDecodeError:
        print(ERROR.format(" invalid message"))
        return False

def auth(username, password):
    for i in users:
        if username == i["username"] and password == i["password"]:
            return True

def connect(msg):
    if "data" in msg:
        if ("username" in msg["data"]) and ("password" in msg["data"]):
            return auth(msg["data"]["username"], msg["data"]["password"])
    return False

def get(msg):
    if "data" in msg:
        if ("type" in msg["data"]):
            type = msg["data"]["type"]
            if type == GET_MESSAGES:
                print(json.dumps(messages))
            elif type == GET_USER_DATA:
                print("user data")
            elif type == GET_USER_STATUS:
                print("user status data")

def send(msg):
    if "data" in msg:
        if ("message" in msg["data"]):
            print(f"you send a message {msg}")

def main_loop():
    while True:
        msg = format_message(input(PROMPT.format(" (authenticated)")))
        if msg:
            if msg["method"] == DISCONNECT:
                break
            elif msg["method"] == GET:
                get(msg)
            elif msg["method"] == SEND:
                send(msg)
            else:
                print(ERROR.format(" invalid message"))

msg = format_message(input(PROMPT.format("")))

if msg:
    if msg['method'] == CONNECT:
        if connect(msg):
            main_loop()
print(EXIT_MSG)
