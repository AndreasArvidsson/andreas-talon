from dataclasses import dataclass
from datetime import datetime
from io import TextIOWrapper
from types import NoneType, UnionType
from typing import (
    Any,
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
from talon import registry, Module, app
from talon.screen import Screen
from talon.types import Rect
from talon.ui import Window, App
from talon.grammar import Phrase, Capture
from pathlib import Path
from talon.skia.image import Image
import inspect
import os

mod = Module()


@dataclass
class Action:
    name: str
    desc: str
    parameters: list[str]
    return_type: str


@mod.action_class
class Actions:
    def read_registry(name: str, value: int) -> str:
        """some description"""
        for name, actions in registry.actions.items():
            print(name)
            action = actions[0]
            print(action)
            print(type(action))
            print(dir(action))
            break
        return ""


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

    if type is Sequence[str]:
        return "str[]"
    if type == list[dict]:
        return "Record<str, any>[]"
    if type == dict:
        return "Record<str, any>"
    if type == list:
        return "any[]"
    if type == tuple:
        return "any[]"
    if type == set:
        return "Set<any>"
    if type == Optional[dict]:
        return "Record<str, any> | null"
    if type == datetime:
        return "Date"
    if type == bytes:
        return "Uint8Array"

    if type == Path:
        return "any"
    if type == Screen:
        return "any"
    if type == Rect:
        return "any"
    if type == Window:
        return "any"
    if type == App:
        return "any"
    if type == Image:
        return "any"
    if type == Capture:
        return "any"
    if type == Phrase:
        return "any"
    if type == Union[Phrase, str]:
        return "any"

    # Check for generic types
    origin = get_origin(py_type)
    args = get_args(py_type)

    if origin is list or origin is List:
        return f"{get_typescript_type(args[0])}[]" if args else "any[]"

    if origin is dict or origin is Dict:
        return (
            f"{{ [key: {get_typescript_type(args[0])}]: {get_typescript_type(args[1])} }}"
            if args
            else "{ [key: string]: any }"
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
        return " | ".join([f'"{get_typescript_type(type)}"' for type in args])

    return "any"  # Default case if type is not recognized


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
    with open(file_path, "w") as f:
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
    namespaces.append("user")

    with open(file_path, "w") as f:
        f.write("export interface Actions {\n")
        main_actions = actions_map["main"]
        write_actions(f, main_actions, "    ")
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
