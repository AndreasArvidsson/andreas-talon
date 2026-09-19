from talon import Module, actions, ui

mod = Module()


def focus_app_or_cycle_window(app: ui.App):
    # Focus next window on same app
    if app == ui.active_app():
        actions.app.window_next()
    # Focus new app
    else:
        actions.apps.focus(app)
    actions.user.help_running_apps_hide()


@mod.action_class
class Actions:
    def window_focus_last():
        """Switch focus to last window"""
        actions.key("alt-tab")

    @staticmethod
    def window_focus_name(name: str):
        """Focus application named <name>"""
        app = actions.user.get_app(name)
        focus_app_or_cycle_window(app)

    @staticmethod
    def focus_number(number: int):
        """Focus application number <number>"""
        apps = list(actions.apps.running().values())
        if number > 0 and number <= len(apps):
            app = apps[number - 1]
            focus_app_or_cycle_window(app)

    def window_switcher_menu():
        """Show window switcher menu"""
        actions.key("super-tab")

    def focus_desktop():
        """Focus desktop"""
        actions.key("super-d")
