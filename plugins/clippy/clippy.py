from typing import Any, Optional
from talon import Module, Context, actions, app, ui

from .clippy_targets import ClippyPrimitiveTarget, ClippyTarget

rpc_key = "cmd-shift-f18" if app.platform == "mac" else "ctrl-shift-alt-o"
rpc_dir_name = "clippy-command-server"
rpc_command_id = "clippy-command"


mod = Module()

mod.list("clippy_command_with_targets", desc="Clippy commands WITH targets")
mod.list("clippy_command_no_targets", desc="Clippy commands WITHOUT targets")
mod.tag(
    "clippy_showing", desc="Tag is active whenever clippy window is showing/not hidden"
)

mod.apps.clippy = r"""
app.name: Electron
title: /Clippy/
"""

ctx = Context()

ctx.lists["user.clippy_command_with_targets"] = {
    "paste": "pasteItems",
    "chuck": "removeItems",
    "copy": "copyItems",
}

ctx.lists["user.clippy_command_no_targets"] = {
    # "exit": "exit",
    "toggle": "toggleShowHide",
    "show": "show",
    "hide": "hide",
    "pin toggle": "togglePinned",
    "pin": "pin",
    "unpin": "unpin",
    "dev tools": "toggleDevTools",
    "dev tools show": "showDevTools",
    "dev tools hide": "hideDevTools",
    "search": "toggleSearch",
    "search show": "showSearch",
    "search hide": "hideSearch",
    "pause toggle": "togglePaused+",
    "pause": "pause",
    "resume": "resume",
    "auto star": "toggleAutoStar",
    "auto star on": "enableAutoStar",
    "auto star off": "disableAutoStar",
    # "clear": "removeAllItems",
    # "remove list": "removeList",
}


@mod.action_class
class Actions:
    def clippy_command_no_targets(command_id: str):
        """Send command without targets to the clipboard manager"""
        send({"id": command_id})

    def clippy_command_with_targets(command_id: str, targets: list[ClippyTarget]):
        """Send a command with targets to the clipboard manager"""
        serializable_targets = [t.to_dict() for t in targets]
        if command_id == "pasteItems":
            command = {"id": "copyItems", "targets": serializable_targets}
            send(command)
            actions.sleep("50ms")
            actions.edit.paste()
        else:
            send({"id": command_id, "targets": serializable_targets})

    def clippy_paste_indices(indices: list[int]):
        """Paste items from the clipboard manager at the given indices"""
        targets = [ClippyPrimitiveTarget(str(i)) for i in indices]
        actions.user.clippy_command_with_targets("pasteItems", targets)

    def clippy_search(text: str):
        """Search for <text> in the clipboard manager"""
        send({"id": "searchItems", "text": text})

    def clippy_rename(targets: list[ClippyTarget], text: Optional[str] = None):
        """Rename clipboard targets to <text>"""
        serializable_targets = [t.to_dict() for t in targets]
        send({"id": "renameItems", "targets": serializable_targets, "text": text})

    def clippy_get(targets: list[ClippyTarget]):
        """Get clipboard targets"""
        serializable_targets = [t.to_dict() for t in targets]
        result = get({"id": "getItems", "targets": serializable_targets})
        print(result)


def send(command: Any):
    return rpc_command(command, wait_for_finish=True)


def get(command: Any):
    return rpc_command(command, return_command_output=True)


def rpc_command(
    command: Any,
    wait_for_finish: bool = False,
    return_command_output: bool = False,
):
    return actions.user.rpc_client_run_command(
        rpc_dir_name,
        lambda: actions.key(rpc_key),
        rpc_command_id,
        [command],
        wait_for_finish,
        return_command_output,
    )


def update(window, onShow):
    if window.title != "Clippy" or window.app.name != "Clippy":
        return
    if onShow:
        ctx.tags = ["user.clippy_showing"]
    else:
        ctx.tags = []


ui.register("win_show", lambda win: update(win, True))
ui.register("win_hide", lambda win: update(win, False))
