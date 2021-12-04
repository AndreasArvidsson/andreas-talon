from talon import Context, Module, actions

ctx = Context()
mod = Module()


@ctx.action_class("edit")
class EditActions:
    def paragraph_start():
        if extend_paragraph_start():
            actions.edit.left()

    def paragraph_end():
        if extend_paragraph_end():
            actions.edit.right()

    def extend_paragraph_start():
        extend_paragraph_start()

    def extend_paragraph_end():
        extend_paragraph_end()

    def select_paragraph():
        if is_line_empty():
            return
        # Search for start of paragraph
        actions.edit.extend_paragraph_start()
        actions.edit.left()

        # Extend to end of paragraph
        actions.edit.extend_paragraph_end()


def is_line_empty():
    actions.edit.extend_line_start()
    text = actions.edit.selected_text().strip()
    if text:
        actions.edit.right()
        return False
    actions.edit.extend_line_end()
    text = actions.edit.selected_text().strip()
    if text:
        actions.edit.left()
        return False
    return True


def extend_paragraph_start() -> bool:
    actions.edit.extend_line_start()
    text = actions.edit.selected_text()
    length = len(text)
    while True:
        actions.edit.extend_up()
        actions.edit.extend_line_start()
        text = actions.edit.selected_text()
        new_length = len(text)
        if new_length == length:
            break
        line = text[: new_length - length].strip()
        if not line:
            actions.edit.extend_down()
            break
        length = new_length
    return text.strip() != ""


def extend_paragraph_end() -> bool:
    actions.edit.extend_line_end()
    text = actions.edit.selected_text()
    length = len(text)
    while True:
        actions.edit.extend_down()
        actions.edit.extend_line_end()
        text = actions.edit.selected_text()
        new_length = len(text)
        if new_length == length:
            break
        line = text[length:].strip()
        if not line:
            actions.edit.extend_line_start()
            actions.edit.extend_left()
            break
        length = new_length
    return text.strip() != ""
