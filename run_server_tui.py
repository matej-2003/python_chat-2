from chat_server import ChatServerTUI
import curses

def main(screen):
    app = ChatServerTUI(screen)
    app.start()

if __name__ == '__main__':
    curses.wrapper(main)