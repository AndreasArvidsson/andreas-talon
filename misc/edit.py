from talon import Context, Module, actions, clip
import re
key = actions.key
edit = actions.edit
user = actions.user

ctx = Context()
ctx_no_terminal = Context()
mod = Module()

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
    def up():                     key("up")
    def down():                   key("down")
    def left():                   key("left")
    def right():                  key("right")

    def file_start():             key("ctrl-home")
    def file_end():               key("ctrl-end")
    def line_start():             key("home")
    def line_end():               key("end")

    def word_left():              key("ctrl-left")
    def word_right():             key("ctrl-right")

    def page_up():                key("pageup")
    def page_down():              key("pagedown")

    # ----- Selection -----
    def select_all():             key("ctrl-a")

    def select_line(n: int = None):
        if n:
            edit.jump_line(n)
        key("end shift-home")

    def select_lines(a: int, b: int):
        number_of_lines = abs(a - b)
        if number_of_lines < 1 or number_of_lines > 500:
            return
        edit.jump_line(a)
        if a < b:
            for _ in range(number_of_lines):
                edit.extend_line_down()
            edit.extend_line_end()
        else:
            edit.line_end()
            for _ in range(number_of_lines):
                edit.extend_line_up()
            edit.extend_line_start()

    def select_none():            key("right")
    def select_word():            key("ctrl-left ctrl-shift-right")

    def extend_up():              key("shift-up")
    def extend_down():            key("shift-down")
    def extend_left():            key("shift-left")
    def extend_right():           key("shift-right")

    def extend_file_start():      key("shift-ctrl-home")
    def extend_file_end():        key("shift-ctrl-end")

    def extend_line_up():         key("shift-up")
    def extend_line_down():       key("shift-down")
    def extend_line_start():      key("shift-home")
    def extend_line_end():        key("shift-end")

    def extend_word_left():       key("ctrl-shift-left")
    def extend_word_right():      key("ctrl-shift-right")

    def line_insert_up():         key("home enter up")
    def line_insert_down():       key("end enter")

    # ----- Save -----
    def save():                   key("ctrl-s")

    # ----- Delete, undo, redo -----
    def delete():                 key("backspace")

    def delete_word():
        edit.select_word()
        edit.delete()

    def delete_line():
        user.clear_line()
        key("home delete")

    def undo():                 key("ctrl-z")
    def redo():                 key("ctrl-y")

    # ----- Copy, cut, paste -----
    def copy():                 key("ctrl-c")
    def cut():                  key("ctrl-x")
    def paste():                key("ctrl-v")

    def line_clone():
        user.copy_line()
        edit.line_insert_down()
        edit.paste()

    def line_swap_up():
        user.cut_line()
        edit.line_start()
        edit.paste()
        key("enter up")

    def line_swap_down():
        user.cut_line()
        key("down end enter")
        edit.paste()

    # ----- Indent -----
    def indent_less():          key("home delete")
    def indent_more():          key("home tab")

    # ----- Find -----
    def find(text: str = None):
        key("ctrl-f")
        if text:
            actions.insert(text)

    def find_previous():        key("shift-f3")
    def find_next():            key("f3")

    # ----- Zoom -----
    def zoom_in():              key("ctrl-+")
    def zoom_out():             key("ctrl--")
    def zoom_reset():           key("ctrl-0")

    def selected_text() -> str:
        with clip.capture() as s:
            edit.copy()
        try:
            return s.get()
        except clip.NoChange:
            return ""


@mod.action_class
class Actions:
    # ----- Navigation -----
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

    def word_left(n: int):
        """Move cursor left <n> words"""
        for _ in range(n):
            edit.word_left()

    def word_right(n: int):
        """Move cursor right <n> words"""
        for _ in range(n):
            edit.word_right()

    def line_start(n: int = None):
        """Move cursor to start of line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.line_start()

    def line_end(n: int = None):
        """Move cursor to end of line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.line_end()

    def line_middle(n: int = None):
        """Move cursor to middle of line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.select_line()
        text = edit.selected_text().strip()
        edit.right()
        for _ in range(round(len(text) / 2)):
            edit.left()

    def line_insert_down(n: int):
        """Insert <n> lines below cursor"""
        for _ in range(n):
            edit.line_insert_down()

    # ----- Selection -----
    def extend_up(n: int):
        """Extend selection up <n> rows"""
        for _ in range(n):
            edit.extend_up()

    def extend_down(n: int):
        """Extend selection down <n> rows"""
        for _ in range(n):
            edit.extend_down()

    def extend_left(n: int):
        """Extend selection left <n> columns"""
        for _ in range(n):
            edit.extend_left()

    def extend_right(n: int):
        """Extend selection right <n> columns"""
        for _ in range(n):
            edit.extend_right()

    def extend_word_left(n: int):
        """Extend selection left <n> words"""
        for _ in range(n):
            edit.extend_word_left()

    def extend_word_right(n: int):
        """Extend selection right <n> words"""
        for _ in range(n):
            edit.extend_word_right()

    def select_word_right():
        """Select word to the right"""
        key("ctrl-right ctrl-shift-left")

    def select_line_start():
        """Select start of line"""
        if edit.selected_text():
            edit.left()
        edit.extend_line_start()
    
    def select_line_end():
        """Select end of line"""
        if edit.selected_text():
            edit.right()
        edit.extend_line_end()

    # ----- Delete, undo, redo -----
    def delete_right():
        """Delete character to the right"""
        key("delete")

    def delete_word_right():
        """Delete word to the right"""
        user.select_word_right()
        edit.delete()

    def delete_line(n: int = None):
        """Delete line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.delete_line()

    def delete_line_start():
        """Delete start of current line"""
        edit.extend_line_start()
        edit.delete()

    def delete_line_end():
        """Delete end of current line"""
        edit.extend_line_end()
        edit.delete()

    def clear_line(n: int = None):
        """Clear line <n> or current"""
        if n:
            edit.jump_line(n)
        key("end shift-home space backspace")

    # ----- Copy, cut, paste -----
    def cut_word():
        """Cut word under cursor"""
        edit.select_word()
        edit.cut()

    def cut_line(n: int = None):
        """Cut line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.select_line()
        edit.cut()
        edit.delete()

    def cut_line_start():
        """Cut start of line"""
        edit.extend_line_start()
        edit.cut()

    def cut_line_end():
        """Cut end of line"""
        edit.extend_line_end()
        edit.cut()

    def copy_word():
        """Copy word under cursor"""
        edit.select_word()
        edit.copy()

    def copy_line(n: int = None):
        """Copy line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.select_line()
        edit.copy()

    def clone_line(n: int = None):
        """Clone line <n> or current"""
        if n:
            edit.jump_line(n)
        edit.line_clone()

    def copy_line_start():
        """Copy start of line"""
        edit.extend_line_start()
        edit.copy()
        edit.right()

    def copy_line_end():
        """Copy end of line"""
        edit.extend_line_end()
        edit.copy()
        edit.left()

    def line_swap_up(n: int):
        """Swap the current line with the line <n> lines above"""
        for _ in range(n):
            edit.line_swap_up()

    def line_swap_down(n: int):
        """Swap the current line with the line <n> lines below"""
        for _ in range(n):
            edit.line_swap_down()


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
