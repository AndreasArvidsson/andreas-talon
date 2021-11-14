from talon import Context, actions


ctx = Context()
ctx.matches = r"""
os: windows
"""

ctx.lists["self.launch_command"] = {
    "control panel": "control",
    "sound settings": "control mmsys.cpl sounds",
    "settings": "ms-settings:",
    "paint": "mspaint",
    "notepad": "notepad",
    "explorer": "explorer",
    "code": "code",
}


@ctx.action_class("user")
class UserActionsWin:
    def exec(command: str):
        actions.key("super-r")
        actions.sleep("30ms")
        actions.insert(command)
        actions.key("enter")

    def system_shutdown():
        shutdown("s")

    def system_restart():
        shutdown("r")

    def system_hibernate():
        shutdown("h")


def shutdown(flag: str):
    actions.key("super-r")
    actions.sleep("30ms")
    actions.insert(f"shutdown /{flag}")
