import curses
from ChatClient import ChatClient, ChatClientTUI

def main(screen):
	import sys
	USERNAME = "matej"
	PASSWORD = "kodermac"

	if len(sys.argv) == 3:
		USERNAME = sys.argv[1]
		PASSWORD = sys.argv[2]
	else:
		exit()
	cc = ChatClient(host="0.0.0.0", port=5002, username=USERNAME, password=PASSWORD)
	app = ChatClientTUI(screen, cc)
	app.start()

if __name__ == "__main__":
	curses.wrapper(main)
