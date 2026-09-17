from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from talon.screen import Screen

if TYPE_CHECKING:
    from .gui import GUI


@dataclass
class Props:
    callback: Callable[[GUI], None]
    screen: Screen | None
    x: float | None
    y: float | None
    width: float | None
    height: float | None
