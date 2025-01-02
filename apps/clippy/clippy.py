from typing import Optional
from talon import Module, actions
from .clippy_clip_item import ClipItem
from .clippy_rpc import rpc, rpc_get
from .clippy_targets import ClippyPrimitiveTarget, ClippyTarget, targets_to_dict

mod = Module()

mod.list("clippy_command_with_targets", desc="Clippy commands WITH targets")
mod.list("clippy_command_no_targets", desc="Clippy commands WITHOUT targets")

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
        """Send command without targets to Clippy"""
        rpc({"id": command_id})

    def clippy_search_items(text: str):
        """Search for clipboard items with <text> in Clippy"""
        rpc({"id": "searchItems", "text": text})

    def clippy_command_with_targets(command_id: str, targets: list[ClippyTarget]):
        """Send a command with targets to Clippy"""
        if command_id == "pasteItems":
            paste_items(targets)
        else:
            rpc({"id": command_id, "targets": targets_to_dict(targets)})

    def clippy_paste_indices(indices: list[int]):
        """Paste clipboard items from Clippy at the given indices"""
        targets = [ClippyPrimitiveTarget(str(i)) for i in indices]
        actions.user.clippy_command_with_targets("pasteItems", targets)

    def clippy_paste_first(count: int):
        """Paste first <count> clipboard items from Clippy in reverse order"""
        target = ClippyPrimitiveTarget("1", count, True)
        actions.user.clippy_command_with_targets("pasteItems", [target])

    def clippy_rename_items(targets: list[ClippyTarget], name: Optional[str] = None):
        """Rename Clippy clipboard items to <name>"""
        rpc({"id": "renameItems", "name": name, "targets": targets_to_dict(targets)})

    def clippy_get_items(targets: list[ClippyTarget]) -> list[ClipItem]:
        """Get clipboard items from Clippy"""
        return rpc_get({"id": "getItems", "targets": targets_to_dict(targets)})


def paste_items(targets: list[ClippyTarget]):
    command = {
        "id": "copyItems",
        "visibility": "hideOrBlurIfPinned",
        "targets": targets_to_dict(targets),
    }
    rpc(command)
    actions.sleep("50ms")
    actions.edit.paste()
