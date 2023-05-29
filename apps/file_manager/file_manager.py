from talon import app, Module, Context, actions, app
from os import path, environ

mod = Module()
mod.tag("file_manager", desc="Tag for enabling generic file management commands")
mod.list("path", desc="List of the users favorite paths")

ctx = Context()

ctx_win = Context()
ctx_win.matches = r"""
os: windows
"""

ctx_linux = Context()
ctx_linux.matches = r"""
os: linux
"""


@ctx_win.action_class("user")
class WinUserActions:
    def file_manager_open(path: str):
        actions.user.exec(f"explorer {path}")


@ctx_linux.action_class("user")
class LinuxUserActions:
    def file_manager_open(path: str):
        actions.user.exec(f"nautilus {path}")


@mod.action_class
class Actions:
    # ----- Path -----
    def talon_app() -> str:
        """Get path to talon application"""
        return actions.path.talon_app()

    def talon_home() -> str:
        """Get path to talon home"""
        return actions.path.talon_home()

    def talon_user() -> str:
        """Get path to talon user"""
        return actions.path.talon_user()

    def user_home() -> str:
        """Get path to user home"""
        return actions.path.user_home()

    def update_path(path: str):
        """Update given path"""
        return path

    # ----- Navigation -----
    def file_manager_go_parent():
        """File manager go parent"""

    def file_manager_go_home():
        """File manager go user home"""

    def file_manager_focus_address():
        """File manager focus address field"""

    def file_manager_go(path: str):
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

    def file_manager_open(path: str):
        """Open file manager at the given path"""


def get_windows_paths():
    return {
        "recycle bin": "shell:RecycleBinFolder",
        "applications": "shell:AppsFolder",
        "root": environ["HOMEDRIVE"],
        "app data": environ["APPDATA"],
        "local app data": environ["LOCALAPPDATA"],
        "program files": environ["PROGRAMFILES"],
        "temp": environ["TEMP"],
        "windows": environ["WINDIR"],
        "talon bin": path.join(str(actions.path.talon_home()), ".venv", "Scripts"),
    }


def get_linux_paths():
    return {
        "root": "/",
        "temp": "/tmp",
        "talon bin": path.join(str(actions.path.talon_home()), "bin"),
    }


def on_ready():
    user_path = str(actions.path.user_home())
    user_dirs = [
        "Desktop",
        "Documents",
        "Downloads",
        "Pictures",
        "Videos",
        "Dropbox",
    ]
    common_paths = {
        "user": user_path,
        "talon app": str(actions.path.talon_app()),
        "talon home": str(actions.path.talon_home()),
        "talon user": str(actions.path.talon_user()),
        "talon recordings": path.join(str(actions.path.talon_home()), "recordings"),
    }
    if app.platform == "windows":
        os_paths = get_windows_paths()
    elif app.platform == "linux":
        os_paths = get_linux_paths()
    else:
        os_paths = {}

    ctx.lists["self.path"] = {
        **{p.lower(): path.join(user_path, p) for p in user_dirs},
        **common_paths,
        **os_paths,
    }

    # for k, v in sorted(ctx.lists["self.path"].items(), key=lambda i: i[1]):
    #     print(f"{k.ljust(20)}{v}")


app.register("ready", on_ready)
