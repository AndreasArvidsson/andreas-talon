from talon import Module, actions
import os


mod = Module()


@mod.action_class
class Actions:
    def cursorless_use_release():
        """Use main branch of cursorless-talon"""
        switch_folder(f"{actions.path.user_home()}\\cursorless-talon")

    def cursorless_use_develop():
        """Use developed folder of cursorless-talon"""
        switch_folder(f"{actions.path.user_home()}\\cursorless\\cursorless-talon")

    def cursorless_browser_open_target(target: dict):
        """Search for target text in browser"""
        texts = actions.user.cursorless_single_target_command_get(
            "getText",
            target,
        )
        text = " + ".join(texts)
        actions.user.browser_open(text)


def switch_folder(target: str):
    link = f"{actions.path.talon_user()}\\cursorless-talon"
    actions.user.debug(f"cmd /c mklink /d {link} {target}")
    os.system(f"cmd /c rmdir {link}")
    os.system(f"cmd /c mklink /d {link} {target}")
    actions.sleep("500ms")
    actions.user.talon_restart()
