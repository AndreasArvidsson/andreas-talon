from talon import Module, Context, actions
import re

mod = Module()
mod.tag(
    "insert_paste_disabled",
    "Never use clipboard/paste for insertions in 'insert' action",
)

ctx = Context()
ctx.matches = r"""
not tag: user.insert_paste_disabled
"""


# Use paste for inserting text that cannot be undone in a single undo step
PASTE_RE = re.compile(r"\s")
# Use paste for inserting text with length greater or equal to the threshold
PASTE_THRESHOLD = 50


@ctx.action_class("main")
class MainActions:
    def insert(text: str):
        if len(text) >= PASTE_THRESHOLD or re.search(PASTE_RE, text):
            actions.user.paste_text(text)
        else:
            actions.next(text)
