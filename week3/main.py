import curses
from curses import wrapper

from editor import Editor
from command import (
    UndoCammand,
    QuitCommand,
    CalculateCommand,
    CommandHistory,
    DeleteCommand,
)

stdscr = curses.initscr()


class Calculator:
    ERR_MSG = "Invalid Syntax"

    def __init__(self, editor: Editor, history: CommandHistory):
        self.editor = editor
        self.history = history
        self.__add_manual()

    def run(self):
        while True:
            try:
                c = self.editor.strscr.getkey()
                if c == "q":
                    QuitCommand.execute()
                elif c in ("KEY_BACKSPACE", "\b", "\x7f"):
                    self.delete = DeleteCommand.execute(self.editor)
                    continue
                elif c in ("KEY_ENTER", "\n", "\r"):
                    CalculateCommand.execute(self.editor, self.history)
                elif c == "u":
                    if len(self.history.snapshots) > 0:
                        self.editor = UndoCammand.execute(self.editor, self.history)
                else:
                    self.editor.strscr.addstr(self.editor.ny, self.editor.x, str(c))
                    self.editor.strscr.move(self.editor.ny, self.editor.x + 1)
                    self.editor.x += 1
                    self.editor.text += c
                self.editor.strscr.refresh()
            except Exception as e:
                self.editor.strscr.addstr(self.editor.ny, 0, self.ERR_MSG)
                self.editor.x = len(self.ERR_MSG)
                self.editor.strscr.move(self.editor.ny, self.editor.x)
                self.editor.strscr.refresh()
                continue

    def __add_manual(self):
        self.editor.strscr.addstr(0, 0, "Press 'q' to quit")
        self.editor.strscr.addstr(1, 0, "Press 'backspace' to delete")
        self.editor.strscr.addstr(2, 0, "Press 'enter' to calculate")
        self.editor.strscr.addstr(3, 0, "Press 'u' to undo")
        self.editor.init_cursor()


def main(stdscr):
    history = CommandHistory()
    editor = Editor(stdscr)
    app = Calculator(editor, history)
    app.run()


wrapper(main)
