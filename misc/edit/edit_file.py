from talon import Context, Module, actions

key = actions.key
edit = actions.edit
user = actions.user

mod = Module()
ctx = Context()


@ctx.action_class("edit")
class EditActions:
    def file_start():
        key("ctrl-home")

    def file_end():
        key("ctrl-end")

    def select_all():
        key("ctrl-a")

    def extend_file_start():
        key("shift-ctrl-home")

    def extend_file_end():
        key("shift-ctrl-end")


@mod.action_class
class Actions:
    def cut_all():
        """Cut all text in the current document"""
        edit.select_all()
        edit.cut()

    def copy_all():
        """Copy all text in the current document"""
        edit.select_all()
        edit.copy()
        edit.select_none()

    def paste_all():
        """Paste to the current document"""
        edit.select_all()
        edit.paste()

    def delete_all():
        """Delete all text in the current document"""
        edit.select_all()
        edit.delete()
