from abc import ABC, abstractmethod

from talon.types import Rect

from .state import State


class Widget(ABC):
    rect: Rect | None

    @abstractmethod
    def draw(self, state: State) -> None: ...
