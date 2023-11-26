from talon import Module, Context, actions

mod = Module()
mod.tag("vscode_notebook", desc="Vscode is in a notebook")

ctx = Context()
ctx.matches = r"""
app: vscode
tag: user.vscode_notebook
"""


@ctx.action_class("user")
class NotebookUserActions:
    def change_language(language: str = ""):
        if language:
            actions.insert(language)


@ctx.action_class("edit")
class NotebookEditActions:
    # ----- Line commands -----
    def line_swap_up():
        actions.user.vscode("notebook.cell.moveUp")

    def line_swap_down():
        actions.user.vscode("notebook.cell.moveDown")
