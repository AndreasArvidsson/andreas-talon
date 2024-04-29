from typing import Optional, Union
from talon import Module
from dataclasses import dataclass


@dataclass
class ClippyPrimitiveTarget:
    type = "primitive"
    hint: str
    count: Optional[int] = None


@dataclass
class ClippyRangeTarget:
    type = "range"
    start: str
    end: str


ClippyTarget = Union[ClippyPrimitiveTarget, ClippyRangeTarget]

mod = Module()


@mod.capture(rule="{user.digit} | {user.letter} [{user.letter}]")
def clippy_hint(m) -> str:
    try:
        return str(m.digit)
    except AttributeError:
        return "".join(m.letter_list)


@mod.capture(rule="[<number_small> items] <user.clippy_hint>")
def clippy_primitive_target(m) -> ClippyPrimitiveTarget:
    target = ClippyPrimitiveTarget(m.clippy_hint)
    try:
        target.count = m.number_small
    except AttributeError:
        pass
    return target


@mod.capture(rule="<user.clippy_hint> past <user.clippy_hint>")
def clippy_range_target(m) -> ClippyRangeTarget:
    return ClippyRangeTarget(m.clippy_hint_list[0], m.clippy_hint_list[1])


@mod.capture(rule="<user.clippy_primitive_target> | <user.clippy_range_target>")
def clippy_target(m) -> ClippyTarget:
    try:
        return m.clippy_primitive_target
    except AttributeError:
        return m.clippy_range_target


@mod.capture(rule="<user.clippy_target> [and <user.clippy_target>]*")
def clippy_targets(m) -> list[ClippyTarget]:
    return m.clippy_target_list
