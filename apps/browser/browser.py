from talon import Module, Context, actions, app

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: browser
"""

browser_name = "Firefox" if app.platform == "windows" else "firefox"

mod.list("domain", "List of top level domains")


@ctx.action_class("browser")
class BrowserActions:
    def focus_address():
        actions.key("ctrl-l")

    def go_home():
        actions.key("alt-home")

    def go(url: str):
        actions.browser.focus_address()
        actions.sleep("100ms")
        actions.insert(url)
        actions.key("enter")

    def focus_search():
        actions.focus_address()

    def submit_form():
        actions.key("enter")

    def go_back():
        actions.key("alt-left")

    def go_forward():
        actions.key("alt-right")

    def reload():
        actions.key("ctrl-r")

    def reload_hard():
        actions.key("ctrl-shift-r")

    def toggle_dev_tools():
        actions.key("ctrl-shift-i")

    def show_history():
        actions.key("ctrl-h")

    def show_downloads():
        actions.key("ctrl-j")

    def bookmark():
        actions.key("ctrl-d")

    def bookmarks():
        actions.key("ctrl-shift-O")

    def bookmarks_bar():
        actions.key("ctrl-shift-b")

    def bookmark_tabs():
        actions.key("ctrl-shift-d")

    def show_clear_cache():
        actions.key("ctrl-shift-delete")


@ctx.action_class("edit")
class EditActions:
    def file_end():
        actions.key("ctrl-end")


@ctx.action_class("user")
class UserActions:
    def go_back():
        actions.browser.go_back()

    def go_forward():
        actions.browser.go_forward()

    def command_server_directory() -> str:
        return "talon-browser-command-server"


@mod.action_class
class Actions:
    def browser_focus_default():
        """Focus default browser"""
        actions.user.window_focus_name(browser_name)

    def browser_copy_address():
        """Browser copy address"""
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.edit.copy()

    def browser_open_new_tab(url: str):
        """Open url in new tab"""

    def browser_open(url: str):
        """Focus browser and open url"""
        if actions.app.name() != browser_name:
            actions.user.browser_focus_default()
            actions.sleep("50ms")
        actions.user.browser_open_new_tab(url)

    def browser_search(text: str):
        """Focus browser and search for <text>"""
        # Prefix with space to avoid matching search text with history
        actions.user.browser_open(f" {text}")

    def browser_search_selected():
        """Focus browser and search for selected text"""
        text = actions.edit.selected_text().strip()
        if text:
            actions.user.browser_search(text)

    def browser_translate(text: str):
        """Focus browser and translate <text>"""
        actions.user.browser_open(
            f"https://translate.google.com/?sl=en&tl=sv&text={text}"
        )

    def browser_translate_selected():
        """Focus browser and translate selected text"""
        text = actions.edit.selected_text()
        actions.user.browser_translate(text)

    def browser_define(text: str):
        """Focus browser and define phrase <text>"""
        actions.user.browser_open(f"https://www.merriam-webster.com/dictionary/{text}")

    def browser_define_selected():
        """Focus browser and define selected text"""
        text = actions.edit.selected_text()
        actions.user.browser_define(text)
