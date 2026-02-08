from typing import Optional
from talon import Module, Context, actions
import json
import re

mod = Module()
mod.list("vscode_sessions", "Known vscode sessions/workspaces")

mod.apps.vscode = r"""
os: windows
and app.exe: code.exe
os: linux
and app.name: Code
"""


ctx = Context()
ctx.matches = r"""
app: vscode
"""


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.user.run_rpc_command("workbench.action.newWindow")

    def tab_open():
        actions.user.run_rpc_command("workbench.action.files.newUntitledFile")

    def tab_previous():
        actions.user.run_rpc_command("workbench.action.previousEditorInGroup")

    def tab_next():
        actions.user.run_rpc_command("workbench.action.nextEditorInGroup")

    def preferences():
        actions.user.run_rpc_command("workbench.action.openGlobalSettings")


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

    # ----- Word -----
    def delete_word():
        empty_selection()
        actions.next()

    # ----- Line commands -----
    def line_insert_down():
        actions.key("ctrl-enter")

    def line_swap_up():
        actions.user.run_rpc_command("editor.action.moveLinesUpAction")

    def line_swap_down():
        actions.user.run_rpc_command("editor.action.moveLinesDownAction")

    def line_clone():
        actions.user.run_rpc_command("editor.action.copyLinesDownAction")

    # Don't use RPC since the PR description editor doesn't support it.
    # def line_insert_up():
    #     actions.user.run_rpc_command("editor.action.insertLineBefore")

    # Don't use RPC since some vscode extension(eg markdown) has specific behavior on enter
    # def line_insert_down():
    # actions.user.run_rpc_command("editor.action.insertLineAfter")

    def delete_line():
        actions.user.run_rpc_command("editor.action.deleteLines")

    def jump_line(n: int):
        actions.user.run_rpc_command("andreas.goToLine", n)

    # ----- Indent -----
    def indent_more():
        actions.user.run_rpc_command("editor.action.indentLines")

    def indent_less():
        actions.user.run_rpc_command("editor.action.outdentLines")

    # ----- Zoom -----
    def zoom_reset():
        actions.user.run_rpc_command("workbench.action.zoomReset")


@ctx.action_class("user")
class UserActions:
    def command_server_directory() -> str:
        return "vscode-command-server"

    # ----- Navigation -----
    def go_back():
        actions.user.run_rpc_command("workbench.action.navigateBack")

    def go_forward():
        actions.user.run_rpc_command("workbench.action.navigateForward")

    def line_middle():
        actions.user.run_rpc_command("andreas.lineMiddle")

    # ----- Find / Replace -----
    def find_everywhere(text: str = None):
        actions.user.run_rpc_command("workbench.action.findInFiles")
        if text:
            actions.sleep("50ms")
            actions.insert(text)

    def find_file(text: str = None):
        actions.user.run_rpc_command("workbench.action.quickOpen")
        if text:
            actions.sleep("50ms")
            actions.insert(text)

    def find_toggle_match_by_case():
        actions.key("alt-c")

    def find_toggle_match_by_word():
        actions.key("alt-w")

    def find_toggle_match_by_regex():
        actions.key("alt-r")

    def find_replace_toggle_preserve_case():
        actions.key("alt-p")

    def find_replace_confirm():
        actions.key("enter")

    def find_replace_confirm_all():
        actions.key("ctrl-alt-enter")

    # ----- Tabs -----
    def tab_jump(number: int):
        actions.user.run_rpc_command("andreas.openEditorAtIndex", number - 1)

    def tab_jump_from_back(number: int):
        actions.user.run_rpc_command("andreas.openEditorAtIndex", -number)

    def tab_final():
        actions.user.run_rpc_command("workbench.action.lastEditorInGroup")

    def tab_back():
        actions.user.run_rpc_command(
            "workbench.action.openPreviousRecentlyUsedEditorInGroup"
        )

    def tab_pin():
        actions.user.run_rpc_command("workbench.action.pinEditor")

    def tab_unpin():
        actions.user.run_rpc_command("workbench.action.unpinEditor")

    def tab_close_all():
        actions.user.run_rpc_command("workbench.action.closeEditorsInGroup")

    def tab_close_others():
        actions.user.run_rpc_command("workbench.action.closeOtherEditors")

    def tab_close_left():
        actions.user.run_rpc_command("workbench.action.closeEditorsToTheLeft")

    def tab_close_right():
        actions.user.run_rpc_command("workbench.action.closeEditorsToTheRight")

    # ----- Scroll -----
    def scroll_up():
        actions.key("ctrl-up")

    def scroll_down():
        actions.key("ctrl-down")

    def scroll_up_page():
        actions.key("alt-pageup")

    def scroll_down_page():
        actions.key("alt-pagedown")

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


@mod.action_class
class Actions:
    def save_without_formatting():
        """Save current document without formatting"""
        actions.user.run_rpc_command("hideSuggestWidget")
        actions.user.run_rpc_command("workbench.action.files.saveWithoutFormatting")

    def format_document():
        """Format document"""
        actions.user.run_rpc_command("editor.action.formatDocument")

    def vscode_find_recent(text: Optional[str] = None):
        """Find recent session, directory or file"""
        actions.user.run_rpc_command("workbench.action.openRecent")
        if text:
            actions.sleep("150ms")
            actions.insert(text)

    def vscode_take_word(cursorless_target: dict, repeats: int):
        """Take word on cursorless target with number of repeats"""
        actions.user.cursorless_command("setSelection", cursorless_target)
        text = actions.edit.selected_text()

        if re.match(r"[\wåäöÅÄÖ]", text):
            actions.edit.right()
        else:
            repeats -= 1

        # Select number of next instances
        for _ in range(repeats):
            actions.user.run_rpc_command("editor.action.addSelectionToNextFindMatch")

        # Select all instances
        if repeats < 0:
            actions.user.run_rpc_command("editor.action.selectHighlights")

    def change_language(language: str = ""):
        """Change language mode"""
        actions.user.run_rpc_command("workbench.action.editor.changeLanguageMode")
        if language:
            actions.insert(language)

    def copy_command_id():
        """Copy the command id of the focused menu item"""
        actions.key("tab:2 enter")
        actions.sleep("500ms")
        json_text = actions.edit.selected_text()
        command_id = json.loads(json_text)["command"]
        actions.app.tab_close()
        actions.clip.set_text(command_id)

    def vscode_add_missing_imports():
        """Add all missing imports"""
        actions.user.run_rpc_command(
            "editor.action.sourceAction",
            {"kind": "source.addMissingImports", "apply": "first"},
        )

    def find_sibling_file():
        """Find sibling file based on file name"""
        full_name = actions.win.filename()
        index = full_name.rfind(".")
        if index < 0:
            return
        short_name = full_name[:index]
        extension = full_name[index + 1 :]
        sibling_extension = actions.user.get_extension_sibling(extension)
        if not sibling_extension:
            return
        sibling_full_name = f"{short_name}.{sibling_extension}"
        actions.user.find_file(sibling_full_name)


def empty_selection():
    if actions.edit.selected_text():
        actions.edit.right()
