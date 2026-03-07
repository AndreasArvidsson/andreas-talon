from talon import Module, Context, actions


mod = Module()
mod.tag("bash")

ctx = Context()

ctx.matches = r"""
tag: user.bash
"""


@ctx.action_class("user")
class UserActions:
    def go_back():
        actions.insert("cd $OLDPWD\n")

    def go_forward():
        actions.insert("cd $OLDPWD\n")

    def file_manager_go_parent():
        actions.user.file_manager_go("..")

    def file_manager_go_home():
        actions.user.file_manager_go("~")

    def file_manager_focus_address():
        actions.skip()

    def file_manager_copy_address():
        actions.insert("pwd | clipboard\n")

    @staticmethod
    def file_manager_go(path: str):
        path = path.replace(" ", "\\ ")
        actions.insert(f"cd {path}")
        actions.key("enter")

    # ----- Create folders / files -----
    @staticmethod
    def file_manager_new_folder(name: str = ""):
        actions.insert(f"mkdir {name}")

    @staticmethod
    def file_manager_new_file(name: str = ""):
        actions.insert(f"touch {name}")
