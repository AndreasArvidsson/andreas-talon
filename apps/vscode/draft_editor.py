from talon import Module, actions, ui

mod = Module()
mod.mode("draft_editor", "Indicates whether the draft editor has been activated")

active_window = None

@mod.action_class
class Actions:
    def draft_editor_open():
        """Open draft editor"""
        global active_window
        active_window = ui.active_window()
        editor = get_editor()
        selected_text = actions.edit.selected_text()
        actions.user.focus_window(editor)
        # Wait for context to change.
        actions.sleep("100ms")
        actions.app.tab_open()
        if selected_text != "":
            actions.user.paste(selected_text)
        actions.mode.enable("user.draft_editor")

    def draft_editor_submit():
        """Submit/save draft editor"""
        close_editor(submit_draft=True)

    def draft_editor_discard():
        """Discard draft editor"""
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
    selected_text = actions.edit.selected_text()
    actions.edit.delete()
    actions.app.tab_close()
    actions.user.focus_window(active_window)
    if submit_draft:
        actions.user.paste(selected_text)
