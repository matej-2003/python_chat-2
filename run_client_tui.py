import curses
from chat_client import ChatClient, ChatClientTUI

def main(screen):
	import sys
	USERNAME = "matej"
	PASSWORD = "kodermac"
	HOST = "127.0.0.1"
	PORT = 5002

	if len(sys.argv) == 3:
		USERNAME = sys.argv[1]
		PASSWORD = sys.argv[2]
	elif len(sys.argv) == 4:
		USERNAME = sys.argv[1]
		PASSWORD = sys.argv[2]
		HOST = sys.argv[3]
	elif len(sys.argv) == 5:
		USERNAME = sys.argv[1]
		PASSWORD = sys.argv[2]
		HOST = sys.argv[3]
		PORT = int(sys.argv[4])
	else:
		print("""
			usage:
				python run_client_tui.py [USERNAME] [PASSWORD] [HOST] [PORT]
				default host = 127.0.0.1
				default port = 5002
			""")
		exit()
	curses.curs_set(1)
	cc = ChatClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
	app = ChatClientTUI(screen, cc)
	app.start()

if __name__ == "__main__":
	curses.wrapper(main)
