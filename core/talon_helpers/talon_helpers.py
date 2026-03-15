import inspect
import json
import os
import re
import time
from itertools import islice
from typing import Any, Callable, Union

from talon import (
    Context,
    Module,
    actions,
    app,
    registry,
    scope,
    speech_system,
    storage,
    ui,
)
from talon.grammar import Phrase  # pyright: ignore[reportAttributeAccessIssue]

mod = Module()

ctx_win = Context()
ctx_win.matches = r"""
os: windows
"""


@mod.action_class
class Actions:
    def talon_add_context_clipboard_python():
        """Adds os-specific context info to the clipboard for the focused app for .py files. Assumes you've a Module named mod declared."""
        name = get_normalized_app_name()
        context_matchers = get_contetxt_matchers()
        result = f'mod.apps.{name} = r"""\n{context_matchers}\n"""'
        actions.clip.set_text(result)

    def talon_add_context_clipboard():
        """Adds os-specific context info to the clipboard for the focused app for .talon files"""
        context_matchers = get_contetxt_matchers()
        actions.clip.set_text(context_matchers)

    def talon_get_tags() -> str:
        """Get tags as text"""
        return format("tags", registry.tags)

    def talon_get_actions() -> str:
        """Get actions list as text"""
        return format("actions", registry.actions)

    def talon_get_actions_long() -> str:
        """Get long actions list as text"""
        return format("actions", registry.decls.actions, add_desc=True)

    @staticmethod
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
        """Search for non alpha keys in talon lists"""
        for n, lst in registry.lists.items():
            for ml in lst:
                if isinstance(ml, str):
                    continue
                if isinstance(ml, Callable):
                    continue
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def as_list(
        arg1: Any = None, arg2: Any = None, arg3: Any = None, arg4: Any = None
    ) -> list:
        """Create list"""
        return [x for x in [arg1, arg2, arg3, arg4] if x]

    def copy_default_talon_actions():
        """Copies the default talon actions to the clipboard"""
        result = []

        for name, action_impls in sorted(registry.actions.items()):
            if name.startswith("user."):
                continue

            action = action_impls[0]

            if not action.type_decl:
                raise ValueError(f"Action {name} has no type_decl")

            result.append(
                {
                    "name": name,
                    "signature": str(inspect.signature(action.func)),
                    "docstr": action.type_decl.desc,
                }
            )

        json_str = json.dumps(result, indent=4)
        actions.clip.set_text(json_str)


@ctx_win.action_class("user")
class WinUserActions:
    def talon_restart():
        storage.set("talon_restart_event", time.time())
        talon_app = ui.apps(pid=os.getpid())[0]
        os.startfile(talon_app.exe)
        actions.sleep("100ms")
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


def get_contetxt_matchers() -> str:
    if app.platform == "mac":
        matcher = f"app.bundle: {actions.app.bundle()}"
    elif app.platform == "windows":
        executable = actions.app.executable().split(os.path.sep)[-1]
        matcher = f"app.exe: {executable}"
    else:
        matcher = f"app.name: {actions.app.name()}"
    return f"os: {app.platform}\nand {matcher}"


def get_normalized_app_name() -> str:
    pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")
    app_name = actions.app.name()
    return "_".join(
        list(islice(pattern.findall(app_name.replace(".exe", "")), 20))
    ).lower()
