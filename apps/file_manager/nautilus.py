from talon import Context, Module, actions

mod = Module()

mod.apps.nautilus = r"""
os: linux
and app.name: Org.gnome.Nautilus
"""

ctx = Context()
ctx.matches = r"""
app: nautilus
"""

ctx.tags = ["user.file_manager", "user.tabs"]


@ctx.action_class("user")
class UserActions:
    def file_manager_go_parent():
        actions.key("alt-up")

    def file_manager_focus_address():
        actions.key("ctrl-l")

    def file_manager_show_properties():
        actions.key("ctrl-i")

    def file_manager_copy_address():
        actions.user.file_manager_focus_address()
        actions.edit.copy()
        actions.key("escape")

    @staticmethod
    def file_manager_go(path: str):
        actions.key("ctrl-l")
        actions.insert(path)
        actions.key("enter")

    @staticmethod
    def file_manager_new_folder(name: str = ""):
        actions.key("ctrl-shift-n")
        if name:
            actions.insert(name)

    @staticmethod
    def pick_item(number: int):
        actions.next(number + 1)
