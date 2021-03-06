from talon import Context, Module, actions

key = actions.key
edit = actions.edit
user = actions.user

mod = Module()
ctx = Context()


@ctx.action_class("edit")
class EditActions:
    def word_left():
        key("ctrl-left")

    def word_right():
        key("ctrl-right")

    def select_word():
        edit.right()
        edit.word_left()
        edit.extend_word_right()
        text = edit.selected_text()
        text_trim = text.rstrip()
        for _ in range(len(text) - len(text_trim)):
            edit.extend_left()

    def extend_word_left():
        key("ctrl-shift-left")

    def extend_word_right():
        key("ctrl-shift-right")

    def delete_word():
        edit.select_word()
        edit.delete()


@mod.action_class
class Actions:
    def select_word_left():
        """Select word to the left"""
        edit.word_left()
        edit.extend_word_right()

    def select_word_right():
        """Select word to the right"""
        edit.word_right()
        edit.extend_word_left()

    def cut_word():
        """Cut word under cursor"""
        edit.select_word()
        edit.cut()

    def copy_word():
        """Copy word under cursor"""
        edit.select_word()
        edit.copy()

    def paste_word():
        """Paste to word under cursor"""
        edit.select_word()
        edit.paste()

    def delete_word_left():
        """Delete word to the left"""
        user.select_word_left()
        actions.sleep("50ms")
        edit.delete()

    def delete_word_right():
        """Delete word to the right"""
        user.select_word_right()
        actions.sleep("50ms")
        edit.delete()
