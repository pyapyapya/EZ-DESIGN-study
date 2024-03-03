from abc import abstractmethod

from snapshot import Snapshot, CommandHistory
from editor import Editor


class Command:
    @abstractmethod
    def execute(self):
        pass

    def save(self):
        pass


class QuitCommand(Command):
    @classmethod
    def execute(cls):
        exit()


class InsertCommand(Command):
    @classmethod
    def execute(cls, editor: Editor, c: str):
        editor.strscr.addstr(editor.ny, editor.x, str(c))
        editor.strscr.move(editor.ny, editor.x + 1)
        editor.x += 1
        editor.text += c


class DeleteCommand(Command):
    @classmethod
    def execute(cls, editor: Editor):
        editor.x -= 1
        editor.strscr.addstr(editor.ny, editor.x, " ")
        editor.strscr.move(editor.ny, editor.x)
        editor.text = editor.text[:-1]


class CalculateCommand(Command):
    @classmethod
    def execute(cls, editor: Editor, history: CommandHistory):
        result = str(float(eval(editor.text)))
        history.snapshots.append(editor.create_snapshot())
        editor.y += 1
        editor.x = 0
        editor.strscr.addstr(editor.y, editor.nx - len(editor.text), editor.text)
        editor.strscr.move(editor.ny, len(result))
        editor.strscr.clrtoeol()
        editor.strscr.addstr(editor.ny, editor.x, result)
        editor.x = len(result)
        editor.text = result


class UndoCommand(Command):
    @classmethod
    def execute(cls, editor: Editor, history: CommandHistory) -> Editor:
        snapshot: Snapshot = history.pop()
        editor: Editor = snapshot.restore(editor)
        editor.strscr.move(len(history.snapshots) + 1, editor.nx - len(editor.text))
        editor.strscr.clrtoeol()
        editor.strscr.move(editor.ny, 0)
        editor.strscr.clrtoeol()
        editor.strscr.addstr(editor.ny, 0, editor.text)
        return editor


class ErrorCommand(Command):
    @classmethod
    def execute(cls, editor: Editor) -> Editor:
        editor.strscr.addstr(editor.ny, 0, "Invalid Syntax")
        editor.x = len("Invalid Syntax")
        editor.strscr.move(editor.ny, editor.x)
        editor.strscr.refresh()
        return editor
