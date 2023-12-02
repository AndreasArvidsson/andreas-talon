from talon import Module, Context, resource, app, actions
from dataclasses import dataclass
from pathlib import Path
import tempfile
import json
import glob
import re
import time


@dataclass
class State:
    workspaceFolders: list[str]


TYPE_PATTERN = r"[a-zA-Z_]{3,}"

mod = Module()
ctx = Context()

mod.list("vscode_identifier", "Known identifiers and types in the vscode workspace")

json_file = Path(tempfile.gettempdir()) / "vscodeState.json"

workspaceFolders: list[Path] = []
spoken_map: dict[str, str] = {}


def on_ready():
    @resource.watch(str(json_file))
    def on_watch(f):
        global workspaceFolders
        state_json: dict = json.loads(f.read())
        state = State(**state_json)
        workspaceFolders = [Path(p) for p in state.workspaceFolders]


@ctx.dynamic_list("user.vscode_identifier")
def vscode_identifier_list() -> dict[str, str]:
    global spoken_map
    t = time.perf_counter()
    types = get_types_from_workspaces()
    spoken_map = generate_spoken_forms(types)
    print("Generating vscode_identifier_list", len(spoken_map))
    print(f"{int((time.perf_counter()-t)*1000)}ms")
    return spoken_map


@mod.capture(rule="{user.vscode_identifier}")
def vscode_identifier(m) -> str:
    return spoken_map[m.vscode_identifier]


def get_types_from_workspaces() -> set[str]:
    file_extension = actions.win.file_ext()
    result: set[str] = set()

    if not file_extension:
        return result

    pattern = f"**/*{file_extension}"

    for folder in workspaceFolders:
        files = glob.glob(pattern, root_dir=folder, recursive=True)

        for file in files:
            file_path = folder / file
            result.update(get_types_from_file(file_path))

    return result


def get_types_from_file(file_path: Path) -> list[str]:
    try:
        with open(file_path, "r") as file:
            return re.findall(TYPE_PATTERN, file.read())
    except Exception as ex:
        return []


def generate_spoken_forms(types: set[str]) -> dict[str, str]:
    return {generate_spoken_form(t): t for t in types}


def generate_spoken_form(type: str) -> str:
    # Replace things that are not letters with spaces
    type = re.sub(r"[^a-zA-Z]", " ", type)
    # Split on camel case
    type = actions.user.de_camel(type)
    # Finally lower case
    return type.lower()


# app.register("ready", on_ready)
