from talon import Context, Module, actions, app

key = actions.key
insert = actions.insert

mod = Module()

mod.apps.nautilus = """
os: linux
and app.name: Org.gnome.Nautilus
"""

ctx = Context()
ctx.matches = """
app: nautilus
"""

ctx.tags = ["user.file_manager", "user.tabs"]


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        key(f"ctrl-{number}")

    def go_back():
        key("alt-left")

    def go_forward():
        key("alt-right")

    def file_manager_go_parent():
        key("alt-up")

    def file_manager_focus_address():
        key("ctrl-l")

    def file_manager_show_properties():
        key("ctrl-i")

    def file_manager_copy_address():
        actions.user.file_manager_focus_address()
        actions.edit.copy()
        key("escape")

    def file_manager_open_directory(path: str):
        key("ctrl-l")
        insert(path)
        key("enter")

    def file_manager_new_folder(name: str = None):
        key("ctrl-shift-n")
        if name:
            insert(name)

    def pick_item(index: int):
        actions.next(index + 1)
