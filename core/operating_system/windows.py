from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: windows
"""

ctx.lists["user.launch_command"] = {
    "control panel": "control",
    "sound settings": "control mmsys.cpl sounds",
    "system settings": "start ms-settings:",
    "taskbar settings": "start ms-settings:taskbar",
    "advanced settings": "systempropertiesadvanced.exe",
    "task manager": "taskmgr",
    "services": "services.msc",
    "device manager": "devmgmt.msc",
    "paint": "mspaint",
    "notepad": "notepad",
    "explorer": "explorer",
    "code": "code",
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
        actions.user.exec("rundll32.exe user32.dll,LockWorkStation")

    def app_switcher():
        """Show system application switcher"""
        actions.key("super-tab")


def shutdown(flag: str):
    actions.key("super-r")
    actions.sleep("50ms")
    actions.insert(f"shutdown /{flag}")
