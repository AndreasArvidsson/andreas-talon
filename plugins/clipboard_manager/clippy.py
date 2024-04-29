import dataclasses
from typing import Any
from talon import Module, Context, actions

from ...core.rpc_client.rpc_client import RpcClient
from .clippy_targets import ClippyTarget

rpc = RpcClient("Clippy", "ctrl-shift-alt-o")

mod = Module()

mod.list("clippy_command_with_targets", desc="Clippy commands WITH targets")
mod.list("clippy_command_no_targets", desc="Clippy commands WITHOUT targets")


ctx = Context()

ctx.lists["user.clippy_command_with_targets"] = {
    "chuck": "removeItems",
    "copy": "copyItems",
    "paste": "pasteItems",
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
        command = {"id": command_id, "targets": targets}
        send(command)

        if command_id == "pasteItems":
            actions.edit.paste()

    def clippy_search(text: str):
        """Search for <text> in the clipboard manager"""
        command = {"id": "search", "text": text}
        send(command)


def send(command: Any):
    rpc.send(
        make_serializable(command),
        wait_for_finish=True,
    )


def make_serializable(value: Any) -> Any:
    """
    Converts a dataclass into a serializable dict

    Note that we don't use the built-in asdict() function because it will
    ignore the static `type` field.

    Args:
        value (any): The value to convert

    Returns:
        _type_: The converted value, ready for serialization
    """
    if isinstance(value, dict):
        return {k: make_serializable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [make_serializable(v) for v in value]
    if dataclasses.is_dataclass(value):
        items = {
            **{k: v for k, v in value.__class__.__dict__.items() if k[0] != "_"},
            **value.__dict__,
        }
        return {k: make_serializable(v) for k, v in items.items() if v is not None}
    return value
