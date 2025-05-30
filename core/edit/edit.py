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
        actions.edit.right()
        actions.insert(f" {text}")

    # ----- Save -----
    def save():
        actions.key("ctrl-s")

    # ----- Delete, Undo, Redo -----
    def delete():
        actions.key("delete")

    def delete_left():
        actions.key("backspace")

    def delete_right():
        actions.key("delete")

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

    def insert_arrow():
        """Insert arrow symbol"""
        actions.insert(" => ")

    def insert_symbol_and_break_at_end(symbol: str):
        """Add <symbol> at end of line and then insert line below"""
        actions.edit.line_end()
        actions.key(symbol)
        actions.edit.line_insert_down()

    def paste_text(text: str):
        """Paste <text> and preserves clipboard"""
        with clip.revert():
            actions.user.clip_set_transient_text(text)
            actions.edit.paste()
            # sleep here so that clip.revert doesn't revert the clipboard too soon
            actions.sleep("100ms")

    def paste_clipboard_formatted(formatters: str):
        """Paste clipboard text formatted as <formatters>"""
        text = actions.clip.text()
        text = actions.user.reformat_text(text, formatters)
        actions.user.paste_text(text)

    def clip_set_transient_text(text: str):
        """Set clipboard text without monitoring"""
        mime = clip.MimeData()
        mime.text = text
        mime["ExcludeClipboardContentFromMonitorProcessing"] = b"true"
        clip.set_mime(mime)

    def insert_clipboard_with_keys():
        """Insert clipboard content by key presses"""
        text = actions.clip.text()
        for c in text:
            actions.key(c)

    def selection_clone_before():
        """Insert a copy of the current selection before the selection"""
        text = actions.edit.selected_text()
        actions.edit.left()
        actions.insert(f"{text} ")
        actions.edit.left()
