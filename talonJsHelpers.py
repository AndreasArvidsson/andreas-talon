from collections.abc import Sequence as AbcSequence, Callable as AbcCallable
from dataclasses import dataclass
from datetime import datetime
from io import TextIOWrapper
from types import NoneType, UnionType
from typing import (
    Any,
    Callable,
    List,
    Dict,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
    Tuple,
    Union,
    Optional,
    get_origin,
    get_args,
)
from talon import registry, app
from talon.screen import Screen
from talon.types import Rect
from talon.scripting.types import CommandImpl, ScriptImpl
from talon.scripting.rctx import ResourceContext
from talon.scripting.talon_script import TalonScript
from talon.ui import Window, App
from talon.grammar import Phrase, Capture
from pathlib import Path
from talon.skia.image import Image
import inspect
import os


@dataclass
class Action:
    name: str
    desc: str
    parameters: list[str]
    return_type: str


type_definitions = [
    App,
    Capture,
    CommandImpl,
    Image,
    Path,
    Phrase,
    Rect,
    ResourceContext,
    Screen,
    ScriptImpl,
    TalonScript,
    Window,
]


def get_typescript_type(py_type: Any) -> str:
    # Check for NoneType
    if py_type is None or py_type is NoneType:
        return "null"

    # Check for basic types
    if py_type is Any:
        return "any"
    if py_type is str:
        return "string"
    if py_type is bool:
        return "boolean"
    if py_type in (int, float):
        return "number"

    if py_type is dict:
        return "Record<string, any>"
    if py_type is list:
        return "any[]"
    if py_type is tuple:
        return "any[]"
    if py_type is set:
        return "Set<any>"
    if py_type is datetime:
        return "Date"
    if py_type is bytes:
        return "Uint8Array"
    if py_type is callable:
        return "() => void"

    if py_type in type_definitions:
        return py_type.__name__

    if py_type is type:
        return "any"

    # Check for generic types
    origin = get_origin(py_type)
    args = get_args(py_type)

    if origin is list or origin is List or origin is AbcSequence:
        return f"{get_typescript_type(args[0])}[]" if args else "any[]"

    if origin is dict or origin is Dict:
        return (
            f"Record<{get_typescript_type(args[0])}, {get_typescript_type(args[1])}>"
            if args
            else "Record<string, any>"
        )

    if origin is tuple or origin is Tuple:
        return (
            f"[{', '.join(get_typescript_type(arg) for arg in args)}]" if args else "[]"
        )

    if origin is Union or origin is UnionType:
        arg_types = [get_typescript_type(arg) for arg in args]
        unique_arg_types = list(dict.fromkeys(arg_types))
        return " | ".join(unique_arg_types)

    if origin is Optional:
        return f"{get_typescript_type(args[0])} | null" if args else "any | null"

    if origin is Literal:
        return " | ".join([f'"{py_type}"' for py_type in args])

    if origin is Callable or origin is AbcCallable:
        parameters = [
            f"arg{i}: {get_typescript_type(param)}" for i, param in enumerate(args[0])
        ]
        return_value = get_typescript_type(args[1])
        return f"({', '.join(parameters)}) => {return_value}"

    if "user." in str(py_type):
        return "any"

    print(py_type)
    print(origin)
    print()

    return "any"


def read_registry():
    results: dict[str, list[Action]] = {}

    for name, actions in registry.actions.items():
        action = actions[0]

        if "." in name:
            index = name.index(".")
            namespace = name[:index]
            func_name = name[index + 1 :]
        else:
            namespace = "main"
            func_name = name

        desc = action.type_decl.desc if action.type_decl else ""
        parameters: list[str] = []
        return_type = "void"

        spec = inspect.getfullargspec(action.func)

        for param, type in spec.annotations.items():
            ts_type = get_typescript_type(type)
            if param == "return":
                return_type = ts_type
            else:
                if param in ["default", "new"]:
                    param += "_"
                parameters.append(f"{param}: {ts_type}")

        if namespace not in results:
            results[namespace] = []

        res_action = Action(func_name, desc, parameters, return_type)
        results[namespace].append(res_action)

    return results


def write_namespace_file(dir: str, namespaces: list[str]):
    file_path = os.path.join(dir, "Namespace.d.ts")
    namespaces.sort()
    with open(file_path, "w", newline="\n") as f:
        f.write("export type Namespace =")
        for namespace in namespaces:
            f.write(f'\n    | "{namespace}"')
        f.write(";\n")


def write_actions_file(dir: str, actions_map: dict[str, list[Action]]):
    file_path = os.path.join(dir, "Actions.d.ts")
    namespaces = list(actions_map.keys())
    namespaces.remove("main")
    namespaces.remove("user")
    namespaces.sort()
    namespaces.insert(0, "main")
    namespaces.append("user")

    with open(file_path, "w", newline="\n") as f:
        for type_definition in type_definitions:
            f.write(f"type {type_definition.__name__} = any;\n")
        f.write("\nexport interface ActionNamespaces {\n")
        for namespace in namespaces:
            ns_actions = actions_map[namespace]
            f.write(f"    {namespace}: {{\n")
            write_actions(f, ns_actions, "        ")
            f.write("    };\n")
        f.write("}\n")


def write_actions(file: TextIOWrapper, actions: list[Action], indent: str):
    actions.sort(key=lambda action: action.name)
    for action in actions:
        if action.desc:
            file.write(f"{indent}/** {action.desc} */\n")
        parameters = ", ".join(action.parameters)
        file.write(f"{indent}{action.name}({parameters}): {action.return_type};\n")


def on_ready():
    actions = read_registry()
    types_dir = os.path.join(os.path.dirname(__file__), ".ts/src/types")
    write_namespace_file(types_dir, list(actions.keys()))
    write_actions_file(types_dir, actions)


# app.register("ready", on_ready)
