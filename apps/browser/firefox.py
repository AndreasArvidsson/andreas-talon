from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.firefox = """
os: windows
and app.name: Firefox
os: windows
and app.exe: firefox.exe
"""

ctx.matches = r"""
app: firefox
"""

mod.list("rango_with_target_action", desc="List of Rango actions used WITH a target")
mod.list(
    "rango_without_target_action", desc="List of Rango actions used WITHOUT a target"
)

ctx.lists["user.rango_with_target_action"] = {
    "click": "clickElement",
    "open": "openInNewTab",
    "stash": "openInBackgroundTab",
    "show": "showLink",
    "hover": "hoverElement",
    "copy": "copyLink",
    "copy mark": "copyMarkdownLink",
    "copy text": "copyElementTextContent",
    "crown": "scrollElementToTop",
    "bottom": "scrollElementToBottom",
    "center": "scrollElementToCenter",
    "upper": "scrollUpAtElement",
    "downer": "scrollDownAtElement",
}

ctx.lists["user.rango_without_target_action"] = {
    "rango single": "includeSingleLetterHints",
    "rango double": "excludeSingleLetterHints",
    "hunt": "toggleHints",
    "hunt refresh": "refreshHints",
    "hover nothing": "unhoverAll",
    "tab clone": "cloneCurrentTab",
    "upper again": "scrollUpAtElement",
    "downer again": "scrollDownAtElement",
}


@ctx.action_class("browser")
class BrowserActions:
    def open_private_window():
        actions.key("ctrl-shift-p")

    def show_extensions():
        actions.key("ctrl-shift-a")


@ctx.action_class("app")
class AppActions:
    def preferences():
        actions.user.browser_open_new_tab("about:preferences")

    # ----- Vimium -----
    def tab_detach():
        actions.key("escape ctrl-alt-M")


@ctx.action_class("edit")
class EditActions:
    def find(text: str = None):
        actions.key("ctrl-f")
        if text:
            actions.sleep("50ms")
            actions.insert(text)


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            actions.key(f"ctrl-{number}")

    def tab_final():
        actions.key("ctrl-9")

    def browser_open_new_tab(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        actions.key("alt-enter")

    # ----- Vimium -----
    def tab_back():
        actions.key("escape ctrl-alt-N")

    def scroll_left():
        actions.key("ctrl-alt-k")

    def scroll_right():
        actions.key("ctrl-alt-l")

    # ----- Rango -----
    def scroll_up():
        actions.user.rango_command_without_target("scrollUpPage", 0.1)

    def scroll_down():
        actions.user.rango_command_without_target("scrollDownPage", 0.1)

    def scroll_up_half_page():
        actions.user.rango_command_without_target("scrollUpPage", 0.45)

    def scroll_down_half_page():
        actions.user.rango_command_without_target("scrollDownPage", 0.45)

    def scroll_up_page():
        actions.user.rango_command_without_target("scrollUpPage", 0.9)

    def scroll_down_page():
        actions.user.rango_command_without_target("scrollDownPage", 0.9)


# ----- LINUX -----

ctx_linux = Context()
ctx_linux.matches = r"""
os: linux
app: firefox
"""


@ctx_linux.action_class("user")
class UserActionsLinux:
    def tab_final():
        actions.key("alt-9")

    def tab_jump(number: int):
        if number < 9:
            actions.key(f"alt-{number}")
