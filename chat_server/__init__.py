from interface.colors import set_pair, get_pair, BG_COLOR
from chat_server.chat_server import ChatServer
from curses.textpad import Textbox
import curses
import threading
import time

class ChatServerTUI:
	def __init__(self, screen):
		self.screen = screen
		curses.start_color()
		set_pair("default", curses.COLOR_WHITE, BG_COLOR)
		set_pair("menu", curses.COLOR_WHITE, BG_COLOR)
		set_pair("menu_selected", curses.COLOR_BLACK, curses.COLOR_WHITE)
		set_pair("title", curses.COLOR_WHITE, BG_COLOR)
		set_pair("statusbar", curses.COLOR_WHITE, curses.COLOR_BLUE)

		self.h, self.w = self.screen.getmaxyx()
		self.body_w = self.w
		self.body_h = self.h - 2

		self.body = curses.newwin(self.body_h, self.body_w, 0, 0)
		self.body_inner = curses.newwin(self.body_h-2, self.body_w-2, 1, 1)
		self.commandbox = curses.newwin(1, self.w, self.h-2, 1)
		self.statusbar = curses.newwin(1, self.w, self.h-1, 0)

		self.update_bg()
		self.menu = ["HOME", "SETTINGS", "USERS", "USER GROUPS"]

	def update_bg(self):
		self.body.border()
		self.statusbar.bkgd(" ", get_pair("statusbar"))
		self.commandbox.bkgd(" ", get_pair("statusbar"))
		self.body.addstr(0, 1, " SERVER ", curses.A_BOLD | get_pair("title"))
		self.commandbox.addstr(0, 0, ":")
		self.statusbar.addstr(0, 0, "\tCTRL+G to send | To exit enter 'q' and send | STATUS BAR")
	
	def update_dimensions(self):
		tmp_h, tmp_w = self.screen.getmaxyx()
		tmp_h = tmp_h
		if tmp_h != self.h or tmp_w != self.w:
			self.h = tmp_h
			self.w = tmp_w
			self.body_w = self.w
			self.body_h = self.h - 2

			self.body = curses.newwin(self.body_h, self.body_w, 0, 0)
			self.body_inner = curses.newwin(self.body_h-2, self.body_w-2, 1, 1)
			self.commandbox = curses.newwin(1, self.w, self.h-2, 0)
			self.statusbar = curses.newwin(1, self.w, self.h-1, 0)

			self.body.resize(self.body_h, self.body_w)
			self.body.mvwin(0, 0)

			self.body_inner.resize(self.body_h-2, self.body_w-2)
			self.body_inner.mvwin(1, 1)

			self.commandbox.resize(1, self.w)
			self.commandbox.mvwin(self.h-2, 0)

			self.statusbar.resize(1, self.w)
			self.statusbar.mvwin(self.h-1, 0)
			return True
		return False

	def refresh_all(self):
		self.screen.refresh()
		self.body.refresh()
		self.body_inner.refresh()
		self.statusbar.refresh()
		self.commandbox.refresh()

	def update_loop(self):
		while True:
			tmp = self.update_dimensions()
			self.update_bg()
			if tmp:
				self.refresh_all()
			time.sleep(0.5)

	def display_menu(self, selection):
		for i, e in enumerate(self.menu):
			if selection == i:
				self.body_inner.addstr(0+i, 1, e, get_pair("menu_selected"))
			else:
				self.body_inner.addstr(0+i, 1, e, get_pair("menu"))

	def start(self):
		# t = threading.Thread(target=self.update_loop)
		# t.daemon = True
		# t.start()

		selection = 0
		self.display_menu(selection)
		self.refresh_all()
		
		while True:
			k = self.commandbox.getch()
			self.body_inner.addstr(8, 1, str(selection), get_pair("menu"))

			if k == ord('w'):
				selection -= 1
				selection %= len(self.menu)
			elif k == ord('s'):
				selection += 1
				selection %= len(self.menu)
			elif k == ord('q'):
				break
			self.display_menu(selection)
			self.refresh_all()
		exit()