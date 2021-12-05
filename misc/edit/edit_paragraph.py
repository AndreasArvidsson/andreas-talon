from talon import Context, Module, actions

key = actions.key
edit = actions.edit
user = actions.user

ctx = Context()
mod = Module()


@ctx.action_class("edit")
class EditActions:
    def paragraph_start():
        if extend_paragraph_start():
            edit.left()

    def paragraph_end():
        if extend_paragraph_end():
            edit.right()

    def select_paragraph():
        if is_line_empty():
            return
        # Search for start of paragraph
        edit.extend_paragraph_start()
        edit.left()
        # Extend to end of paragraph
        edit.extend_paragraph_end()

    def extend_paragraph_start():
        extend_paragraph_start()

    def extend_paragraph_end():
        extend_paragraph_end()

    def delete_paragraph():
        edit.select_paragraph()
        edit.delete()
        edit.delete()
        edit.delete_line()


@mod.action_class
class Actions:
    def cut_paragraph():
        """Cut paragraph under the cursor"""
        edit.select_paragraph()
        edit.cut()

    def copy_paragraph():
        """Copy paragraph under the cursor"""
        edit.select_paragraph()
        edit.copy()


def is_line_empty():
    edit.extend_line_start()
    text = edit.selected_text().strip()
    if text:
        edit.right()
        return False
    edit.extend_line_end()
    text = edit.selected_text().strip()
    if text:
        edit.left()
        return False
    return True


def extend_paragraph_start() -> bool:
    edit.extend_line_start()
    text = edit.selected_text()
    length = len(text)
    while True:
        edit.extend_up()
        edit.extend_line_start()
        text = edit.selected_text()
        new_length = len(text)
        if new_length == length:
            break
        line = text[: new_length - length].strip()
        if not line:
            edit.extend_down()
            break
        length = new_length
    return text.strip() != ""


def extend_paragraph_end() -> bool:
    edit.extend_line_end()
    text = edit.selected_text()
    length = len(text)
    while True:
        edit.extend_down()
        edit.extend_line_end()
        text = edit.selected_text()
        new_length = len(text)
        if new_length == length:
            break
        line = text[length:].strip()
        if not line:
            edit.extend_line_start()
            edit.extend_left()
            break
        length = new_length
    return text.strip() != ""
