from talon import Context, Module, actions, clip

mod = Module()
ctx = Context()


@ctx.action_class("edit")
class EditActions:
    # ----- Navigation -----
    def up():
        actions.key("up")

    def down():
        actions.key("down")

    def left():
        actions.key("left")

    def right():
        actions.key("right")

    def page_up():
        actions.key("pageup")

    def page_down():
        actions.key("pagedown")

    # ----- Selection -----
    def select_none():
        actions.key("right")

    def extend_up():
        actions.key("shift-up")

    def extend_down():
        actions.key("shift-down")

    def extend_left():
        actions.key("shift-left")

    def extend_right():
        actions.key("shift-right")

    def selection_clone():
        text = actions.edit.selected_text()
        actions.edit.select_none()
        actions.insert(text)

    # ----- Save -----
    def save():
        actions.key("ctrl-s")

    # ----- Delete, Undo, Redo -----
    def delete():
        actions.key("backspace")

    def undo():
        actions.key("ctrl-z")

    def redo():
        actions.key("ctrl-y")

    # ----- Cut, Copy, Paste -----
    def cut():
        actions.key("ctrl-x")

    def copy():
        actions.key("ctrl-c")

    def paste():
        actions.key("ctrl-v")
        actions.sleep("30ms")

    def paste_match_style():
        actions.key("ctrl-shift-v")

    # ----- Indent -----
    def indent_less():
        actions.key("home delete")

    def indent_more():
        actions.key("home tab")

    # ----- Find -----
    def find(text: str = None):
        actions.key("ctrl-f")
        if text:
            actions.insert(text)

    def find_previous():
        actions.key("shift-f3")

    def find_next():
        actions.key("f3")

    # ----- Zoom -----
    def zoom_in():
        actions.key("ctrl-+")

    def zoom_out():
        actions.key("ctrl--")

    def zoom_reset():
        actions.key("ctrl-0")

    # ----- Miscellaneous -----
    def selected_text() -> str:
        with clip.capture(0.1) as c:
            actions.edit.copy()
        try:
            return c.text()
        except clip.NoChange:
            return ""


@mod.action_class
class Actions:
    def insert_with_padding(text: str):
        """Insert <text> with padding"""
        if text[0].isspace() or text[-1].isspace():
            before, after = actions.user.dictation_get_context()

            # At start of line or has leading whitespace
            if before is not None and (len(before) == 0 or before[-1].isspace()):
                text = text.lstrip()

            # Has trailing whitespace
            # Disabled for now because it's too annoying
            # if after is not None and len(after) != 0 and after[0].isspace():
            #     text = text.rstrip()

        actions.insert(text)

    def delete_right():
        """Delete character to the right"""
        actions.key("delete")

    def insert_arrow():
        """Insert arrow symbol"""
        actions.insert(" => ")

    def insert_symbol_and_break_at_end(symbol: str):
        """Add <symbol> at end of line and then insert line below"""
        actions.edit.line_end()
        actions.key(symbol)
        actions.edit.line_insert_down()

    def paste_text(text: str):
        """Pastes <text> and preserves clipboard"""
        with clip.revert():
            clip.set_text(text)
            actions.edit.paste()

    def insert_clipboard_with_keys():
        """Insert clipboard content by key presses"""
        text = actions.clip.text()
        for c in text:
            actions.key(c)

    def edit_text_file(path: str):
        """Edit text file <path>"""
        actions.user.exec(f"code {path}")

    # ----- Cut, copy, paste -----
    def edit_cut():
        """Cut selection to clipboard"""
        actions.edit.cut()

    def edit_copy():
        """Copy selection to clipboard"""
        actions.edit.copy()

    def edit_paste(expand: bool):
        """Paste clipboard at cursor"""
        actions.edit.paste()
