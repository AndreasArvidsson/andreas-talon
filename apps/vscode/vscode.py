from talon import Module, Context, actions
import json
import re

UNTITLED_RE = re.compile(r"Untitled-\d$")

mod = Module()
mod.tag("vscode_notebook")

mod.apps.vscode = r"""
os: windows
and app.exe: Code.exe
os: linux
and app.name: Code
"""


ctx = Context()
ctx.matches = r"""
app: vscode
"""

ctx_notebook = Context()
ctx_notebook.matches = r"""
app: vscode
tag: user.vscode_notebook
"""


mod.list("vscode_panel", "Available panels for resizing in vscode")
panels = {
    "bar": {
        "filename": "vscode_bar_ellipses.png",
        "position": "right",
        "xDirection": True,
    },
    "panel": {
        "filename": "vscode_panel_terminal.png",
        "position": "top",
        "xDirection": False,
    },
}
ctx.lists["self.vscode_panel"] = panels.keys()

mod.list("vscode_sessions", "Known vscode sessions/workspaces")
ctx.lists["self.vscode_sessions"] = {
    "mine": "andreas-talon",
    "extension": "andreas-vscode",
    "cursor less": "cursorless",
}


@mod.capture(rule="{self.vscode_panel}")
def vscode_panel(m) -> dict:
    return panels[m.vscode_panel]


@ctx.action_class("win")
class WinActions:
    def filename():
        filename = actions.win.title().split(" - ")[0]
        if is_untitled(filename):
            return get_untitled_name(filename)
        if "." in filename:
            return filename
        return ""


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.user.vscode("workbench.action.newWindow")

    def tab_open():
        actions.user.vscode("workbench.action.files.newUntitledFile")

    def tab_previous():
        actions.user.vscode("workbench.action.previousEditorInGroup")

    def tab_next():
        actions.user.vscode("workbench.action.nextEditorInGroup")

    def preferences():
        actions.user.vscode("workbench.action.openGlobalSettings")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.user.vscode("editor.action.commentLine")

    def complete():
        actions.user.vscode("editor.action.triggerSuggest")


@ctx.action_class("edit")
class EditActions:
    def save():
        actions.user.vscode("hideSuggestWidget")
        actions.next()

    def selected_text() -> str:
        selectedTexts = actions.user.vscode_get("andreas.getSelectedText")
        if selectedTexts is not None:
            return "\n".join(selectedTexts)
        return actions.next()

    def select_none():
        actions.key("escape")

    # ----- Word -----
    def delete_word():
        empty_selection()
        actions.next()

    # ----- Line commands -----
    def line_swap_up():
        actions.user.vscode("editor.action.moveLinesUpAction")

    def line_swap_down():
        actions.user.vscode("editor.action.moveLinesDownAction")

    def line_clone():
        actions.user.vscode("editor.action.copyLinesDownAction")

    def line_insert_up():
        actions.user.vscode("editor.action.insertLineBefore")

    # Don't use RPC since some vscode extension(eg markdown) has specific behavior on enter
    # def line_insert_down():
    # actions.user.vscode("editor.action.insertLineAfter")

    def delete_line():
        actions.user.vscode("editor.action.deleteLines")

    def extend_line(n: int):
        actions.user.vscode("andreas.selectTo", n)

    def jump_line(n: int):
        actions.user.vscode("workbench.action.gotoLine")
        actions.insert(str(n))
        actions.key("enter")

    # ----- Indent -----
    def indent_more():
        actions.user.vscode("editor.action.indentLines")

    def indent_less():
        actions.user.vscode("editor.action.outdentLines")

    # ----- Zoom -----
    def zoom_reset():
        actions.user.vscode("workbench.action.zoomReset")


@ctx.action_class("user")
class UserActions:
    # ----- Navigation -----
    def go_back():
        actions.user.vscode("workbench.action.navigateBack")

    def go_forward():
        actions.user.vscode("workbench.action.navigateForward")

    def line_middle():
        actions.user.vscode("andreas.lineMiddle")

    # ----- Find / Replace -----
    def find_everywhere(text: str = None):
        actions.user.vscode("workbench.action.findInFiles")
        if text:
            actions.sleep("50ms")
            actions.insert(text)

    def find_file(text: str = None):
        actions.user.vscode("workbench.action.quickOpen")
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
    def tab_back():
        actions.user.vscode("workbench.action.openPreviousRecentlyUsedEditorInGroup")

    def tab_final():
        actions.user.vscode("workbench.action.lastEditorInGroup")

    def tab_jump(number: int):
        actions.user.vscode("andreas.openEditorAtIndex", number - 1)

    def tab_jump_from_back(number: int):
        actions.user.vscode("andreas.openEditorAtIndex", -number)

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
        actions.user.vscode("editorScroll", {"to": "up", "by": "halfPage"})

    def scroll_down_half_page():
        actions.user.vscode("editorScroll", {"to": "down", "by": "halfPage"})

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
    def dictation_get_context() -> tuple[str, str]:
        context = actions.user.vscode_get("andreas.getDictationContext")
        if context is not None:
            return (context["before"], context["after"])
        return (None, None)

    # ----- Snippets -----
    def insert_snippet(snippet: str):
        # actions.user.cursorless_insert_snippet(snippet)
        actions.user.vscode("editor.action.insertSnippet", {"snippet": snippet})


