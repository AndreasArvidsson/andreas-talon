from talon import Context, actions
import ctypes


ctx = Context()
ctx.matches = r"""
os: windows
"""

ctx.lists["user.launch_command"] = {
    "advanced settings": "systempropertiesadvanced.exe",
    "code": "code",
    "control panel": "control",
    "device manager": "devmgmt.msc",
    "disk management": "diskmgmt.msc",
    "explorer": "explorer",
    "notepad": "notepad",
    "paint": "mspaint",
    "services": "services.msc",
    "sound settings": "control mmsys.cpl sounds",
    "system settings": "start ms-settings:",
    "task manager": "taskmgr",
    "taskbar settings": "start ms-settings:taskbar",
}


@ctx.action_class("user")
class UserActions:
    def system_shutdown():
        shutdown("s /t 0")

    def system_restart():
        shutdown("r /t 0")

    def system_hibernate():
        shutdown("h")
        actions.key("enter")

    def system_lock():
        ctypes.windll.user32.LockWorkStation()


def shutdown(flag: str):
    actions.key("super-r")
    actions.sleep("100ms")
    actions.insert(f"shutdown /{flag}")
