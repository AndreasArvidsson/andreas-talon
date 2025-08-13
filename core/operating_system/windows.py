from talon import Context, actions
import ctypes


ctx = Context()
ctx.matches = r"""
os: windows
"""

ctx.lists["user.launch_command"] = {
    "code": "code",
    "explorer": "explorer",
    "notepad": "notepad",
    "paint": "mspaint",
    "task manager": "taskmgr",
    "services": "services.msc",
    "control panel": "control",
    "device manager": "devmgmt.msc",
    "disk management": "diskmgmt.msc",
    "sound settings": "control mmsys.cpl sounds",
    "system settings": "start ms-settings:",
    "taskbar settings": "start ms-settings:taskbar",
    "advanced settings": "systempropertiesadvanced.exe",
    "environment variables": "rundll32.exe sysdm.cpl,EditEnvironmentVariables",
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
