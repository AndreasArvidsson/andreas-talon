from talon import app, Module, Context, actions, app
from os import path, environ
from ....andreas.merge import merge

ctx = Context()
mod = Module()
mod.tag("file_manager", desc="Tag for enabling generic file management commands")
mod.list("path", desc="List of the users favorite paths")


@mod.action_class
class Actions:
    # ----- Navigation -----
    def file_manager_go_back():
        """File manager go back"""
    def file_manager_go_forward():
        """File manager go forward"""
    def file_manager_go_parent():
        """File manager go parent"""
    def file_manager_focus_address():
        """File manager focus address field"""
    def file_manager_open_directory(path: str):
        """File manager go to path"""
    def file_manager_copy_address():
        """File manager copy address"""

    # ----- Create folders / files -----
    def file_manager_new_folder(name: str = None):
        """Creates a new folder"""
    def file_manager_new_file(name: str = None):
        """Creates a new file"""

    # ----- Miscellaneous -----
    def file_manager_show_properties():
        """Shows the properties for the file"""
    def file_manager_terminal_here():
        """Opens terminal at current location"""


def get_windows_paths():
    return {
        "recycle bin":          "shell:RecycleBinFolder",
        "root":                 environ["HOMEDRIVE"],
        "app data":             environ["APPDATA"],
        "program files":        environ["PROGRAMFILES"],
        "temp":                 environ["TEMP"],
        "windows":              environ["WINDIR"]
    }


def get_linux_paths():
    return {
        "root":                 "/",
        "temp":                "/tmp"
    }


def on_ready():
    user_path = str(actions.path.user_home())
    user_dirs = [
        "Desktop",
        "Documents",
        "Downloads",
        "Pictures",
        "Dropbox"
    ]
    common_paths = {
        "user":                 user_path,
        "talon app":            str(actions.path.talon_app()),
        "talon home":           str(actions.path.talon_home()),
        "talon user":           str(actions.path.talon_user())
    }
    os_paths = {}
    if app.platform == "windows":
        os_paths = get_windows_paths()
    elif app.platform == "linux":
        os_paths = get_linux_paths()

    ctx.lists["self.path"] = merge(
        {p.lower(): path.join(user_path, p) for p in user_dirs},
        common_paths,
        os_paths
    )

    # for k, v in sorted(ctx.lists["self.path"].items(), key=lambda i: i[1]):
    #     print(f"{k.ljust(20)}{v}")


app.register("ready", on_ready)
