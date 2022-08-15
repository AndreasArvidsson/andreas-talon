from talon import Context, actions


ctx = Context()
ctx.matches = r"""
os: windows
"""

ctx.lists["self.launch_command"] = {
    "control panel": "control",
    "sound settings": "control mmsys.cpl sounds",
    "system settings": "ms-settings:",
    "taskbar settings": "ms-settings:taskbar",
    "services": "services.msc",
    "device manager": "devmgmt.msc",
    "paint": "mspaint",
    "notepad": "notepad",
    "explorer": "explorer",
    "code": "code",
}


@ctx.action_class("user")
class UserActionsWin:
    def exec(command: str):
        actions.key("super-r")
        actions.sleep("40ms")
        actions.insert(command)
        actions.key("enter")

    def system_shutdown():
        shutdown("s /t 0")

    def system_restart():
        shutdown("r /t 0")

    def system_hibernate():
        shutdown("h")
        actions.key("enter")


def shutdown(flag: str):
    actions.key("super-r")
    actions.sleep("30ms")
    actions.insert(f"shutdown /{flag}")
