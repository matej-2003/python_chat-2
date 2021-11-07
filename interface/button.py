import curses
import threading
import time

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

event_list = {}

class Button:
	def __init__(self, win, x, y, value, action=None):
		self.x = x
		self.y = y
		self.value = value
		self.length = len(value)
		self.action = action
		self.win = win
		event_list

	def is_hover(self, mouse_x, mouse_y):
		return mouse_y == self.y and mouse_x in range(self.x, self.x + self.length)

	def hover(self, mouse_x, mouse_y):
		if self.is_hover(mouse_x, mouse_y):
			if not not self.hover_action:
				self.win.addstr(self.y, self.x, self.value, get_pair("button_hover"))
				self.hover_action()

	def pressed(self, mouse_x, mouse_y):
		if self.is_hover(mouse_x, mouse_y):
			if not not self.action:
				self.win.addstr(self.y, self.x, self.value, get_pair("button_clicked"))
				self.action()

	def display(self):
		self.win.addstr(self.y, self.x, self.value, get_pair("button"))


def main(screen):
	curses.curs_set(0)
	curses.mousemask(1)
	set_pair("button", curses.COLOR_WHITE, curses.COLOR_BLUE)
	set_pair("button_clicked", curses.COLOR_WHITE, curses.COLOR_RED)
	set_pair("button_hover", curses.COLOR_WHITE, curses.COLOR_GREEN)
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)

	def action_1():
		screen.addstr(0, 0, "Hello!", curses.color_pair(1))
	def action_2():
		screen.addstr(0, 0, "Hello!", curses.color_pair(2))

	b1 = Button(screen, 5, 3, "<Button 1>", action=action_1)
	b2 = Button(screen, 5, 4, "<Button 2>", action=action_2)

	b1.display()
	b2.display()
	# screen.addstr(1, 0, "Red")
	# screen.addstr(2, 0, "Green")

	# def hover():
	# 	while True:
	# 		key = screen.getch()
	# 		if key == curses.KEY_MOUSE:
	# 			_, x, y, _, _ = curses.getmouse()
	# 		screen.addstr(10, 10, f"{x}{y}")
	
	# t = threading.Thread(target=hover)
	# t.start()

	def handle_event(event_list=[]):
		while True:
			key = screen.getch()
			if key == curses.KEY_EXIT:
				break
			for event_handler in event_list:
				if key == event_handler["event"]:
					for func in event_handler["action"]:
						if not not func:
							func()

	t = threading.Thread(handle_event, args=(event_list))

	while 1:
		screen.refresh()
		b1.display()
		b2.display()
		key = screen.getch()

		if key == ord("\t"):
			pass

		if key == curses.KEY_MOUSE:
			_, x, y, _, _ = curses.getmouse()
			b1.pressed(x, y)
			b2.pressed(x, y)
			screen.refresh()

		elif key == 27:
			break


if __name__ == '__main__':
	curses.wrapper(main)