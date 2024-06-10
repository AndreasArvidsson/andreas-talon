from talon import Context, actions

ctx = Context()
ctx.matches = r"""
tag: terminal
"""


@ctx.action_class("main")
class MainActions:
    def insert(text: str):
        # Inserting text ending with new line means that we want to press enter
        if text[-1] == "\n":
            actions.next(text[:-1])
            actions.key("enter")
        else:
            actions.next(text)
