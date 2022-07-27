from talon import Module, Context, actions, ui
from talon.clip import MimeData

mod = Module()
ctx = Context()
mod.tag("draft_editor_active", "Indicates whether the draft editor has been activated")

ctx.matches = r"""
app: vscode
"""

original_window = None
original_selected_text = None
last_draft_mime = None


@mod.action_class
class Actions:
    def draft_editor_open():
        """Open draft editor"""
        global original_window, original_selected_text
        original_window = ui.active_window()
        editor_app = get_editor_app()
        original_selected_text = get_text()
        actions.user.focus_app(editor_app)
        # Wait for context to change.
        actions.sleep("100ms")
        actions.app.tab_open()
        if original_selected_text:
            actions.insert(original_selected_text)
        ctx.tags = ["user.draft_editor_active"]

    def draft_editor_submit():
        """Submit/save draft editor"""
        global last_draft_mime
        mime = use_preview_to_get_mime_data()

        if mime and "PLACEHOLDER" in mime.text:
            actions.edit.select_none()
            actions.user.notify("Placeholder text found")
            return

        last_draft_mime = mime
        close_editor_and_focus_back()

        # Some applications like slack(browser) have a problem with pasting over selected text.
        if original_selected_text:
            actions.edit.delete()

        actions.user.draft_editor_paste_last()

    def draft_editor_discard():
        """Discard draft editor"""
        global last_draft_mime
        last_draft_mime = None
        close_editor_and_focus_back()

    def draft_editor_paste_last():
        """Paste last submitted draft"""
        if last_draft_mime:
            actions.user.paste_mime(last_draft_mime)


def get_editor_app() -> ui.App:
    editor_names = {"Visual Studio Code", "Code", "VSCodium", "Codium", "code-oss"}
    for app in ui.apps(background=False):
        if app.name in editor_names:
            return app
    raise RuntimeError("VSCode is not running")


def close_editor_and_focus_back():
    ctx.tags = []
    actions.edit.select_all()
    actions.edit.delete()
    actions.app.tab_close()
    actions.user.focus_window(original_window)


def use_preview_to_get_mime_data() -> MimeData or None:
    """Open markdown preview and copy to get html mime data"""
    actions.user.vscode("markdown.showPreview")
    actions.sleep("50ms")
    actions.user.vscode("workbench.action.focusActiveEditorGroup")
    actions.sleep("50ms")
    actions.edit.select_all()
    mime = actions.user.selected_mime()
    actions.app.tab_close()
    return mime


def get_text() -> str:
    """Try to convert known mime types to markdown. Default to plaintext."""
    mime = actions.user.selected_mime()
    if not mime:
        return ""
    mime_text = actions.user.slack_mime_to_markdown(mime)
    if mime_text:
        return mime_text
    return mime.text
