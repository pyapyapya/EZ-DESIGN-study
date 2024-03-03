from abc import abstractmethod

from snapshot import CommandHistory
from editor import Editor


class Command:
    def __init__(self, editor: Editor, history: CommandHistory = None):
        self.editor = editor
        self.history = history

    @abstractmethod
    def execute(self):
        pass

    def save_snapshot(self):
        if self.history:
            self.history.push(self.editor.create_snapshot())

    def undo(self) -> Editor:
        return self.history.pop().restore(self.editor)


class QuitCommand(Command):
    @staticmethod
    def execute():
        exit()


class InsertCommand(Command):
    def __init__(self, editor: Editor, c: str, history: CommandHistory = None):
        super().__init__(editor, history)
        self.c = c

    def execute(self):
        self.editor.strscr.addstr(self.editor.ny, self.editor.x, str(self.c))
        self.editor.strscr.move(self.editor.ny, self.editor.x + 1)
        self.editor.x += 1
        self.editor.text += self.c


class DeleteCommand(Command):
    def __init__(self, editor: Editor, c: str, history: CommandHistory = None):
        super().__init__(editor, history)
        self.c = c

    def execute(self):
        self.editor.x -= 1
        self.editor.strscr.addstr(self.editor.ny, self.editor.x, " ")
        self.editor.strscr.move(self.editor.ny, self.editor.x)
        self.editor.text = self.editor.text[:-1]


class CalculateCommand(Command):
    def __init__(self, editor: Editor, history: CommandHistory = None):
        super().__init__(editor, history)

    def execute(self):
        result = str(float(eval(self.editor.text)))
        self.save_snapshot()
        self.editor.y += 1
        self.editor.x = 0
        self.editor.strscr.addstr(
            self.editor.y, self.editor.nx - len(self.editor.text), self.editor.text
        )
        self.editor.strscr.move(self.editor.ny, len(result))
        self.editor.strscr.clrtoeol()
        self.editor.strscr.addstr(self.editor.ny, self.editor.x, result)
        self.editor.x = len(result)
        self.editor.text = result


class UndoCommand(Command):
    def __init__(self, editor: Editor, history: CommandHistory = None):
        super().__init__(editor, history)

    def execute(self):
        self.editor = self.undo()
        self.editor.strscr.move(
            len(self.history.snapshots) + 1, self.editor.nx - len(self.editor.text)
        )
        self.editor.strscr.clrtoeol()
        self.editor.strscr.move(self.editor.ny, 0)
        self.editor.strscr.clrtoeol()
        self.editor.strscr.addstr(self.editor.ny, 0, self.editor.text)


class ErrorCommand(Command):
    def __init__(self, editor: Editor, history: CommandHistory = None):
        super().__init__(editor, history)

    def execute(self) -> Editor:
        self.editor.strscr.addstr(self.editor.ny, 0, "Invalid Syntax")
        self.editor.x = len("Invalid Syntax")
        self.editor.strscr.move(self.editor.ny, self.editor.x)
        self.editor.strscr.refresh()
        self.editor.strscr.clrtoeol()
