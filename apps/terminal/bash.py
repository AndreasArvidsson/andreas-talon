from talon import Module, Context, actions
key = actions.key
insert = actions.insert
user = actions.user

mod = Module()
mod.tag("bash")

ctx = Context()

ctx.matches = r"""
tag: user.bash
"""

@ctx.action_class("user")
class UserActions:
    def go_back():                      insert("cd $OLDPWD\n")
    def go_forward():                   insert("cd $OLDPWD\n")
    def file_manager_go_parent():       user.file_manager_open_directory("..")
    def file_manager_focus_address():   actions.skip()
    def file_manager_copy_address():    insert("pwd | clipboard\n")

    def file_manager_open_directory(path: str):
        path = path.replace(" ", "\\ ")
        insert(f"cd {path}")
        key("enter")

    # ----- Create folders / files -----
    def file_manager_new_folder(name: str = None):
        insert(f"mkdir {name or ''}")
    def file_manager_new_file(name: str = None):
        insert(f"touch {name or ''}")
