from interface import CharArt
from interface import LoginUI
import curses

ip, username, password = None, None, None

def main(screen):
	global ip, username, password
	ascii_art = """
╔═╗╦ ╦╦═╗╔═╗╔══╔═╗  ╔═╗╦ ╦╔═╗╔╦╗
║  ║ ║╠╦╝╚═╗╠═ ╚═╗  ║  ╠═╣╠═╣ ║ 
╚═╝╚═╝╩╚═╚═╝╚══╚═╝  ╚═╝╩ ╩╩ ╩ ╩ """.strip("\n ")

	ascii_art1 = """
┌─┐┬ ┬┬─┐┌─┐┌──┌─┐  ┌─┐┬ ┬┌─┐┌┬┐
│  │ │├┬┘└─┐├─ └─┐  │  ├─┤├─┤ │ 
└─┘└─┘┴└─└─┘└──└─┘  └─┘┴ ┴┴ ┴ ┴ """.strip("\n ")
	banner = CharArt(32, 3, arts=[ascii_art, ascii_art1])
	app = LoginUI(screen, banner=banner)
	ip, username, password = app.start()
	ip = ip.strip(" ")
	password = password.strip(" ")
	username = username.strip(" ")

	if (not not ip) and (not not username) and (not not password):
		from chat_client import ChatClient, ChatClientTUI
		cc = ChatClient(host=ip, port=5002, username=username, password=password)
		app = ChatClientTUI(screen, cc)
		app.start()

if __name__ == "__main__":
	curses.wrapper(main)
	print(ip, username, password)