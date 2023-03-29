from talon import Context, Module, actions


mod = Module()

mod.apps.windows_explorer = """
os: windows
and app.name: Windows Explorer
os: windows
and app.exe: explorer.exe
"""

# many commands should work in most save/open dialog.
# note the "show options" stuff won"t work unless work
# unless the path is displayed in the title, which is rare for those
mod.apps.windows_file_browser = """
os: windows
title: /(Save|Open|Browse|Select|Install from|File Upload)/
"""

ctx = Context()
ctx.matches = """
app: windows_explorer
app: windows_file_browser
"""


@ctx.action_class("edit")
class EditActions:
    def file_start():
        actions.key("home")

    def file_end():
        actions.key("end")


@ctx.action_class("user")
class UserActions:
    # ----- Tabs -----
    def tab_duplicate():
        actions.user.file_manager_focus_address()
        address = actions.edit.selected_text()
        actions.sleep("50ms")
        actions.app.tab_open()
        actions.sleep("100ms")
        actions.user.file_manager_go(address)

    # ----- Navigation -----

    def go_back():
        actions.key("alt-left")

    def go_forward():
        actions.key("alt-right")

    def file_manager_go_parent():
        actions.key("alt-up")

    def file_manager_go_home():
        actions.user.file_manager_go(
            actions.user.user_home(),
        )

    def file_manager_focus_address():
        actions.key("alt-d")

    def file_manager_copy_address():
        actions.user.file_manager_focus_address()
        actions.edit.copy()
        actions.key("escape")

    def file_manager_go(path: str):
        actions.key("ctrl-l")
        actions.insert(path)
        actions.key("enter")

    # ----- Create folders / files -----

    def file_manager_new_folder(name: str = None):
        actions.key("home")
        actions.key("ctrl-shift-n")
        if name:
            actions.insert(name)

    def file_manager_new_file(name: str = None):
        actions.key("shift-f10 w t")
        if name:
            actions.insert(name)

    # ----- Miscellaneous -----

    def file_manager_show_properties():
        actions.key("alt-enter")

    def file_manager_terminal_here():
        actions.key("ctrl-l")
        actions.insert("cmd.exe")
        actions.key("enter")

    def pick_item(number: int):
        if number == 1:
            actions.key("space enter")
        else:
            actions.next(number)


@mod.action_class
class Actions:
    def select_up():
        """Move selection up"""
        actions.key("ctrl-up")

    def select_down():
        """Move selection down"""
        actions.key("ctrl-down")

    def select_toggle():
        """Toggle selection"""
        actions.key("ctrl-space")
