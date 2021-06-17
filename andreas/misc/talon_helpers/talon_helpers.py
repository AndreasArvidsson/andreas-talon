from talon import Context, actions, ui, Module, app, clip, registry, scope
from talon_init import VENV_BIN
import os
import re
from itertools import islice

mod = Module()
pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")

# todo: should this be an action that lives elsewhere??


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
        callback = lambda k: f"{k.ljust(40)} {registry.decls.actions[k].desc}"
        return format("actions", registry.decls.actions, callback)

    def talon_get_modes() -> str:
        """Get modes as text"""
        return format("modes", scope.get("mode"))

    def talon_get_captures() -> str:
        """Get captures as text"""
        return format("captures", registry.captures)

    def talon_get_lists() -> str:
        """Get lists as text"""
        return format("lists", registry.lists)

    def talon_run(path: str):
        """Run talon binary"""
        EXT = ".bat" if app.platform == "windows" else ""
        path = str(os.path.join(VENV_BIN, f"{path}{EXT}"))
        ui.launch(path="cmd", args=["/c", path])


def format(title, values, get_line = None) -> str:
    text = f"-------- {title.upper()} ({len(values)}) ------------\n"
    if get_line:
        text += "\n".join(map(get_line, sorted(values)))
    else:
        text += "\n".join(sorted(values))
    text += "\n----------------------------------"
    return text

