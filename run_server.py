from chat_server.chat_server import ChatServer

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
    print([i["username"] for i in chat_server.users])
    chat_server.start()