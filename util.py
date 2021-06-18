from collections.abc import Iterable
import re

def merge(*args):
    result = {}
    for arg in args:
        if isinstance(arg, dict):
            result.update(arg)
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
    return re.split("(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[a-zA-Z])(?=[0-9])|(?<=[0-9])(?=[a-zA-Z])", text)