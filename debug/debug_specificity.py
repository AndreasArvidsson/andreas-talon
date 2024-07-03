from talon import Module, Context, registry, app, actions


matchers = [
    "app: vscode",
    "tag: user.cursorless",
    "tag: user.cursorless\ntag: user.tabs",
    "tag: user.cursorless\nand tag: user.tabs",
    "mode: all",
    "mode: command",
    "not mode: sleep",
]


def on_ready():
    lists = registry.lists["user.debug_matches"]
    lists.reverse()
    result = []

    for i, l in enumerate(lists):
        matches = l["matches"]  # type: ignore
        result.append(f"{i+1}: {matches}")

    res = "\n".join(result)
    print(" \n" + res)
    actions.clip.set_text(res)


def run():
    mod = Module()
    mod.list("debug_matches")

    for matches in matchers:
        ctx = Context()
        ctx.matches = matches
        ctx.lists["user.debug_matches"] = {"matches": matches}

    app.register("ready", on_ready)


# run()


# 1: app: vscode
# 2: not mode: sleep
# 3: mode: command
# 4: mode: all
# 5: tag: user.cursorless
#    and tag: user.tabs
# 6: tag: user.cursorless
#    tag: user.tabs
# 7: tag: user.cursorless
