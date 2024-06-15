from talon import (
    Context,
    Module,
    actions,
    app,
    storage,
)
from typing import Optional

mod = Module()

mod.tag("eye_tracker", "Indicates that the eye tracker is enabled")
mod.tag(
    "eye_tracker_frozen",
    "Indicates that the eye tracker cursor position updating is frozen",
)

ctx = Context()

ctx_eye_tracker = Context()
ctx_eye_tracker.matches = r"""
tag: user.eye_tracker
"""

ctx_frozen = Context()
ctx_frozen.matches = r"""
tag: user.eye_tracker_frozen
"""


@ctx_eye_tracker.action_class("user")
class EyeTrackerActions:
    def mouse_on_pop():
        actions.user.mouse_click_with_conditions()


@ctx_frozen.action_class("user")
class FrozenActions:
    def mouse_on_pop():
        actions.user.mouse_click_with_conditions()

    def mouse_freeze_toggle():
        enable_tracker()


@mod.action_class
class Actions:
    def mouse_control_toggle(enable: Optional[bool] = None):
        """Toggle enable/disable for the eye tracker"""
        if enable is None:
            enable = not actions.tracking.control_enabled()

        if enable:
            enable_tracker()
        else:
            disable_tracker()

        enabled = actions.tracking.control_enabled()
        actions.user.notify(f"Control mouse: {enabled}")

    def mouse_freeze_toggle():
        """Toggle freeze cursor position updates for the eye tracker"""
        freeze_tracker()

    def mouse_wake():
        """Set control mouse to earlier state"""
        tracking_control = storage.get("tracking_control", "disabled")
        if tracking_control == "enabled":
            enable_tracker()
        elif tracking_control == "frozen":
            ctx.tags = ["user.eye_tracker_frozen"]

    def mouse_sleep():
        """Disables control mouse and scroll"""
        actions.user.mouse_scroll_stop()
        actions.user.mouse_release_held_buttons()
        actions.tracking.control_toggle(False)
        ctx.tags = []


def enable_tracker():
    actions.tracking.control_toggle(True)
    if actions.tracking.control_enabled():
        storage.set("tracking_control", "enabled")
        ctx.tags = ["user.eye_tracker"]


def disable_tracker():
    actions.tracking.control_toggle(False)
    storage.set("tracking_control", "disabled")
    ctx.tags = []


def freeze_tracker():
    actions.tracking.control_toggle(False)
    storage.set("tracking_control", "frozen")
    ctx.tags = ["user.eye_tracker_frozen"]


def on_launch():
    """Restore eye tracker after a Talon restart"""
    if actions.user.talon_was_restarted():
        actions.user.mouse_wake()


app.register("launch", on_launch)
