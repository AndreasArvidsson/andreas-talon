import ctypes
from ctypes import wintypes

from talon import Module, actions, cron, ui

cron_job = None
move_offset = 2

MOUSEEVENTF_MOVE = 0x0001
ULONG_PTR = (
    ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong
)

mouse_event = ctypes.WinDLL("user32", use_last_error=True).mouse_event
mouse_event.argtypes = (
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    ULONG_PTR,
)
mouse_event.restype = None

mod = Module()

mod.setting(
    "mouse_wiggle",
    type=bool,
    default=False,
    desc="Wiggle the mouse periodically to trigger mouse move event",
)


def mouse_wiggle():
    mouse_event(MOUSEEVENTF_MOVE, move_offset, move_offset, 0, 0)
    mouse_event(MOUSEEVENTF_MOVE, -move_offset, -move_offset, 0, 0)


def on_activate(app):
    global cron_job
    if actions.settings.get("user.mouse_wiggle"):
        cron_job = cron.interval("8ms", mouse_wiggle)


def on_deactivate(app):
    global cron_job
    if cron_job is not None:
        cron.cancel(cron_job)
        cron_job = None


ui.register("app_activate", on_activate)
ui.register("app_deactivate", on_deactivate)
