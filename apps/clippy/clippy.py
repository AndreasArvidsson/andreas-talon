from typing import Optional
from talon import Module, Context, actions, app, ui
from .clippy_clip_item import ClipItem
from .clippy_targets import ClippyPrimitiveTarget, ClippyTarget

rpc_key = "cmd-shift-f18" if app.platform == "mac" else "ctrl-shift-alt-o"
rpc_dir_name = "clippy-command-server"
rpc_command_id = "clippy-command"

mod = Module()
ctx = Context()

mod.list("clippy_command_with_targets", desc="Clippy commands WITH targets")
mod.list("clippy_command_no_targets", desc="Clippy commands WITHOUT targets")
mod.tag(
    "clippy_showing",
    desc="Tag is active whenever clippy window is showing/not hidden",
)

mod.apps.clippy = r"""
os: windows
app.exe: clippy.exe
"""
# This is used for development purposes
mod.apps.clippy = r"""
os: windows
app.exe: electron.exe
title: Clippy
"""


@mod.action_class
class Actions:
    def clippy_command_no_targets(command_id: str):
        """Send command without targets to the clipboard manager"""
        send({"id": command_id})

    def clippy_search_items(text: str):
        """Search for <text> in the clipboard manager"""
        send({"id": "searchItems", "text": text})

    def clippy_command_with_targets(command_id: str, targets: list[ClippyTarget]):
        """Send a command with targets to the clipboard manager"""
        if command_id == "pasteItems":
            send(
                {
                    "id": "copyItems",
                    "visibility": "hideOrBlurIfPinned",
                    "targets": to_dict(targets),
                }
            )
            actions.sleep("50ms")
            actions.edit.paste()
        else:
            send({"id": command_id, "targets": to_dict(targets)})

    def clippy_paste_indices(indices: list[int]):
        """Paste items from the clipboard manager at the given indices"""
        targets = [ClippyPrimitiveTarget(str(i)) for i in indices]
        actions.user.clippy_command_with_targets("pasteItems", targets)

    def clippy_rename_items(targets: list[ClippyTarget], name: Optional[str] = None):
        """Rename clipboard targets to <name>"""
        send({"id": "renameItems", "targets": to_dict(targets), "name": name})

    def clippy_get_items(targets: list[ClippyTarget]) -> list[ClipItem]:
        """Get clipboard targets"""
        return get({"id": "getItems", "targets": to_dict(targets)})


def to_dict(targets: list[ClippyTarget]) -> list[dict]:
    return [t.to_dict() for t in targets]


def send(command: dict):
    rpc_command(command, wait_for_finish=True)


def get(command: dict):
    return rpc_command(command, return_command_output=True)


def rpc_command(
    command: dict,
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


def update(window: ui.Window, onShow: bool):
    if window.title != "Clippy":
        return
    if window.app.name != "Clippy" and window.app.name != "Electron":
        return
    if onShow:
        ctx.tags = ["user.clippy_showing"]
    else:
        ctx.tags = []


ui.register("win_show", lambda win: update(win, True))
ui.register("win_hide", lambda win: update(win, False))
