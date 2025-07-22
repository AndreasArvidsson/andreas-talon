from talon import Context, Module, actions

mod = Module()
ctx = Context()


@ctx.action_class("edit")
class EditActions:
    def word_left():
        actions.key("ctrl-left")

    def word_right():
        actions.key("ctrl-right")

    def select_word():
        actions.edit.right()
        actions.edit.word_left()
        actions.edit.extend_word_right()
        text = actions.edit.selected_text()
        text_trim = text.rstrip()
        for _ in range(len(text) - len(text_trim)):
            actions.edit.extend_left()

    def extend_word_left():
        actions.key("ctrl-shift-left")

    def extend_word_right():
        actions.key("ctrl-shift-right")

    def delete_word():
        actions.edit.select_word()
        actions.edit.delete()


@mod.action_class
class Actions:
    def select_containing_word_if_empty():
        """Select the word under the cursor if no text is selected"""
        if actions.edit.selected_text() == "":
            actions.edit.select_word()

    def select_word_left():
        """Select word to the left"""
        actions.edit.word_left()
        actions.edit.extend_word_right()

    def select_word_right():
        """Select word to the right"""
        actions.edit.word_right()
        actions.edit.extend_word_left()

    def cut_word():
        """Cut word under cursor"""
        actions.edit.select_word()
        actions.edit.cut()

    def copy_word():
        """Copy word under cursor"""
        actions.edit.select_word()
        actions.edit.copy()

    def paste_word():
        """Paste to word under cursor"""
        actions.edit.select_word()
        actions.edit.paste()

    def delete_word_left():
        """Delete word to the left"""
        actions.user.select_word_left()
        actions.sleep("50ms")
        actions.edit.delete()

    def delete_word_right():
        """Delete word to the right"""
        actions.user.select_word_right()
        actions.sleep("50ms")
        actions.edit.delete()
