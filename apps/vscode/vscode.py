from talon import Context, actions, Module, app
key = actions.key
insert = actions.insert
edit = actions.edit
vscode = actions.user.vscode

mod = Module()

mod.apps.vscode = """
os: linux
and app.name: Code
os: linux
and app.name: code-oss
os: linux
and app.name: VSCodium
os: linux
and app.name: Codium
"""
mod.apps.vscode = """
os: windows
and app.name: Visual Studio Code
os: windows
and app.exe: Code.exe
os: windows
and app.name: VSCodium
os: windows
and app.exe: VSCodium.exe
"""


ctx = Context()
ctx.matches = r"""
app: vscode
"""

ctx_talon = Context()
ctx_talon.matches = r"""
app: vscode
and mode: user.talon
app: vscode
and mode: user.auto_lang
and code.language: talon
"""

mod.list("vscode_actions", desc="List of vscode actions")
ctx.lists["self.vscode_actions"] = {
    "go": "go",
    "before": "before",
    "after": "after",
    "select": "select",
    "copy": "copy",
    "extend": "extend",
    "scratch": "delete"
}


@ctx.action_class("win")
class WinActions:
    def filename():
        parts = actions.win.title().split(" - ")
        result = (parts[1]
                  if parts[0] == "[Extension Development Host]"
                  else parts[0])
        if "." in result:
            return result
        return ""


@ctx.action_class("app")
class AppActions:
    def window_open():          vscode("workbench.action.newWindow")
    def tab_open():             vscode("workbench.action.files.newUntitledFile")


@ctx.action_class("code")
class CodeActions:
    def complete():             vscode("editor.action.triggerSuggest")


@ctx.action_class("edit")
class EditActions:
    def select_none():          key("escape")

    # ----- Line commands -----
    def line_swap_up():         vscode("editor.action.moveLinesUpAction")
    def line_swap_down():       vscode("editor.action.moveLinesDownAction")
    def line_clone():           vscode("editor.action.copyLinesDownAction")
    def line_insert_up():       vscode("editor.action.insertLineBefore")
    def line_insert_down():     vscode("editor.action.insertLineAfter")
    def delete_line():          vscode("editor.action.deleteLines")
    def extend_line(n: int):    vscode("andreas.selectTo", n)

    def jump_line(n: int):
        vscode("workbench.action.gotoLine")
        insert(n)
        key("enter")

    # ----- Indent -----
    def indent_more():          vscode("editor.action.indentLines")
    def indent_less():          vscode("editor.action.outdentLines")

    # ----- Save -----
    def save():
        actions.user.stop_app()
        actions.next()

    # ----- Zoom -----
    def zoom_reset():           vscode("workbench.action.zoomReset")


@ctx.action_class("user")
class UserActions:
    # ----- Navigation -----
    def declaration_go():       vscode("editor.action.goToReferences")
    def definition_go():        vscode("editor.action.revealDefinition")
    def definition_peek():      vscode("editor.action.peekDefinition")
    def definition_split():     vscode("editor.action.revealDefinitionAside")
    def references_go():        vscode("editor.action.goToReferences")
    def references_peek():      vscode("editor.action.referenceSearch.trigger")

    def line_middle(n: int = None):
        if n:
            edit.jump_line(n)
        vscode("andreas.lineMiddle")

    # ----- Find / Replace -----
    def find_all(text: str = None):
        vscode("workbench.action.findInFiles")
        if text:
            insert(text)

    def find_file(text: str = None):
        vscode("workbench.action.quickOpen")
        if text:
            actions.sleep("50ms")
            insert(text)

    def find_recent(text: str = None):
        vscode("workbench.action.openRecent")
        if text:
            insert(text)

    def find_replace_word():    key("enter")
    def find_replace_all():     key("ctrl-alt-enter")

    # ----- Run -----
    def run_program():          vscode("workbench.action.debug.run")
    def debug_program():        vscode("workbench.action.debug.start")
    def debug_breakpoint():     vscode("editor.debug.action.toggleBreakpoint")
    def debug_continue():       vscode("workbench.action.debug.continue")
    def debug_step_over():      vscode("workbench.action.debug.stepOver")
    def debug_step_into():      vscode("workbench.action.debug.stepInto")
    def debug_step_out():       vscode("workbench.action.debug.stepOut")
    def debug_restart():        vscode("workbench.action.debug.restart")
    def debug_pause():          vscode("workbench.action.debug.pause")
    def debug_stop():           vscode("workbench.action.debug.stop")

    # ----- Tabs -----
    def quick_fix():            vscode("editor.action.quickFix")
    def tab_final():            key("alt-0")

    def tab_jump(number: int):
        if number < 10:
            key(f"alt-{number}")

    # ----- Format -----
    def format_document():      vscode("editor.action.formatDocument")
    def format_selection():     vscode("editor.action.formatSelection")

    # ----- Comments -----
    def comment():              vscode("editor.action.addCommentLine")
    def uncomment():            vscode("editor.action.removeCommentLine")

    # ----- Scroll -----
    def scroll_up():             key("ctrl-up")
    def scroll_down():           key("ctrl-down")
    # def scroll_left():           key(ctrl-alt-k)
    # def scroll_right():          key(ctrl-alt-l)
    def scroll_up_page():         key("alt-pageup")
    def scroll_down_page():       key("alt-pagedown")

    def scroll_up_half_page():
        vscode("editorScroll", {"to": "up", "by": "halfPage"})
    def scroll_down_half_page():
        vscode("editorScroll", {"to": "down", "by": "halfPage"})

    # ----- Miscellaneous -----
    def open_settings():        vscode("workbench.action.openGlobalSettings")


@ctx_talon.action_class("user")
class TalonUserActions:
    # ----- Format -----
    def format_document():      vscode("andreas.formatDocument")
    def format_selection():     actions.skip()


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
