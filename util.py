from collections.abc import Iterable

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