from talon import Module, Context, registry, app, actions


matchers = [
    "os: windows",
    "language: en",
    "code.language: python",
    "speech.engine: wav2letter",
    "hostname: /andreas/",
    "title: /debug/",
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
        index = str(i + 1).rjust(2)
        result.append(f"{index}: {matches}")

    res = "\n".join(result)
    print(" \n" + res)
    actions.clip.set_text(res)


def run():
    mod = Module()
    mod.list("debug_matches")

    for matches in matchers:
        ctx = Context()
        ctx.matches = matches
        ctx.lists["user.debug_matches"] = {"matches": matches.replace("\n", " \\n ")}

    app.register("ready", on_ready)


# run()


#  1: app: vscode
#  2: title: /debug/
#  3: hostname: /andreas/
#  4: speech.engine: wav2letter
#  5: code.language: python
#  6: not mode: sleep
#  7: mode: command
#  8: mode: all
#  9: language: en
# 10: tag: user.cursorless \n and tag: user.tabs
# 11: tag: user.cursorless \n tag: user.tabs
# 12: tag: user.cursorless
# 13: os: windows
