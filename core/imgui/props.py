from dataclasses import dataclass
from typing import Callable

from talon.screen import Screen


@dataclass
class Props:
    callback: Callable
    screen: Screen | None
    x: float | None
    y: float | None
    width: float | None
    height: float | None
