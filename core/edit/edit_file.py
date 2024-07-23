from talon import Context, Module, actions

mod = Module()
ctx = Context()


@ctx.action_class("edit")
class EditActions:
    def file_start():
        actions.key("ctrl-home")

    def file_end():
        actions.key("ctrl-end")

    def select_all():
        actions.key("ctrl-a")

    def extend_file_start():
        actions.key("shift-ctrl-home")

    def extend_file_end():
        actions.key("shift-ctrl-end")

    # This is some stuff I added
    def delete_all():
        actions.edit.select_all()
        actions.edit.delete()


@mod.action_class
class Actions:
    def cut_all():
        """Cut all text in the current document"""
        actions.edit.select_all()
        actions.edit.cut()

    def copy_all():
        """Copy all text in the current document"""
        actions.edit.select_all()
        actions.edit.copy()
        actions.edit.select_none()

    def paste_all():
        """Paste to the current document"""
        actions.edit.select_all()
        actions.edit.paste()
