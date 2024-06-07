from talon import Context, resource, actions
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


JSON_FILE = Path(tempfile.gettempdir()) / "vscodeState.json"
SYMBOL_PATTERN = r"[a-zA-Z_]{3,}"

workspaceFolders: list[Path] = []
spoken_map: dict[str, str] = {}

ctx = Context()
ctx.matches = r"""
app: vscode
"""


@resource.watch(str(JSON_FILE))
def on_watch(f):
    global workspaceFolders
    state_json: dict = json.loads(f.read())
    state = State(**state_json)
    workspaceFolders = [Path(p) for p in state.workspaceFolders]


@ctx.dynamic_list("user.code_symbol")
def code_symbol(_) -> dict[str, str]:
    global spoken_map
    t = time.perf_counter()
    symbols = get_symbols_from_workspaces()
    spoken_map = generate_spoken_forms(symbols)
    print("Generating code_symbol list: ", len(spoken_map))
    print(f"{int((time.perf_counter()-t)*1000)}ms")
    return spoken_map


def get_symbols_from_workspaces() -> set[str]:
    file_extension = actions.win.file_ext()
    result: set[str] = set()

    if not file_extension:
        return result

    pattern = f"**/*{file_extension}"

    for folder in workspaceFolders:
        files = glob.glob(pattern, root_dir=folder, recursive=True)

        for file in files:
            file_path = folder / file
            result.update(get_symbols_from_file(file_path))

    return result


def get_symbols_from_file(file_path: Path) -> list[str]:
    try:
        with open(file_path, "r") as file:
            return re.findall(SYMBOL_PATTERN, file.read())
    except Exception as ex:
        return []


def generate_spoken_forms(symbols: set[str]) -> dict[str, str]:
    return {generate_spoken_form(t): t for t in symbols}


def generate_spoken_form(symbol: str) -> str:
    # Replace things that are not letters with spaces
    symbol = re.sub(r"[^a-zA-Z]", " ", symbol)
    # Split on camel case
    symbol = actions.user.de_camel(symbol)
    # Finally lower case
    return symbol.lower()
