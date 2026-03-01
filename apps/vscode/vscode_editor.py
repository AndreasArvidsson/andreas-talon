from typing import Optional
from talon import Context, actions

ctx = Context()
ctx.matches = r"""
app: vscode
win.title: /\[Text Editor\]/
"""


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.user.run_rpc_command("editor.action.commentLine")

    def complete():
        actions.user.run_rpc_command("editor.action.triggerSuggest")


@ctx.action_class("edit")
class EditActions:
    def save():
        actions.user.run_rpc_command("hideSuggestWidget")
        actions.next()

    def selected_text() -> str:
        try:
            selectedTexts = actions.user.run_rpc_command_get("andreas.getSelectedText")
            if selectedTexts is not None:
                return "\n".join(selectedTexts)
        except Exception as ex:
            print(f"EXCEPTION: {ex}")

        return actions.next()

    def select_none():
        actions.key("escape")

    # ----- Line commands -----

    def line_insert_up():
        actions.key("home enter up")

    # Don't use RPC since some vscode extension(eg markdown) has specific behavior on enter
    def line_insert_down():
        actions.edit.line_end()
        actions.key("enter")

    def line_swap_up():
        actions.user.run_rpc_command("editor.action.moveLinesUpAction")

    def line_swap_down():
        actions.user.run_rpc_command("editor.action.moveLinesDownAction")

    def line_clone():
        actions.user.run_rpc_command("editor.action.copyLinesDownAction")

    def delete_line():
        actions.user.run_rpc_command("editor.action.deleteLines")

    def jump_line(n: int):
        actions.user.run_rpc_command("andreas.goToLine", n)

    # ----- Word -----

    def delete_word():
        empty_selection()
        actions.next()

    # ----- Indent -----

    def indent_more():
        actions.user.run_rpc_command("editor.action.indentLines")

    def indent_less():
        actions.user.run_rpc_command("editor.action.outdentLines")


@ctx.action_class("user")
class UserActions:
    # ----- Navigation -----

    def line_middle():
        actions.user.run_rpc_command("andreas.lineMiddle")

    # ----- Scroll -----

    def scroll_up_half_page():
        actions.user.run_rpc_command("editorScroll", {"to": "up", "by": "halfPage"})

    def scroll_down_half_page():
        actions.user.run_rpc_command("editorScroll", {"to": "down", "by": "halfPage"})

    # ----- Word -----

    def cut_word():
        empty_selection()
        actions.next()

    def copy_word():
        empty_selection()
        actions.next()

    def paste_word():
        empty_selection()
        actions.next()

    # ----- Dictation -----

    def dictation_get_context() -> tuple[Optional[str], Optional[str]]:
        try:
            context = actions.user.run_rpc_command_get("andreas.getDictationContext")
        except Exception:
            context = None

        if context is not None:
            return (context["before"], context["after"])
        return (None, None)

    # ----- Snippets -----

    def insert_snippet(body: str):
        actions.user.run_rpc_command("editor.action.insertSnippet", {"snippet": body})

    # ----- Text getters -----

    def code_get_class_name() -> Optional[str]:
        return actions.user.run_rpc_command_get("andreas.getClassName")

    def code_get_open_tag_name() -> Optional[str]:
        return actions.user.run_rpc_command_get("andreas.getOpenTagName")


def empty_selection():
    if actions.edit.selected_text():
        actions.edit.right()
