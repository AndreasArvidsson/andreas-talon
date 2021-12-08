from talon import Context, Module, actions, clip
import re

key = actions.key
edit = actions.edit
user = actions.user

mod = Module()
ctx = Context()
ctx_no_terminal = Context()

ctx_no_terminal.matches = r"""
not tag: terminal
"""


@ctx_no_terminal.action_class("main")
class MainActions:
    def insert(text: str):
        if not text:
            return
        if isinstance(text, str) and len(text) > 2 and re.search(r"[ /-]|\n", text):
            if paste_text(text):
                return
        actions.next(text)


@ctx.action_class("edit")
class EditActions:
    # ----- Navigation -----
    def up():
        key("up")

    def down():
        key("down")

    def left():
        key("left")

    def right():
        key("right")

    def page_up():
        key("pageup")

    def page_down():
        key("pagedown")

    # ----- Selection -----
    def select_none():
        key("right")

    def extend_up():
        key("shift-up")

    def extend_down():
        key("shift-down")

    def extend_left():
        key("shift-left")

    def extend_right():
        key("shift-right")

    # ----- Save -----
    def save():
        key("ctrl-s")

    # ----- Delete, Undo, Redo -----
    def delete():
        key("backspace")

    def undo():
        key("ctrl-z")

    def redo():
        key("ctrl-y")

    # ----- Cut, Copy, Paste -----
    def cut():
        key("ctrl-x")

    def copy():
        key("ctrl-c")

    def paste():
        key("ctrl-v")

    def paste_match_style():
        key("ctrl-shift-v")

    # ----- Indent -----
    def indent_less():
        key("home delete")

    def indent_more():
        key("home tab")

    # ----- Find -----
    def find(text: str = None):
        key("ctrl-f")
        if text:
            actions.insert(text)

    def find_previous():
        key("shift-f3")

    def find_next():
        key("f3")

    # ----- Zoom -----
    def zoom_in():
        key("ctrl-+")

    def zoom_out():
        key("ctrl--")

    def zoom_reset():
        key("ctrl-0")

    # ----- Miscellaneous -----
    def selected_text() -> str:
        with clip.capture() as s:
            edit.copy()
        try:
            return s.get()
        except clip.NoChange:
            return ""


@mod.action_class
class Actions:
    def up(n: int):
        """Move cursor up <n> rows"""
        for _ in range(n):
            edit.up()

    def down(n: int):
        """Move cursor down <n> rows"""
        for _ in range(n):
            edit.down()

    def left(n: int):
        """Move cursor left <n> columns"""
        for _ in range(n):
            edit.left()

    def right(n: int):
        """Move cursor right <n> columns"""
        for _ in range(n):
            edit.right()

    def delete_right():
        """Delete character to the right"""
        key("delete")


def paste_text(text: str):
    """Pastes text and preserves clipboard"""
    with clip.revert():
        clip.set_text(text)

        if clip.text() != text:
            user.notify("Failed to set clipboard")
            print(f"Clipboard: '{clip.text()}'")
            return False

        edit.paste()
        # sleep here so that clip.revert doesn't revert the clipboard too soon
        actions.sleep("150ms")
    return True
