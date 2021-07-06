from collections.abc import Iterable


def merge(*args) -> dict:
    """Merge dictionaries and lists"""
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
