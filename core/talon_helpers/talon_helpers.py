from talon import (
    Module,
    Context,
    actions,
    app,
    registry,
    scope,
    ui,
    speech_system,
    storage,
)
import os
import re
import time
from itertools import islice
from typing import Any, Union
from talon.grammar import Phrase

mod = Module()

ctx_win = Context()
ctx_win.matches = r"""
os: windows
"""


@mod.action_class
class Actions:
    def talon_add_context_clipboard_python():
        """Adds os-specific context info to the clipboard for the focused app for .py files. Assumes you've a Module named mod declared."""
        friendly_name = actions.app.name()
        executable = actions.app.executable().split(os.path.sep)[-1]
        app_name = create_name(friendly_name)
        if app.platform == "mac":
            result = 'mod.apps.{} = """\nos: {}\nand app.bundle: {}\n"""'.format(
                app_name, app.platform, actions.app.bundle()
            )
        elif app.platform == "windows":
            result = 'mod.apps.{} = """\nos: windows\nand app.name: {}\nos: windows\nand app.exe: {}\n"""'.format(
                app_name, friendly_name, executable
            )
        else:
            result = 'mod.apps.{} = """\nos: {}\nand app.name: {}\n"""'.format(
                app_name, app.platform, friendly_name
            )

        actions.clip.set_text(result)

    def talon_add_context_clipboard():
        """Adds os-specific context info to the clipboard for the focused app for .talon files"""
        friendly_name = actions.app.name()
        executable = actions.app.executable().split(os.path.sep)[-1]
        if app.platform == "mac":
            result = "os: {}\nand app.bundle: {}\n".format(
                app.platform, actions.app.bundle()
            )
        elif app.platform == "windows":
            result = (
                "os: windows\nand app.name: {}\nos: windows\nand app.exe: {}\n".format(
                    friendly_name, executable
                )
            )
        else:
            result = "os: {}\nand app.name: {}\n".format(app.platform, friendly_name)

        actions.clip.set_text(result)

    def talon_get_tags() -> str:
        """Get tags as text"""
        return format("tags", registry.tags)

    def talon_get_actions() -> str:
        """Get actions list as text"""
        return format("actions", registry.actions)

    def talon_get_actions_long() -> str:
        """Get long actions list as text"""
        return format("actions", registry.decls.actions, add_desc=True)

    def talon_get_actions_search(text: str) -> str:
        """Get list of actions from search parameter"""
        actions = filter_search(registry.decls.actions, text)
        return format("actions", actions, add_desc=True)

    def talon_get_modes() -> str:
        """Get modes as text"""
        return format("modes", scope.get("mode"))

    def talon_get_captures() -> str:
        """Get captures as text"""
        return format("captures", registry.captures)

    def talon_print_list_problems():
        """Search for non alpha keys in meta lists"""
        for n, l in registry.lists.items():
            for ml in l:
                for v in ml:
                    if re.search(r"[^a-zA-Z' ]", v):
                        print(f"{n}: {v}")

    def talon_get_lists() -> str:
        """Get lists as text"""
        return format("lists", registry.lists)

    def talon_get_core() -> str:
        """Get core lists and captures as text"""
        captures = filter_core(registry.decls.captures)
        actions = filter_core(registry.decls.actions)
        captures_string = format("captures", captures, add_desc=True)
        actions_string = format("actions", actions, add_desc=True)
        return f"{captures_string}\n\n{actions_string}"

    def talon_sim_phrase(phrase: Union[str, Phrase]):
        """Sims the phrase in the active app and dumps to the log"""
        print("**** Simulated phrase **** ")
        sim = speech_system._sim(str(phrase))
        print(f" \n{sim}")
        print("*************************")

    def talon_restart():
        """Quit and relaunch the Talon app"""

    def talon_was_restarted() -> bool:
        """Returns true if Talon was just restarted"""
        restart_event = storage.get("talon_restart_event", 0)
        return time.time() - restart_event < 25

    def as_dict(
        arg1: Any = None, arg2: Any = None, arg3: Any = None, arg4: Any = None
    ) -> dict:
        """Create dict"""
        args = actions.user.as_list(arg1, arg2, arg3, arg4)
        if len(args) % 2 != 0:
            raise RuntimeError("Can't create dictionary: Uneven number of arguments")
        result = {}
        for i in range(0, len(args), 2):
            result[args[i]] = args[i + 1]
        return result

    def as_list(
        arg1: Any = None, arg2: Any = None, arg3: Any = None, arg4: Any = None
    ) -> list:
        """Create list"""
        return [x for x in [arg1, arg2, arg3, arg4] if x]


@ctx_win.action_class("user")
class WinUserActions:
    def talon_restart():
        storage.set("talon_restart_event", time.time())
        talon_app = ui.apps(pid=os.getpid())[0]
        os.startfile(talon_app.exe)
        talon_app.quit()


def format(title, values, add_desc=False) -> str:
    text = f"-------- {title.upper()} ({len(values)}) ------------\n"
    for name in sorted(values):
        text += f"{name}"
        if add_desc:
            text += "()"
        text += "\n"
        if add_desc:
            desc = values[name].desc.replace("\n", " ")
            desc = re.sub(" +", " ", desc)
            text += f"  {desc}\n"
    text += "\n----------------------------------"
    return text


def filter_core(values: dict) -> dict:
    result = {}
    for k in values:
        if not k.startswith("user."):
            result[k] = values[k]
    return result


def filter_search(values: dict, text: str) -> dict:
    result = {}
    for k in values:
        if text in k:
            result[k] = values[k]
    return result


def create_name(text, max_len=20):
    pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")
    return "_".join(
        list(islice(pattern.findall(text.replace(".exe", "")), max_len))
    ).lower()
