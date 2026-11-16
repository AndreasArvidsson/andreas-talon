import ctypes
from ctypes import wintypes

from talon import Context, Module, cron, settings, ui

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
ctx = Context()

mod.setting(
    "mouse_wiggle",
    type=bool,
    default=False,
    desc="Wiggle the mouse periodically to trigger mouse move event",
)


@mod.action_class
class Actions:
    def mouse_wiggle_toggle(enabled: bool):
        """Enable or disable mouse wiggle"""
        if enabled:
            ctx.settings = {
                "user.mouse_wiggle": True,
            }
        else:
            ctx.settings = {}
        update()


def mouse_wiggle():
    mouse_event(MOUSEEVENTF_MOVE, move_offset, move_offset, 0, 0)
    mouse_event(MOUSEEVENTF_MOVE, -move_offset, -move_offset, 0, 0)


def activate():
    global cron_job
    if cron_job is None:
        cron_job = cron.interval("8ms", mouse_wiggle)


def deactivate():
    global cron_job
    if cron_job is not None:
        cron.cancel(cron_job)
        cron_job = None


def update():
    if settings.get("user.mouse_wiggle"):
        activate()
    else:
        deactivate()


ui.register("app_activate", lambda _: update())
ui.register("app_deactivate", lambda _: update())
