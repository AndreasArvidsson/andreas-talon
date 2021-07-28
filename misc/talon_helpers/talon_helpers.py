from talon import Context, actions, ui, Module, app, clip, registry, scope
from talon_init import VENV_BIN
import os
import re
from itertools import islice
from pathlib import Path

mod = Module()
pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")

def create_name(text, max_len=20):
    return "_".join(list(islice(pattern.findall(text), max_len))).lower()


@mod.action_class
class Actions:
    def talon_add_context_clipboard_python():
        """Adds os-specific context info to the clipboard for the focused app for .py files. Assumes you've a Module named mod declared."""
        friendly_name = actions.app.name()
        executable = actions.app.executable().split(os.path.sep)[-1]
        app_name = create_name(friendly_name.replace(".exe", ""))
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

        clip.set_text(result)

    def talon_add_context_clipboard():
        """Adds os-specific context info to the clipboard for the focused app for .talon files"""
        friendly_name = actions.app.name()
        executable = actions.app.executable().split(os.path.sep)[-1]
        if app.platform == "mac":
            result = "os: {}\nand app.bundle: {}\n".format(
                app.platform, actions.app.bundle()
            )
        elif app.platform == "windows":
            result = "os: windows\nand app.name: {}\nos: windows\nand app.exe: {}\n".format(
                friendly_name, executable
            )
        else:
            result = "os: {}\nand app.name: {}\n".format(
                app.platform, friendly_name)

        clip.set_text(result)

    def talon_get_tags() -> str:
        """Get tags as text"""
        return format("tags", registry.tags)

    def talon_get_actions() -> str:
        """Get actions list as text"""
        return format("actions", registry.actions)

    def talon_get_actions_long() -> str:
        """Get long actions list as text"""
        return format("actions", registry.decls.actions, add_desc = True)

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
                    if re.search(r"[^a-zA-Z ]", v):
                        print(f"{n}: {v}")

    def talon_get_lists() -> str:
        """Get lists as text"""
        return format("lists", registry.lists)

    def talon_get_core() -> str:
        """Get core lists and captures as text"""
        captures = filter_core(registry.decls.captures)
        actions = filter_core(registry.decls.actions)
        captures_string = format("captures", captures, add_desc = True)
        actions_string = format("actions", actions, add_desc = True)
        return f"{captures_string}\n\n{actions_string}"


def format(title, values, add_desc = False) -> str:
    text = f"-------- {title.upper()} ({len(values)}) ------------\n"
    for name in sorted(values):
        text += f"{name}\n"
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