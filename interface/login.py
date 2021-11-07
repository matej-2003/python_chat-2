import curses
from curses.textpad import Textbox
import time
# from playsound import playsound
import threading

colors = {}
pairs = {}
name_counter = 0

def set_color(name, *args):
    global name_counter
    name_counter += 1
    colors[name] = name_counter
    curses.init_color(name_counter, *args)

def set_pair(name, *args):
    global name_counter
    name_counter += 1
    pairs[name] = name_counter
    curses.init_pair(name_counter, *args)

def get_pair(name):
    return curses.color_pair(colors[name])

BG_COLOR = curses.COLOR_BLUE

art_w = 32
art_h = 3

ascii_art = """
╔═╗╦ ╦╦═╗╔═╗╔══╔═╗  ╔═╗╦ ╦╔═╗╔╦╗
║  ║ ║╠╦╝╚═╗╠═ ╚═╗  ║  ╠═╣╠═╣ ║ 
╚═╝╚═╝╩╚═╚═╝╚══╚═╝  ╚═╝╩ ╩╩ ╩ ╩ """.strip("\n").strip(" ")

ascii_art1 = """
┌─┐┬ ┬┬─┐┌─┐┌──┌─┐  ┌─┐┬ ┬┌─┐┌┬┐
│  │ │├┬┘└─┐├─ └─┐  │  ├─┤├─┤ │ 
└─┘└─┘┴└─└─┘└──└─┘  └─┘┴ ┴┴ ┴ ┴ """.strip("\n").strip(" ")

def draw_art(win, w, art, style):
    line_n = 0
    for line in art.split('\n'):
        win.addstr(line_n, int((w - art_w) / 2), line, style)
        line_n += 1

def main(screen):
    screen = curses.initscr()
    curses.start_color()
    curses.init_color(1, 94, 9, 0)
    curses.init_color(2, 255, 255, 255)
    curses.init_pair(13, 2, 1)
    curses.init_pair(14, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(15, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.init_pair(1, curses.COLOR_BLUE, BG_COLOR)
    curses.init_pair(2, curses.COLOR_WHITE, BG_COLOR)
    curses.init_pair(3, curses.COLOR_RED, BG_COLOR)
    curses.init_pair(4, curses.COLOR_GREEN, BG_COLOR)
    curses.init_pair(5, curses.COLOR_YELLOW, BG_COLOR)
    curses.init_pair(6, curses.COLOR_MAGENTA, BG_COLOR)
    curses.init_pair(7, curses.COLOR_CYAN, BG_COLOR)

    h, w = screen.getmaxyx()
    h = h - 1
    header_h = 5
    body_h = h - header_h
    header_w = w
    body_w = w

    header = curses.newwin(header_h, header_w, 0, 0)
    header.border()
    header.bkgd(" ", curses.color_pair(13))
    header_inner = curses.newwin(header_h-2, header_w-2, 1, 1)

    body = curses.newwin(body_h, body_w, header_h, 0)
    body.border()
    body.bkgd(" ", curses.color_pair(13))
    body.addstr(0, 5, " LOGIN: ", curses.A_BOLD)

    body.addstr(2, 5, "SERVER IP :", curses.A_BOLD)
    body.addstr(4, 5, "USERNAME  :", curses.A_BOLD)
    body.addstr(6, 5, "PASSWORD  :", curses.A_BOLD)

    server_ip = curses.newwin(1, 16, header_h + 2, 20)
    username = curses.newwin(1, 16, header_h + 4, 20)
    password = curses.newwin(1, 16, header_h + 6, 20)

    server_ip.bkgd(" ", curses.color_pair(15))
    username.bkgd(" ", curses.color_pair(15))
    password.bkgd(" ", curses.color_pair(15))

    statusbar = curses.newwin(1, w, h, 0)
    statusbar.bkgd(" ", curses.color_pair(14))
    statusbar.addstr("\t Message | STATUS BAR")


    def refresh_all():
        screen.refresh()
        header.refresh()
        header_inner.refresh()
        body.refresh()
        statusbar.refresh()
        password.refresh()
        username.refresh()
        server_ip.refresh()
    
    refresh_all()
    
    def animation():
        counter = 0
        while True:
            counter = (counter + 1) % 7
            header_inner.clear()
            header_inner.refresh()
            if counter % 2 == 0:
                # header_inner.addstr(ascii_art, curses.A_BOLD | curses.color_pair(counter + 1))
                draw_art(header_inner, w, ascii_art, curses.A_BOLD | curses.color_pair(counter + 1))
            else:
                # header_inner.addstr(ascii_art1, curses.A_BOLD | curses.color_pair(counter + 1))
                draw_art(header_inner, w, ascii_art, curses.A_BOLD | curses.color_pair(counter + 1))
            header_inner.refresh()
            refresh_all()
            time.sleep(0.5)

    # t = threading.Thread(target=animation)
    # t.daemon = True
    # t.start()

    while True:
        server_ip_input = Textbox(server_ip)
        server_ip_input.edit()
        username.refresh()

    
        # username_ = Textbox(username)
        # username_.edit()
        # password.refresh()
        # password_ = Textbox(password)
        # password_.edit()

if __name__ == "__main__":
    curses.wrapper(main)