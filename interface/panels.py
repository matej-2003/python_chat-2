import curses
from curses import ascii
import time
import string

sl_lang = {
    161: "š",
    141: "č",
    135: "ć",
    190: "ž",
    145: "đ",
}

char_codes = [ord(i) for i in string.printable]

def main(screen):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE)
    # pad = curses.newpad(100, 100)
    # for y in range(0, 99):
    #     for x in range(0, 99):
    #         pad.addch(y,x, ord('a') + (x*x+y*y) % 26)

    screen.refresh()
    # pad.refresh( 0,0, 5,5, 20,75)
    # screen.attron(curses.color_pair(1))
    txt = "".join(["\n line {i}" for i in range(10)])
    screen.addstr("\n\n\n\ntest", curses.color_pair(1))

    line_n = 0
    screen.scrollok(True)
    screen.scroll(10)

    while True:
        # screen.refresh()
        c = screen.getch()
        # screen.addstr(10, 10, f"{c}{chr(c)} Š:{ord('š')}")
        
        # if c in char_codes:
        #     screen.addstr(chr(c))
        # if c in sl_lang.keys():
        #     screen.addstr(sl_lang[c])
        # if c == curses.KEY_BACKSPACE:
        #     screen.addstr("\b \b")
        # if c == ascii.DEL:
        #     screen.addstr(" ")
        if c == curses.KEY_DOWN:
            # line_n += 1
            screen.scroll(1)
        if c == curses.KEY_UP:
            # line_n -= 1
            screen.scroll(-1)
        elif c == ord('q'):
            break
        elif c == curses.KEY_HOME:
            x = y = 0

if __name__ == '__main__':
    curses.wrapper(main)