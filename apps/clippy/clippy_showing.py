from talon import Module, Context, ui

mod = Module()
ctx = Context()

mod.tag(
    "clippy_showing",
    desc="Tag is active whenever clippy window is showing/not hidden",
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
