import curses
from curses import wrapper

from editor import Editor
from command import (
    UndoCommand,
    QuitCommand,
    CalculateCommand,
    CommandHistory,
    DeleteCommand,
    InsertCommand,
    ErrorCommand,
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
                    DeleteCommand(self.editor, c, self.history).execute()
                    continue
                elif c in ("KEY_ENTER", "\n", "\r"):
                    CalculateCommand(self.editor, self.history).execute()
                elif c == "u":
                    if len(self.history.snapshots) > 0:
                        UndoCommand(self.editor, self.history).execute()
                else:
                    InsertCommand(self.editor, c, self.history).execute()
                self.editor.strscr.refresh()
            except Exception as e:
                ErrorCommand(self.editor, self.history).execute()
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
