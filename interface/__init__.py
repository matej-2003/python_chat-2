import curses

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