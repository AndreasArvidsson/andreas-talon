from talon import Context, Module, actions

key = actions.key
insert = actions.insert

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
        key("home")

    def file_end():
        key("end")


@ctx.action_class("user")
class UserActions:
    def go_back():
        key("alt-left")

    def go_forward():
        key("alt-right")

    def file_manager_go_parent():
        key("alt-up")

    def file_manager_focus_address():
        key("alt-d")

    def file_manager_copy_address():
        actions.user.file_manager_focus_address()
        actions.edit.copy()
        key("escape")

    def file_manager_go(path: str):
        key("ctrl-l")
        insert(path)
        key("enter")

    # ----- Create folders / files -----
    def file_manager_new_folder(name: str = None):
        key("home")
        key("ctrl-shift-n")
        if name:
            insert(name)

    def file_manager_new_file(name: str = None):
        key("shift-f10 w t")
        if name:
            insert(name)

    # ----- Miscellaneous -----
    def file_manager_show_properties():
        key("alt-enter")

    def file_manager_terminal_here():
        key("ctrl-l")
        insert("cmd.exe")
        key("enter")

    def pick_item(number: int):
        if number == 1:
            key("space enter")
        else:
            actions.next(number)


@mod.action_class
class Actions:
    def select_up():
        """Move selection up"""
        key("ctrl-up")

    def select_down():
        """Move selection down"""
        key("ctrl-down")

    def select_toggle():
        """Toggle selection"""
        key("ctrl-space")


# ----- Windows explorer application only, no file browser -----

ctx_no_browser = Context()
ctx_no_browser.matches = """
app: windows_explorer
"""


@ctx_no_browser.action_class("edit")
class EditActions:
    def delete():
        key("delete")
