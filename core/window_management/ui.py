from talon import Context, Module, ui, actions, ctrl
import time
import re

mod = Module()
ctx = Context()


@ctx.action_class("app")
class AppActions:
    def window_previous():
        cycle_windows(ui.active_app(), -1)

    def window_next():
        cycle_windows(ui.active_app(), 1)


@mod.action_class
class Actions:
    @staticmethod
    def get_app(name: str) -> ui.App:
        """Get application by name"""
        # Try to get application by name
        apps = [a for a in ui.apps(background=False) if a.name == name]

        # No application found for name
        if not apps:
            raise RuntimeError(f"App '{name}' not running")

        # Multiple hits on this application. Filter out invalid applications.
        if len(apps) > 1:
            apps2 = [a for a in apps if is_app_valid(a)]
            if apps2:
                return apps2[0]

        # Finally just pick the first application
        return apps[0]

    @staticmethod
    def get_app_window(app_name: str) -> ui.Window:
        """Get top window by application name"""
        app = actions.user.get_app(app_name)
        return app.windows()[0]

    def get_window_under_cursor() -> ui.Window:
        """Get the window under the mouse cursor"""
        x, y = ctrl.mouse_pos()
        windows = [
            w
            for w in ui.windows(hidden=False)
            if w.rect.contains(x, y) and is_window_valid(w) and is_app_valid(w.app)
        ]
        if not windows:
            raise ValueError("Can't find window under the mouse cursor")
        return windows[0]

    @staticmethod
    def send_key(key: str, app: ui.App):
        """Send key <key> to application"""
        active_app = ui.active_app()
        if active_app != app:
            actions.user.focus_app(app)
            actions.key(key)
            actions.user.focus_app(active_app)
        else:
            actions.key(key)

    @staticmethod
    def focus_app(app: ui.App):
        """Focus app and wait until finished"""
        app.focus()
        t1 = time.monotonic()
        while ui.active_app() != app:
            if time.monotonic() - t1 > 1:
                raise RuntimeError(f"Can't focus app: {app.name}")
            actions.sleep("50ms")

    @staticmethod
    def focus_window(window: ui.Window):
        """Focus window and wait until finished"""
        window.focus()
        t1 = time.monotonic()
        while ui.active_window() != window:
            if time.monotonic() - t1 > 1:
                raise RuntimeError(f"Can't focus window '{window.title}'")
            actions.sleep("50ms")

    @staticmethod
    def wait_for_title(title_pattern: str, timeout: float = 1.0):
        """Wait for a window title to match pattern"""
        t1 = time.monotonic()
        while re.search(title_pattern, actions.win.title()) is None:
            if time.monotonic() - t1 > timeout:
                raise RuntimeError(f"Can't find window with title: {title_pattern}")
            actions.sleep("50ms")

    @staticmethod
    def wait_for_title_change(timeout: float = 1.0):
        """Wait for a window title to change"""
        initial_title = actions.win.title()
        t1 = time.monotonic()
        while actions.win.title() == initial_title:
            if time.monotonic() - t1 > timeout:
                raise RuntimeError(f"Window title did not change from: {initial_title}")
            actions.sleep("50ms")


def cycle_windows(app, diff: int):
    """Cycle windows backwards or forwards for the given application"""
    active = app.active_window
    windows = [w for w in app.windows() if w == active or is_window_valid(w)]
    windows.sort(key=lambda w: w.id)
    current = windows.index(active)
    i = (current + diff) % len(windows)

    while i != current:
        try:
            actions.user.focus_window(windows[i])
            break
        except Exception as e:
            print(e)
            i = (i + diff) % len(windows)


def is_app_valid(app: ui.App) -> bool:
    """Returns true if this application is valid for focusing"""
    return (
        not app.background
        and not is_system_app(app)
        and is_window_valid(app.active_window)
    )


def is_window_valid(window: ui.Window) -> bool:
    """Returns true if this window is valid for focusing"""
    return (
        not window.hidden
        # On Windows, there are many fake windows with empty titles -- this excludes them.
        and window.title != ""
        # Exclude some windows that are technically valid but not actual windows, such as the "Chrome Legacy Window" which is used for rendering in Chrome and is not an actual window.
        and window.title != "Chrome Legacy Window"
        # This excludes many tiny windows that are not actual windows, and is a rough heuristic.
        and window.rect.width > window.screen.dpi
        and window.rect.height > window.screen.dpi
    )


def is_system_app(app: ui.App):
    return app.exe.startswith("C:\\WINDOWS\\SystemApps") or app.exe.startswith(
        "C:\\WINDOWS\\system32"
    )