# @ctx_notebook.action_class("main")
# class NotebookMainActions:
#     def insert(text: str):
#         if not text:
#             return
#         if text.endswith("\n"):
#             print(f"'{text}'")
#             print(f"'{text[0:-1]}'")
#             actions.next(text[0:-1])
#             actions.user.vscode("notebook.cell.executeAndInsertBelow")
#         else:
#             actions.next(text)


@ctx_notebook.action_class("user")
class NotebookUserActions:
    def change_language(language: str = ""):
        if language:
            actions.insert(language)


@ctx_notebook.action_class("edit")
class NotebookEditActions:
    # ----- Line commands -----
    def line_swap_up():
        actions.user.vscode("notebook.cell.moveUp")

    def line_swap_down():
        actions.user.vscode("notebook.cell.moveDown")


@mod.action_class
class Actions:
    def jump_line_character(l: int, c: int):
        """Move cursor to line <l> and character <c>"""
        actions.user.vscode("workbench.action.gotoLine")
        actions.insert(f"{l}:{c}")
        actions.key("enter")

    def save_without_formatting():
        """Save current document without formatting"""
        actions.user.vscode("hideSuggestWidget")
        actions.user.vscode("workbench.action.files.saveWithoutFormatting")

    def format_document():
        """Format document"""
        actions.user.vscode("editor.action.formatDocument")

    def vscode_find_recent(text: str = None):
        """Find recent session, directory or file"""
        actions.user.vscode("workbench.action.openRecent")
        if text:
            actions.sleep("150ms")
            actions.insert(text)

    def git_open_remote_file_url(use_selection: bool, use_branch: bool):
        """Open remote git file in browser"""
        url = actions.user.vscode_get(
            "andreas.getGitFileURL",
            {"useSelection": use_selection, "useBranch": use_branch},
        )
        if url:
            actions.user.browser_open(url)

    def git_copy_remote_file_url(use_selection: bool, use_branch: bool):
        """Copy remote git file URL to clipboard"""
        url = actions.user.vscode_get(
            "andreas.getGitFileURL",
            {"useSelection": use_selection, "useBranch": use_branch},
        )
        if url:
            actions.clip.set_text(url)

    def git_open_url(command: str):
        """Open remote repository in browser"""
        url = actions.user.vscode_get(f"andreas.getGit{command}URL")
        if url:
            actions.user.browser_open(url)

    def git_copy_markdown_remote_file_url(targets: list):
        """Copy remote git file URL to clipboard as markdown link"""
        use_selection = False

        # The second target is optional and is used for getting the text
        if len(targets) == 2:
            texts = texts = actions.user.c_get_texts(targets[1])
            text = "".join(texts)
            use_selection = True

        # The first target is the source of the git url
        actions.user.cursorless_command("setSelection", targets[0])

        # If the second target is omitted used the selected text
        if len(targets) == 1:
            text = actions.edit.selected_text()

        url = actions.user.vscode_get(
            "andreas.getGitFileURL",
            {"useSelection": use_selection, "useBranch": False},
        )
        if url and text:
            actions.clip.set_text(f"[`{text}`]({url})")

    def git_find_branch(text: str = None):
        """Fined git branch"""
        actions.user.vscode("git.checkout")
        if text:
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
            actions.user.vscode("editor.action.addSelectionToNextFindMatch")

        # Select all instances
        if repeats < 0:
            actions.user.vscode("editor.action.selectHighlights")

    def change_language(language: str = ""):
        """Change language mode"""
        actions.user.vscode("workbench.action.editor.changeLanguageMode")
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
        actions.user.vscode(
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


def is_untitled(filename: str):
    return UNTITLED_RE.search(filename) is not None


def get_untitled_name(filename: str):
    return UNTITLED_RE.search(filename).group()
