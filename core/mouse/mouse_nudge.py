import win32api
import win32con
from talon import Module, actions, cron, ui

mod = Module()

cron_job = None
move_offset = 2

mod.setting(
    "mouse_nudge",
    type=bool,
    default=False,
    desc="Nudge the mouse periodically to trigger mouse move event",
)


def mouse_nudge():
    """Nudge the mouse to trigger mouse move event"""
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, move_offset, move_offset)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -move_offset, -move_offset)


def on_activate(app):
    global cron_job
    if actions.settings.get("user.mouse_nudge"):
        cron_job = cron.interval("8ms", mouse_nudge)


def on_deactivate(app):
    global cron_job
    if cron_job is not None:
        cron.cancel(cron_job)
        cron_job = None


ui.register("app_activate", on_activate)
ui.register("app_deactivate", on_deactivate)
