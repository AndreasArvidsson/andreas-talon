from talon import cron, actions, app  # pyright: ignore[reportUnusedImport] # noqa: F401

title = ""


def debug_title():
    global title
    if title != actions.win.title():
        title = actions.win.title()
        print(f"'{title}'", actions.app.name())


def on_ready():
    cron.interval("32ms", debug_title)


# app.register("ready", on_ready)
