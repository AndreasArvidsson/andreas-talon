from talon import Module, Context, actions, ui, ctrl

key = actions.key
insert = actions.insert
edit = actions.edit
vscode = actions.user.vscode

mod = Module()

mod.apps.vscode = """
os: linux
and app.name: Code
"""
mod.apps.vscode = """
os: windows
and app.name: Visual Studio Code
os: windows
and app.exe: Code.exe
"""


ctx = Context()
ctx.matches = r"""
app: vscode
"""

ctx_talon = Context()
ctx_talon.matches = r"""
app: vscode
tag: user.talon
"""


mod.list("vscode_panel", desc="Available panels for resizing in vscode")
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


@mod.capture(rule="{self.vscode_panel}")
def vscode_panel(m) -> dict:
    return panels[m.vscode_panel]


@ctx.action_class("win")
class WinActions:
    def filename():
        parts = actions.win.title().split(" - ")
        result = parts[1] if parts[0] == "[Extension Development Host]" else parts[0]
        if "." in result:
            return result
        return ""


@ctx.action_class("app")
class AppActions:
    def window_open():
        vscode("workbench.action.newWindow")

    def tab_open():
        vscode("workbench.action.files.newUntitledFile")

    def tab_previous():
        vscode("workbench.action.previousEditorInGroup")

    def tab_next():
        vscode("workbench.action.nextEditorInGroup")

    def preferences():
        vscode("workbench.action.openGlobalSettings")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        vscode("editor.action.commentLine")

    def complete():
        vscode("editor.action.triggerSuggest")


@ctx.action_class("edit")
class EditActions:
    def select_none():
        key("escape")

    # ----- Word -----
    def select_word():
        vscode("editor.action.addSelectionToNextFindMatch")

    def delete_word():
        empty_selection()
        actions.next()

    # ----- Line commands -----
    def line_swap_up():
        vscode("editor.action.moveLinesUpAction")

    def line_swap_down():
        vscode("editor.action.moveLinesDownAction")

    def line_clone():
        vscode("editor.action.copyLinesDownAction")

    def line_insert_up():
        vscode("editor.action.insertLineBefore")

    def line_insert_down():
        vscode("editor.action.insertLineAfter")

    def delete_line():
        vscode("editor.action.deleteLines")

    def extend_line(n: int):
        vscode("andreas.selectTo", n)

    def jump_line(n: int):
        vscode("workbench.action.gotoLine")
        insert(n)
        key("enter")

    # ----- Indent -----
    def indent_more():
        vscode("editor.action.indentLines")

    def indent_less():
        vscode("editor.action.outdentLines")

    # ----- Save -----
    def save():
        actions.user.stop_app()
        actions.next()

    # ----- Zoom -----
    def zoom_reset():
        vscode("workbench.action.zoomReset")

    # ----- Find -----
    def find_previous():
        key("shift-f4")

    def find_next():
        key("f4")

    # ----- Miscellaneous -----
    def selected_text() -> str:
        return actions.user.vscode_get("andreas.getSelectedText")


@ctx.action_class("user")
class UserActions:
    # ----- Navigation -----
    def go_back():
        vscode("workbench.action.navigateBack")

    def go_forward():
        vscode("workbench.action.navigateForward")

    def line_middle(n: int = None):
        if n:
            edit.jump_line(n)
        vscode("andreas.lineMiddle")

    # ----- Find / Replace -----
    def find_everywhere(text: str = None):
        vscode("workbench.action.findInFiles")
        if text:
            actions.sleep("50ms")
            insert(text)

    def find_file(text: str = None):
        vscode("workbench.action.quickOpen")
        if text:
            actions.sleep("50ms")
            insert(text)

    def find_toggle_match_by_case():
        key("alt-c")

    def find_toggle_match_by_word():
        key("alt-w")

    def find_toggle_match_by_regex():
        key("alt-r")

    def find_replace_toggle_preserve_case():
        key("alt-p")

    def find_replace_confirm():
        key("enter")

    def find_replace_confirm_all():
        key("ctrl-alt-enter")

    # ----- Tabs -----
    def tab_back():
        vscode("workbench.action.openPreviousRecentlyUsedEditor")

    def tab_final():
        vscode("workbench.action.lastEditorInGroup")

    def tab_jump(number: int):
        vscode("workbench.action.openEditorAtIndex", number - 1)

    # ----- Scroll -----
    def scroll_up():
        key("ctrl-up")

    def scroll_down():
        key("ctrl-down")

    def scroll_up_page():
        key("alt-pageup")

    def scroll_down_page():
        key("alt-pagedown")

    def scroll_up_half_page():
        vscode("editorScroll", {"to": "up", "by": "halfPage"})

    def scroll_down_half_page():
        vscode("editorScroll", {"to": "down", "by": "halfPage"})

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


@ctx_talon.action_class("user")
class TalonUserActions:
    # ----- Format -----
    def format_document():
        vscode("andreas.formatDocument")


@ctx_talon.action_class("edit")
class TalonEditActions:
    def save():
        actions.user.format_document()
        actions.next()


@mod.action_class
class Actions:
    def jump_line_character(l: int, c: int):
        """Move cursor to line <l> and character <c>"""
        vscode("workbench.action.gotoLine")
        insert(f"{l}:{c}")
        key("enter")

    def format_document():
        """Format document"""
        vscode("editor.action.formatDocument")

    def vscode_find_recent(text: str = None, sleep: bool = False):
        """Find recent session, directory or file"""
        vscode("workbench.action.openRecent")
        if text or sleep:
            actions.sleep("50ms")
        if text:
            insert(text)

    def git_open_working_file_url(line_number: bool = False):
        """Open current file in in git webpage"""
        url = actions.user.vscode_get("andreas.git.getURL", line_number)
        if url:
            actions.user.browser_focus_open(url)

    def git_copy_working_file_url(line_number: bool = False):
        """Copy current file URL to clipboard"""
        url = actions.user.vscode_get("andreas.git.getURL", line_number)
        if url:
            actions.clip.set_text(url)

    def vscode_take_word(cursorless_target: dict, repeats: int):
        """Take word on cursorless target with number of repeats"""
        actions.user.cursorless_simple_action("setSelection", cursorless_target)
        for _ in range(repeats):
            actions.edit.select_word()

    def vscode_resize_panel(panel: dict, size: str):
        """Resize vscode sidebar/panel"""
        actions.user.mouse_center_window()
        actions.sleep(0.2)
        ok, x, y = actions.user.locate_drag(panel["filename"], panel["position"])
        if ok:
            if size == "small":
                ratio = 0.2
            elif size == "medium":
                ratio = 0.3
            elif size == "large":
                ratio = 0.4
            window = ui.active_window()
            screen_size = min(window.screen.width, window.screen.height)
            if panel["xDirection"]:
                x = window.rect.x + screen_size * ratio
            else:
                y = window.rect.y + window.rect.height - screen_size * ratio
            ctrl.mouse_move(x, y)
            actions.sleep(0.1)
            ctrl.mouse_click(button=0, up=True)

    def vscode_grab_line(panel: dict):
        """Grab vscode sideboard/panel line to resize"""
        actions.user.locate_drag(panel["filename"], panel["position"])


def empty_selection():
    if edit.selected_text():
        edit.right()
