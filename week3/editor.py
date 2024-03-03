from snapshot import Snapshot


class Editor:
    def __init__(self, stdscr):
        self.strscr = stdscr
        stdscr.clear()

        maxyx = stdscr.getmaxyx()
        self.x = 0
        self.y = 0
        self.nx = maxyx[1] - 1
        self.ny = maxyx[0] - 1
        self.init_cursor()
        self.text = ""

    def set_text(self, text):
        self.text = text

    def set_cursor(self, cursor):
        x, y = cursor
        self.x = x
        self.y = y

    def init_cursor(self):
        self.strscr.move(self.ny, 0)

    def create_snapshot(self):
        return Snapshot(self, self.x, self.y, self.text)
