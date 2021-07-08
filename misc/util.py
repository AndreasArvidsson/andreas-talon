from talon import Module
import re

mod = Module()
camel_regex = r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[a-zA-Z])(?=[0-9])|(?<=[0-9])(?=[a-zA-Z])"


@mod.action_class
class Actions:
    def cycle(value: int, min: int, max: int) -> int:
        """Cycle value between minimum and maximum"""
        if value < min:
            return max
        if value > max:
            return min
        return value

    def cramp(value: int, min: int, max: int) -> int:
        """Cramp value between minimum and maximum"""
        if value < min:
            return min
        if value > max:
            return max
        return value

    def split_camel(text: str) -> [str]:
        """Split camel case. Including numbers"""
        return re.split(camel_regex, text)

    def de_camel(text: str) -> str:
        """Replacing camelCase boundaries with blank space"""
        return re.sub(camel_regex, " ", text)
