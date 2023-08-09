from talon import Context, app, fs
from pathlib import Path
from .snippets_parser import get_snippets

SNIPPETS_DIR = Path(__file__).parent / "snippets"


def update_snippets():
    snippets = get_snippets(SNIPPETS_DIR)

    for snippet in snippets:
        print(snippet)


def on_ready():
    fs.watch(str(SNIPPETS_DIR), lambda _1, _2: update_snippets())
    update_snippets()


# app.register("ready", on_ready)


# snippet = f"{symbol}$TM_SELECTED_TEXT$0{symbol}"
# actions.user.cursorless_insert_snippet(snippet)

# actions.user.insert_snippet(
#     snippet
# )
# actions.user.cursorless_wrap_with_snippet(snippet, target, "try", "statement")
