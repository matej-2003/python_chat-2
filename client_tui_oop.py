from chat_client import ChatClient
import curses
from curses.textpad import Textbox
import threading
import time

BG_COLOR = 0

colors = {}
pairs = {}
name_counter = 0

def set_color(name, *args):
	global name_counter
	name_counter += 1
	colors[name] = name_counter
	curses.init_color(name_counter, *args)

def get_color(name):
	return colors[name]

def set_pair(name, *args):
	global name_counter
	name_counter += 1
	pairs[name] = name_counter
	curses.init_pair(name_counter, *args)

def get_pair(name):
	return curses.color_pair(pairs[name])

class ChatClientTUI:
	def __init__(self, screen, chat_client):
		self.screen = screen
		self.chat_client = chat_client
		self.chat_client.on_new_message = self.on_new_message
		self.chat_client.on_user_update = self.on_user_update
		self.status = 0
		# self.BG_COLOR = 0
		# self.colors = {}
		# self.pairs = {}
		# self.name_counter = 0
		curses.start_color()
		set_pair("user_online", curses.COLOR_GREEN, BG_COLOR)
		set_pair("user_ofline", curses.COLOR_RED, BG_COLOR)
		set_pair("user", curses.COLOR_WHITE, BG_COLOR)
		set_pair("title", curses.COLOR_WHITE, BG_COLOR)
		set_pair("message_date", curses.COLOR_GREEN, BG_COLOR)
		set_pair("message_user", curses.COLOR_YELLOW, BG_COLOR)
		set_pair("message_text", curses.COLOR_WHITE, BG_COLOR)
		set_pair("statusbar", curses.COLOR_WHITE, curses.COLOR_BLUE)

		self.h, self.w = self.screen.getmaxyx()
		self.h = self.h - 1
		self.sidebar_w = int((1/5) * self.w)
		self.chatbox_w = int((4/5) * self.w) - 1
		self.textpanel_w = int((4/5) * self.w) - 1
		self.sidebar_h = self.h
		self.chatbox_h = int((8/10) * self.h)
		self.textpanel_h = int((2/10) * self.h)
		if self.chatbox_h + self.textpanel_h >= self.h:
			self.textpanel_h -= 1

		self.sidebar = curses.newwin(self.sidebar_h, self.sidebar_w, 0, 0)
		self.sidebar_inner = curses.newwin(self.sidebar_h-2, self.sidebar_w-2, 1, 1)
		self.chatbox = curses.newwin(self.chatbox_h, self.chatbox_w+1, 0, self.sidebar_w)
		self.chatbox_inner = curses.newwin(self.chatbox_h-2, self.chatbox_w-2, 1, self.sidebar_w+1)
		self.textbox = curses.newwin(self.textpanel_h+1, self.textpanel_w+1, self.chatbox_h, self.sidebar_w)
		self.textbox_inner = curses.newwin(self.textpanel_h-1, self.textpanel_w-1, self.chatbox_h+1, self.sidebar_w+1)
		self.statusbar = curses.newwin(1, self.w, self.h, 0)

		# self.update_dimensions()
		self.update_bg()

	def update_bg(self):
		self.sidebar.border()
		self.chatbox.border()
		self.textbox.border()
		# self.sidebar.bkgd(" ", get_pair("message_text"))
		# self.sidebar_inner.bkgd(" ", get_pair("message_text"))
		# self.chatbox.bkgd(" ", get_pair("message_text"))
		# self.textbox_inner.bkgd(" ", get_pair("message_text"))
		self.statusbar.bkgd(" ", get_pair("statusbar"))
		self.sidebar.addstr(0, 1, " User list: ", curses.A_BOLD | get_pair("title"))
		self.chatbox.addstr(0, 1, " Messages: ", curses.A_BOLD | get_pair("title"))
		self.textbox.addstr(0, 1, " Write a message: ", curses.A_BOLD | get_pair("title"))
		self.statusbar.addstr(0, 0, "\tCTRL+G to send | To exit enter 'q' and send | STATUS BAR")
	
	def update_dimensions(self):
		self.h, self.w = self.screen.getmaxyx()
		self.h = self.h - 1
		self.sidebar_w = int((1/5) * self.w)
		self.chatbox_w = int((4/5) * self.w) - 1
		self.textpanel_w = int((4/5) * self.w) - 1
		self.sidebar_h = self.h
		self.chatbox_h = int((8/10) * self.h)
		self.textpanel_h = int((2/10) * self.h)
		if self.chatbox_h + self.textpanel_h >= self.h:
			self.textpanel_h -= 1

		self.sidebar.resize(self.sidebar_h, self.sidebar_w)
		self.sidebar.mvwin(0, 0)

		self.sidebar_inner.resize(self.sidebar_h-2, self.sidebar_w-2)
		self.sidebar_inner.mvwin(1, 1)

		self.chatbox.resize(self.chatbox_h, self.chatbox_w+1)
		self.chatbox.mvwin(0, self.sidebar_w)

		self.chatbox_inner.resize(self.chatbox_h-2, self.chatbox_w-2)
		self.chatbox_inner.mvwin(1, self.sidebar_w+1)

		self.textbox.resize(self.textpanel_h+1, self.textpanel_w+1)
		self.textbox.mvwin(self.chatbox_h, self.sidebar_w)

		self.textbox_inner.resize(self.textpanel_h-1, self.textpanel_w-1)
		self.textbox_inner.mvwin(self.chatbox_h+1, self.sidebar_w+1)

		self.statusbar.resize(1, self.w)
		self.statusbar.mvwin(self.h, 0)

	def refresh_all(self):
		self.screen.clear()
		self.screen.refresh()
		self.sidebar.refresh()
		self.sidebar_inner.refresh()
		self.chatbox.refresh()
		self.chatbox_inner.refresh()
		self.statusbar.refresh()
		self.textbox.refresh()
		self.textbox_inner.refresh()

	def update_all(self):
		while self.status:
			self.update_dimensions()
			# self.update_bg()
			self.refresh_all()
			time.sleep(1)
	
	def on_new_message(self):
		self.chatbox_inner.clear()
		for i in self.chat_client.messages:
			self.display_message(i)

	def on_user_update(self):
		self.sidebar_inner.clear()
		for user, status in self.chat_client.users:
			if status:
				self.sidebar_inner.addstr("● ",  get_pair("user_online") | curses.A_BOLD)
			else:
				self.sidebar_inner.addstr("● ",  get_pair("user_ofline") | curses.A_BOLD)
			self.sidebar_inner.addstr(user, get_pair("user") | curses.A_BOLD)
			self.sidebar_inner.addstr("\n")

	def display_message(self, msg):
		date_format = "[%s]" % (msg[0])
		self.chatbox_inner.addstr(date_format, get_pair("message_date"))
		self.chatbox_inner.addstr(f" {msg[1]}: ", get_pair("message_user"))
		self.chatbox_inner.addstr(msg[2] + "\n", get_pair("message_text"))
		self.chatbox_inner.refresh()

	def start(self):
		self.chat_client.connect()
		self.status = 1
		self.on_new_message()
		self.on_user_update()
		self.refresh_all()

		t = threading.Thread(target=self.update_all)
		t.daemon = True
		t.start()
		box = Textbox(self.textbox_inner)
		
		while True:
			box.edit()
			msg = box.gather().strip("\n").strip(" ")
			self.textbox_inner.erase()
			if msg.lower() == 'q':
				self.status = 0
				self.chat_client.disconnect()
				break
		exit()

def main(screen):
	cc = ChatClient(host="0.0.0.0", port=5002, username="matej", password="kodermac")
	app = ChatClientTUI(screen, cc)
	app.start()

if __name__ == "__main__":
	curses.wrapper(main)