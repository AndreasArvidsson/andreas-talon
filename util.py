from collections.abc import Iterable
import re

def merge(*args):
    result = {}
    for arg in args:
        if isinstance(arg, dict):
            for k, v in arg.items():
                if v == None:
                    del result[k]
                else:
                    result[k] = v
        elif isinstance(arg, Iterable):
            for v in arg:
                result[v] = v
        else:
            raise Exception("Unknown type " + str(type(arg)))
    return result


def cycle(value, min, max):
    if value < min:
        return max
    if value > max:
        return min
    return value

def cramp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value

def split_camel(text: str):
    """Split camel case. Including numbers"""
    return re.split(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[a-zA-Z])(?=[0-9])|(?<=[0-9])(?=[a-zA-Z])", text)

def de_camel(text: str) -> str:
    """Replacing camelCase boundaries with blank space"""
    return re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[a-zA-Z])(?=[0-9])|(?<=[0-9])(?=[a-zA-Z])", " ", text)
