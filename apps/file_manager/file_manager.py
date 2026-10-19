from os import environ, path

from talon import Context, Module, actions, app

mod = Module()
mod.tag("file_manager", "Tag for enabling generic file management commands")
mod.list("path", "List of the users favorite paths")

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
    @staticmethod
    def file_manager_open(path: str):
        actions.user.exec(f"explorer {path}")


@ctx_linux.action_class("user")
class LinuxUserActions:
    @staticmethod
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

    @staticmethod
    def update_path(path: str):
        """Update given path"""
        return path

    # ----- Navigation -----
    def file_manager_focus_address():
        """File manager focus address field"""

    @staticmethod
    def file_manager_go(path: str):
        """File manager go to path"""

    def file_manager_go_parent():
        """File manager go parent"""

    def file_manager_go_home():
        """File manager go user home"""
        actions.user.file_manager_go(
            actions.user.user_home(),
        )

    @staticmethod
    def file_manager_open_new_tab(path: str):
        """File manager open path in new tab"""
        actions.app.tab_open()
        actions.sleep("100ms")
        actions.user.file_manager_go(path)

    def file_manager_open_home_new_tab():
        """File manager open user home in new tab"""
        actions.user.file_manager_open_new_tab(
            actions.user.user_home(),
        )

    def file_manager_copy_address():
        """File manager copy address"""

    # ----- Create folders / files -----
    @staticmethod
    def file_manager_new_folder(name: str):
        """Creates a new folder"""

    @staticmethod
    def file_manager_new_file(name: str):
        """Creates a new file"""

    # ----- Miscellaneous -----
    def file_manager_show_properties():
        """Shows the properties for the file"""

    def file_manager_terminal_here():
        """Opens terminal at current location"""

    @staticmethod
    def file_manager_open(path: str):
        """Open file manager at the given path"""


def get_windows_paths():
    app_data = path.dirname(environ["APPDATA"])
    return {
        "recycle bin": "shell:RecycleBinFolder",
        "applications": "shell:AppsFolder",
        "root": environ["HOMEDRIVE"],
        "app data": app_data,
        "program files": environ["PROGRAMFILES"],
        "temp": environ["TEMP"],
        "windows": environ["WINDIR"],
        "talon bin": path.join(actions.path.talon_home(), ".venv", "Scripts"),
        "magic arena": rf"{app_data}\LocalLow\Wizards Of The Coast\MTGA",
        "pictures": r"D:\Pictures",
        "dropbox": r"D:\Dropbox",
        "repositories": r"D:\repositories",
        "gss": r"D:\repositories\gss-dev-environment",
    }


def get_linux_paths():
    return {
        "root": "/",
        "temp": "/tmp",
        "talon bin": path.join(actions.path.talon_home(), "bin"),
    }


def get_os_paths():
    if app.platform == "windows":
        return get_windows_paths()
    if app.platform == "linux":
        return get_linux_paths()
    return {}


def on_ready():

    common_paths = {
        "user": actions.path.user_home(),
        "talon app": actions.path.talon_app(),
        "talon home": actions.path.talon_home(),
        "talon user": actions.path.talon_user(),
        "talon recordings": path.join(actions.path.talon_home(), "recordings"),
    }

    user_dirs = [
        "Desktop",
        "Documents",
        "Downloads",
        "Videos",
    ]

    ctx.lists["user.path"] = {
        **get_os_paths(),
        **common_paths,
        **{p.lower(): path.join(actions.path.user_home(), p) for p in user_dirs},
    }


app.register("ready", on_ready)
