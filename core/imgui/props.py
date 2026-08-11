from collections.abc import Callable
from dataclasses import dataclass

from talon.screen import Screen


@dataclass
class Props:
    callback: Callable
    screen: Screen | None
    x: float | None
    y: float | None
    width: float | None
    height: float | None
