import dataclasses
from typing import Any
from talon import Module, Context, actions

from ...core.rpc_client.rpc_client import RpcClient
from .clippy_targets import ClippyPrimitiveTarget, ClippyTarget

rpc = RpcClient("Clippy", "ctrl-shift-alt-o")

mod = Module()

mod.list("clippy_command_with_targets", desc="Clippy commands WITH targets")
mod.list("clippy_command_no_targets", desc="Clippy commands WITHOUT targets")


ctx = Context()

ctx.lists["user.clippy_command_with_targets"] = {
    "chuck": "removeItems",
    "copy": "copyItems",
}

ctx.lists["user.clippy_command_no_targets"] = {
    "clear": "clear",
    "pin": "togglePinned",
    "search": "toggleSearch",
}


@mod.action_class
class Actions:
    def clippy_command_no_targets(command_id: str):
        """Send command without targets to the clipboard manager"""
        command = {"id": command_id}
        send(command)

    def clippy_command_with_targets(command_id: str, targets: list[ClippyTarget]):
        """Send a command with targets to the clipboard manager"""
        if command_id == "pasteItems":
            command = {"id": "copyItems", "targets": targets}
            send(command)
            actions.sleep("50ms")
            actions.edit.paste()
        else:
            command = {"id": command_id, "targets": targets}
            send(command)

    def clippy_paste_indices(indices: list[int]):
        """Paste items from the clipboard manager at the given indices"""
        targets = [ClippyPrimitiveTarget(str(i)) for i in indices]
        actions.user.clippy_command_with_targets("pasteItems", targets)

    def clippy_search(text: str):
        """Search for <text> in the clipboard manager"""
        command = {"id": "search", "text": text}
        send(command)


def send(command: Any):
    rpc.send(command, wait_for_finish=True)
