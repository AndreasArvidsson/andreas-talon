from talon import Module, actions, ui

mod = Module()
active_window = None
editor = None

@mod.action_class
class Actions:
    def draft_editor_open():
        """Open draft editor"""
        global active_window, editor
        active_window = ui.active_window()
        editor = get_editor()
        has_selected_text = actions.edit.selected_text() != ""
        if has_selected_text:
            actions.edit.copy()
        actions.edit.copy()
        actions.user.focus_window(editor)
        new_file()
        if has_selected_text:
            actions.edit.paste()

    def draft_editor_save():
        """Save draft editor"""
        global active_window, editor
        if not active_window or ui.active_window() != editor:
            return
        actions.edit.select_all()
        actions.edit.copy()
        close_file()
        actions.user.focus_window(active_window)
        actions.edit.paste()
        active_window = None
        editor = None

    def draft_editor_discard():
        """Discard draft editor"""
        global active_window, editor
        if not active_window or ui.active_window() != editor:
            return
        actions.edit.select_all()
        close_file()
        actions.user.focus_window(active_window)
        active_window = None
        editor = None


def get_editor():
    editor_names = {
        "Visual Studio Code",
        "Code",
        "VSCodium",
        "Codium",
        "code-oss"
    }
    for w in ui.windows():
        if w.app.name in editor_names:
            return w
    raise RuntimeError("VSCode is not running")

def new_file():
    actions.user.vscode("workbench.action.files.newUntitledFile")

def close_file():
    actions.edit.delete()
    actions.app.tab_close()