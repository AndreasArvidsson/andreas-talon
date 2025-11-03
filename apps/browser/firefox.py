from talon import Module, Context, actions
import re

mod = Module()
ctx = Context()

mod.apps.firefox = r"""
os: windows
and app.exe: firefox.exe
os: windows
and app.exe: librewolf.exe
os: windows
and app.exe: waterfox.exe
"""

ctx.matches = r"""
app: firefox
"""

mod.list("rango_with_target_action", "List of Rango actions used WITH a target")
mod.list("rango_without_target_action", "List of Rango actions used WITHOUT a target")

# https://github.com/david-tejada/rango
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
    "hunt include": "includeExtraSelectors",
    "hunt exclude": "excludeExtraSelectors",
}

ctx.lists["user.rango_without_target_action"] = {
    "rango single": "includeSingleLetterHints",
    "rango double": "excludeSingleLetterHints",
    "hunt on": "toggleHints",
    "hunt off": "toggleHints",
    "hunt refresh": "refreshHints",
    "hover nothing": "unhoverAll",
    "upper again": "scrollUpAtElement",
    "downer again": "scrollDownAtElement",
    "hunt extra": "displayExtraHints",
    "hunt more": "displayExcludedHints",
    "hunt less": "displayLessHints",
    "hunt save": "confirmSelectorsCustomization",
    "hunt reset": "resetCustomSelectors",
    "hunt bigger": "increaseHintSize",
    "hunt smaller": "decreaseHintSize",
    "hunt some more": "includeOrExcludeMoreSelectors",
    "hunt some less": "includeOrExcludeLessSelectors",
}

url_pattern = re.compile(r"https?://\S+")


@ctx.action_class("browser")
class BrowserActions:
    def address() -> str:
        # Rango adds address to window title
        title = actions.win.title()
        match = url_pattern.search(title)
        if match:
            return match.group()
        return ""

    def open_private_window():
        actions.key("ctrl-shift-p")

    def show_extensions():
        actions.key("ctrl-shift-a")


@ctx.action_class("app")
class AppActions:
    def preferences():
        actions.user.browser_open_new_tab("about:preferences")

    # ----- Rango -----
    def tab_detach():
        actions.user.rango_command_without_target("moveCurrentTabToNewWindow")


@ctx.action_class("edit")
class EditActions:
    def find(text: str = None):
        actions.key("ctrl-f")
        if text:
            actions.sleep("50ms")
            actions.insert(text)


@ctx.action_class("user")
class UserActions:
    def browser_copy_address():
        actions.user.rango_command_without_target("copyLocationProperty", "href")

    def browser_open_new_tab(url: str):
        actions.browser.focus_address()
        actions.sleep("50ms")
        actions.insert(url)
        actions.sleep("50ms")
        actions.key("alt-enter")

    # ----- Scrolling -----
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

    # ----- Tabs -----
    def tab_jump(number: int):
        if number < 9:
            actions.key(f"ctrl-{number}")

    def tab_final():
        actions.key("ctrl-9")

    def tab_back():
        actions.user.rango_command_without_target("focusPreviousTab")

    def tab_duplicate():
        actions.user.rango_command_without_target("cloneCurrentTab")

    def tab_close_others():
        actions.user.rango_command_without_target("closeOtherTabsInWindow")

    def tab_close_left():
        actions.user.rango_command_without_target("closeTabsToTheLeftInWindow")

    def tab_close_right():
        actions.user.rango_command_without_target("closeTabsToTheRightInWindow")


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
