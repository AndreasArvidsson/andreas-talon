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
    def go_home():              key("alt-home")
    def open_private_window():  key("ctrl-shift-p")
    def reload():               key("ctrl-r")
    def reload_hard():          key("ctrl-shift-r")
    def show_clear_cache():     key("ctrl-shift-delete")
    def show_downloads():       key("ctrl-j")
    def show_extensions():      key("ctrl-shift-a")
    def show_history():         key("ctrl-h")
    def toggle_dev_tools():     key("ctrl-shift-i")
    def go(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        key("enter")


@ctx.action_class("app")
class AppActions:
    def tab_detach():
        key("escape ctrl-alt-M")
    def preferences():
        actions.user.browser_open("about:preferences")


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            key(f"ctrl-{number}")

    def tab_final():    key("ctrl-9")
    def tab_back():     key("escape ctrl-alt-N")

    def browser_open(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        key("alt-enter")

    # ----- Scroll -----
    def scroll_up():                key("ctrl-alt-h")
    def scroll_down():              key("ctrl-alt-j")
    def scroll_left():              key("ctrl-alt-k")
    def scroll_right():             key("ctrl-alt-l")
    def scroll_up_page():           key("pageup")
    def scroll_down_page():         key("pagedown")
    def scroll_up_half_page():      key("alt-pageup")
    def scroll_down_half_page():    key("alt-pagedown")


# ----- LINUX -----

ctx_linux = Context()
ctx_linux.matches = r"""
os: linux
app: firefox
"""

@ctx_linux.action_class("user")
class UserActionsLinux:
    def tab_final():    key("alt-9")
    def tab_jump(number: int):
        if number < 9:
            key(f"alt-{number}")
