class Snapshot:
    def __init__(self, editor, x, y, text):
        self.editor = editor
        self.cursor = (x, y)
        self.text = text

    def restore(self, editor):
        editor.set_cursor(self.cursor)
        editor.set_text(self.text)
        return editor


class CommandHistory:
    def __init__(self):
        self.snapshots: list[Snapshot] = []

    def push(self, snapshot):
        self.snapshots.append(snapshot)

    def pop(self) -> Snapshot:
        return self.snapshots.pop()
