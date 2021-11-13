import curses

BG_COLOR = curses.COLOR_BLACK

colors = {}
pairs = {}
name_counter = 0

def set_color(name, *args):
	global name_counter
	name_counter += 1
	colors[name] = name_counter
	curses.init_color(name_counter, *args)

def color_list(colors=[]):
	global name_counter
	color_list = []
	for i in colors:
		name_counter += 1
		color_list.append(name_counter)
		curses.init_pair(name_counter, *i)
	return color_list

def get_color(name):
	return colors[name]

def set_pair(name, *args):
	global name_counter
	name_counter += 1
	pairs[name] = name_counter
	curses.init_pair(name_counter, *args)

def get_pair(name):
	return curses.color_pair(pairs[name])