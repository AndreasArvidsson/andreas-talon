from talon import Module, Context, actions, app
key = actions.key
ctx = Context()
mod = Module()
apps = mod.apps

apps.firefox = "app.name: Firefox"
apps.firefox = "app.name: firefox"
apps.firefox = """
os: windows
and app.name: Firefox
os: windows
and app.exe: firefox.exe
"""
apps.firefox = """
os: mac
and app.bundle: org.mozilla.firefox
"""

ctx.matches = r"""
app: firefox
"""


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            key(f"ctrl-{number}")

    def tab_final():    key("ctrl-9")
    def tab_mute():     key("ctrl-m")


@ctx.action_class("browser")
class BrowserActions:
    def go(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        key("enter")

    def focus_search():     actions.focus_address()
    def submit_form():      key("enter")
    def bookmark():         key("ctrl-d")
    def bookmark_tabs():    key("ctrl-shift-d")
    def bookmarks():        key("ctrl-shift-b")

    def bookmarks_bar():
        key("alt-v")
        actions.sleep("50ms")
        key("t")
        actions.sleep("50ms")
        key("b")

    def focus_address():        key("ctrl-l")
    def go_blank():             key("ctrl-n")
    def go_back():              key("alt-left")
    def go_forward():           key("alt-right")
    def go_home():              key("alt-home")
    def open_private_window():  key("ctrl-shift-p")
    def reload():               key("ctrl-r")
    def reload_hard():          key("ctrl-shift-r")
    def show_clear_cache():     key("ctrl-shift-delete")
    def show_downloads():       key("ctrl-j")
    def show_extensions():      key("ctrl-shift-a")
    def show_history():         key("ctrl-h")
    def toggle_dev_tools():     key("ctrl-shift-i")
