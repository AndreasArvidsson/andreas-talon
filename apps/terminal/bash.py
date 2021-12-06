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
    def go_back():
        insert("cd $OLDPWD\n")

    def go_forward():
        insert("cd $OLDPWD\n")

    def file_manager_go_parent():
        user.file_manager_open_directory("..")

    def file_manager_focus_address():
        actions.skip()

    def file_manager_copy_address():
        insert("pwd | clipboard\n")

    def file_manager_open_directory(path: str):
        path = path.replace(" ", "\\ ")
        insert(f"cd {path}")
        key("enter")

    # ----- Create folders / files -----
    def file_manager_new_folder(name: str = None):
        insert(f"mkdir {name or ''}")

    def file_manager_new_file(name: str = None):
        insert(f"touch {name or ''}")


@mod.action_class
class Actions:
    def tail_talon_log():
        """Tail Talon log file"""
        python = f"{user.talon_app()}/venv_bin/posix/python"
        python_updated = python.replace(" ", "\\ ")
        tail = f"{user.talon_app()}/tail.py"
        tail_updated = tail.replace(" ", "\\ ")
        file = f"{user.talon_home()}/talon.log"
        file_updated = file.replace(" ", "\\ ")
        actions.insert(f"{python_updated} {tail_updated} {file_updated}\n")
