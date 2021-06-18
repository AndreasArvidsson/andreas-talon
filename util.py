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
