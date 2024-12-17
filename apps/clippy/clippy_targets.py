from contextlib import suppress
from typing import Optional, Union
from talon import Module
from dataclasses import dataclass


@dataclass
class ClippyPrimitiveTarget:
    type = "primitive"
    hint: str
    count: Optional[int] = None

    def to_dict(self):
        return {"type": self.type, **self.__dict__}


@dataclass
class ClippyRangeTarget:
    type = "range"
    start: str
    end: str

    def to_dict(self):
        return {"type": self.type, **self.__dict__}


@dataclass
class ClippySearchTarget:
    type = "search"
    offset: int
    itemType: Optional[str] = None
    itemText: Optional[str] = None

    def to_dict(self):
        return {"type": self.type, **self.__dict__}


ClippyTarget = Union[ClippyPrimitiveTarget, ClippyRangeTarget, ClippySearchTarget]

mod = Module()
mod.list("clippy_search_type", desc="Clippy search types")


@mod.capture(rule="<user.number_key> | {user.letter} [{user.letter}]")
def clippy_hint(m) -> str:
    with suppress(AttributeError):
        return str(m.number_key)
    return "".join(m.letter_list)


@mod.capture(rule="[<number_small> items] <user.clippy_hint>")
def clippy_primitive_target(m) -> ClippyPrimitiveTarget:
    target = ClippyPrimitiveTarget(m.clippy_hint)
    with suppress(AttributeError):
        target.count = m.number_small
    return target


@mod.capture(rule="<user.clippy_hint> past <user.clippy_hint>")
def clippy_range_target(m) -> ClippyRangeTarget:
    return ClippyRangeTarget(m.clippy_hint_list[0], m.clippy_hint_list[1])


@mod.capture(
    rule="[<user.ordinals_small>] ({user.clippy_search_type} | with <user.prose>)"
)
def clippy_search_target(m) -> ClippySearchTarget:
    try:
        offset = m.ordinals_small - 1
    except AttributeError:
        offset = 0
    target = ClippySearchTarget(offset)
    with suppress(AttributeError):
        target.itemType = m.clippy_search_type
    with suppress(AttributeError):
        target.itemText = m.prose
    return target


@mod.capture(
    rule="<user.clippy_primitive_target> | <user.clippy_range_target> | <user.clippy_search_target>"
)
def clippy_target(m) -> ClippyTarget:
    with suppress(AttributeError):
        return m.clippy_primitive_target
    with suppress(AttributeError):
        return m.clippy_range_target
    return m.clippy_search_target


@mod.capture(rule="<user.clippy_target> [and <user.clippy_target>]*")
def clippy_targets(m) -> list[ClippyTarget]:
    return m.clippy_target_list
