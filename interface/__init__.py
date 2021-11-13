from interface.colors import BG_COLOR, get_pair, set_pair, color_list
from curses.textpad import Textbox
import curses
import time
import threading

class CharArt:
	def __init__(self, w, h, arts=[]):
		self.w = w
		self.h = h
		self.ascii_art = arts[0]
		self.ascii_art1 = arts[1]
		self.animation_colors = color_list([
			(curses.COLOR_BLUE, BG_COLOR),
			(curses.COLOR_WHITE, BG_COLOR),
			(curses.COLOR_RED, BG_COLOR),
			(curses.COLOR_GREEN, BG_COLOR),
			(curses.COLOR_YELLOW, BG_COLOR),
			(curses.COLOR_MAGENTA, BG_COLOR),
			(curses.COLOR_CYAN, BG_COLOR),
		])
		self.playing = True
	
	def stop(self):
		self.playing = False

	def draw_art(self, win, w, art, style):
		line_n = 0
		for line in art.split('\n'):
			win.addstr(line_n, int((w - 32) / 2), line, style)
			line_n += 1
	
	def animation(self, win, w, refresh=None):
		counter = 0
		while self.playing:
			counter = (counter + 1) % (len(self.animation_colors) - 1)
			win.clear()
			win.refresh()
			if counter % 2 == 0:
				self.draw_art(win, w, self.ascii_art, curses.A_BOLD | curses.color_pair(self.animation_colors[counter + 1]))
			else:
				self.draw_art(win, w, self.ascii_art1, curses.A_BOLD | curses.color_pair(self.animation_colors[counter + 1]))
			win.refresh()
			if not not refresh:
				refresh()
			time.sleep(0.5)

class LoginUI:
	def __init__(self, screen, banner=None):
		self.screen = screen
		self.status = 1
		self.banner = banner
		curses.start_color()
		set_pair("loadingbar", curses.COLOR_WHITE, BG_COLOR)
		set_pair("default", curses.COLOR_GREEN, BG_COLOR)
		set_pair("statusbar", curses.COLOR_WHITE, curses.COLOR_BLUE)
		set_pair("input", curses.COLOR_BLUE, curses.COLOR_WHITE)

		self.h, self.w = screen.getmaxyx()
		self.h = self.h - 1
		self.header_h = 5
		self.body_h = self.h - self.header_h
		self.header_w = self.w
		self.body_w = self.w

		self.header = curses.newwin(self.header_h, self.header_w, 0, 0)
		self.header_inner = curses.newwin(self.header_h-2, self.header_w-2, 1, 1)
		self.body = curses.newwin(self.body_h, self.body_w, self.header_h, 0)
		self.server_ip = curses.newwin(1, 16, self.header_h + 2, 20)
		self.username = curses.newwin(1, 16, self.header_h + 4, 20)
		self.password = curses.newwin(1, 16, self.header_h + 6, 20)
		self.statusbar = curses.newwin(1, self.w, self.h, 0)

		self.connection = False
		self.server_ip_ = None
		self.username_ = None
		self.password_ = None
	
	def update_bg(self):
		self.header.border()
		self.body.border()
		
		self.header.bkgd(" ", get_pair("default"))
		self.body.bkgd(" ", get_pair("default"))
		self.server_ip.bkgd(" ", get_pair("input"))
		self.username.bkgd(" ", get_pair("input"))
		self.password.bkgd(" ", get_pair("input"))
		self.statusbar.bkgd(" ", get_pair("statusbar"))

		self.body.addstr(0, 5, " LOGIN: ", curses.A_BOLD)
		self.body.addstr(2, 5, "SERVER IP :", curses.A_BOLD)
		self.body.addstr(4, 5, "USERNAME  :", curses.A_BOLD)
		self.body.addstr(6, 5, "PASSWORD  :", curses.A_BOLD)
		self.statusbar.addstr("\t Message | STATUS BAR")

	def update_dimensions(self):
		tmp_h, tmp_w = self.screen.getmaxyx()
		tmp_h = tmp_h - 1
		if tmp_h != self.h or tmp_w != self.w:
			self.h, self.w = tmp_h, tmp_w
			self.h = self.h - 1
			self.header_h = 5
			self.body_h = self.h - self.header_h
			self.header_w = self.w
			self.body_w = self.w

			self.header.resize(self.header_h, self.header_w)
			self.header.mnwin(0, 0)
			self.header_inner.resize(self.header_h-2, self.header_w-2)
			self.header_inner.mvwin(1, 1)
			self.body.resize(self.body_h, self.body_w)
			self.body.mvwin(self.header_h, 0)

			self.server_ip.resize(1, 16)
			self.server_ip.mvwin(self.header_h + 2, 20)
			self.username.resize(1, 16)
			self.username.mvwin(self.header_h + 4, 20)
			self.password.resize(1, 16)
			self.password.mvwin(self.header_h + 6, 20)

			self.statusbar.resize(1, self.w)
			self.statusbar.mvwin(self.h, 0)
			return True
		return False

	def refresh_all(self):
		self.screen.refresh()
		self.header.refresh()
		self.header_inner.refresh()
		self.body.refresh()
		self.statusbar.refresh()

		if not self.server_ip_:
			self.server_ip.refresh()
		else:
			if not self.username_:
				self.username.refresh()
			else:
				self.password.refresh()

	def update_loop(self):
		while self.status:
			tmp = self.update_dimensions()
			self.update_bg()
			if tmp:
				self.refresh_all()
			time.sleep(0.5)
	
	def connect_animation(self):
		from interface.loading_bar import LoadingBar
		import datetime

		start = time.time()
		bar = LoadingBar(20, bar_l=5, fg=" ", bg=".")
		text="Connecting: "
		form="[{b}]{s} ({t}s)"

		p = threading.Thread(target=self.connect)
		p.start()

		while not self.connection:
			self.body.refresh()
			screen = text + form.format(
				b=bar.get(),
				s=LoadingBar.spinner(bar.step),
				t=datetime.timedelta(seconds=(time.time() - start)).seconds
			)
			self.body.addstr(8, 5, screen, get_pair("loadingbar") | curses.A_BOLD)
			time.sleep(0.1)
	
	def connect(self):
		time.sleep(5)
		self.connection = True

	def start(self):
		self.update_dimensions()
		self.update_bg()

		t = threading.Thread(target=self.banner.animation, args=(self.header_inner, self.w, self.refresh_all))
		t.daemon = True
		t.start()

		self.refresh_all()
		self.server_ip.refresh()
		self.username.refresh()
		self.password.refresh()

		server_ip_input = Textbox(self.server_ip)
		server_ip_input.edit()
		self.server_ip_ = server_ip_input.gather()

		username_input = Textbox(self.username)
		username_input.edit()
		self.username_ = username_input.gather()

		password_input = Textbox(self.password)
		password_input.edit()
		self.password_ = password_input.gather()
		# while True:
		# 	server_ip_input.edit()
		# 	k = server_ip_input.gather()
		# 	if k == '':
		# 		break
		# 	time.sleep(0.5)
	
		# self.connect_animation()

		self.banner.stop()
		time.sleep(0.5)
		self.screen.clear()
		return (self.server_ip_, self.username_, self.password_)