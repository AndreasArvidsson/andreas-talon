from talon import Module, Context, actions, ui

mod = Module()
ctx = Context()
mod.tag("draft_editor_active", "Indicates whether the draft editor has been activated")

ctx.matches = r"""
app: vscode
"""

original_window = None
original_selected_text = None
last_draft = None


@mod.action_class
class Actions:
    def draft_editor_open():
        """Open draft editor"""
        global original_window, original_selected_text
        original_window = ui.active_window()
        editor_app = get_editor_app()
        original_selected_text = actions.edit.selected_text()
        actions.user.focus_app(editor_app)
        # Wait for context to change.
        actions.sleep("100ms")
        actions.app.tab_open()
        if original_selected_text:
            actions.insert(original_selected_text)
        ctx.tags = ["user.draft_editor_active"]

    def draft_editor_submit():
        """Submit/save draft editor"""
        close_editor(submit_draft=True)

    def draft_editor_discard():
        """Discard draft editor"""
        close_editor(submit_draft=False)

    def draft_editor_paste_last():
        """Paste last submitted draft"""
        if last_draft:
            actions.insert(last_draft)


def get_editor_app() -> ui.App:
    editor_names = {"Visual Studio Code", "Code"}
    for app in ui.apps(background=False):
        if app.name in editor_names:
            return app
    raise RuntimeError("VSCode is not running")


def close_editor(submit_draft: bool):
    global last_draft

    if not actions.win.filename().startswith("Untitled-"):
        return

    if submit_draft:
        last_draft = actions.user.vscode_get("andreas.getDocumentText")

        if last_draft and "PLACEHOLDER" in last_draft:
            actions.user.notify("Placeholder text found")
            return
    else:
        last_draft = None

    ctx.tags = []
    actions.user.vscode("workbench.action.revertAndCloseActiveEditor")
    actions.user.focus_window(original_window)

    if submit_draft:
        # Some applications like slack(browser) have a problem with pasting over selected text.
        if original_selected_text:
            actions.edit.delete()

        actions.insert(last_draft)
