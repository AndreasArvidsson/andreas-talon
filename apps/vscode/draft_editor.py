from talon import Module, actions, ui

mod = Module()
mod.mode("draft_editor", "Mode to show if the draft editor is open")

active_window = None

@mod.action_class
class Actions:
    def draft_editor_open():
        """Open draft editor"""
        global active_window
        active_window = ui.active_window()
        editor = get_editor()
        has_selected_text = actions.edit.selected_text() != ""
        if has_selected_text:
            actions.edit.copy()
        actions.user.focus_window(editor)
        actions.user.vscode("workbench.action.files.newUntitledFile")
        if has_selected_text:
            actions.edit.paste()
        actions.mode.enable("user.draft_editor")

    def draft_editor_submit():
        """Submit/save draft"""
        close_editor(submit_draft=True)

    def draft_editor_discard():
        """Discard draft"""
        close_editor(submit_draft=False)

def get_editor():
    editor_names = {
        "Visual Studio Code",
        "Code",
        "VSCodium",
        "Codium",
        "code-oss"
    }
    for app in ui.apps(background=False):
        if app.name in editor_names:
            return app.windows()[0]
    raise RuntimeError("VSCode is not running")

def close_editor(submit_draft: bool):
    actions.mode.disable("user.draft_editor")
    actions.edit.select_all()
    if submit_draft:
        actions.edit.copy()
    actions.edit.delete()
    actions.app.tab_close()
    actions.user.focus_window(active_window)
    if submit_draft:
        actions.edit.paste()
