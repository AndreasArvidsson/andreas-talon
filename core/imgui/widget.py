from abc import ABC, abstractmethod

from talon.types import Rect

from .state import State


class Widget(ABC):
    clickable: bool = False
    numbered: bool = False
    rect: Rect | None

    @abstractmethod
    def draw(self, state: State) -> None: ...

    def clicked(self) -> bool:
        return False

    def click(self) -> None:
        pass
