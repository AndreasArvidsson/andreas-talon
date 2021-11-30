from talon import Module, Context, actions, ui

mod = Module()
ctx = Context()
mod.tag("draft_editor_active", "Indicates whether the draft editor has been activated")

ctx.matches = r"""
app: vscode
"""

original_window = None


@mod.action_class
class Actions:
    def draft_editor_open():
        """Open draft editor"""
        global original_window
        original_window = ui.active_window()
        editor_app = get_editor_app()
        selected_text = actions.edit.selected_text()
        actions.user.focus_app(editor_app)
        # Wait for context to change.
        actions.sleep("100ms")
        actions.app.tab_open()
        if selected_text:
            actions.insert(selected_text)
        ctx.tags = ["user.draft_editor_active"]

    def draft_editor_submit():
        """Submit/save draft editor"""
        close_editor(submit_draft=True)

    def draft_editor_discard():
        """Discard draft editor"""
        close_editor(submit_draft=False)


def get_editor_app() -> ui.App:
    editor_names = {"Visual Studio Code", "Code", "VSCodium", "Codium", "code-oss"}
    for app in ui.apps(background=False):
        if app.name in editor_names:
            return app
    raise RuntimeError("VSCode is not running")


def close_editor(submit_draft: bool):
    ctx.tags = []
    actions.edit.select_all()
    selected_text = actions.edit.selected_text()
    actions.edit.delete()
    actions.app.tab_close()
    actions.user.focus_window(original_window)
    if submit_draft:
        actions.insert(selected_text)
