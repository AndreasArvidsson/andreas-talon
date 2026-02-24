from abc import ABC, abstractmethod


from .state import State


class Widget(ABC):
    @abstractmethod
    def draw(self, state: State) -> None: ...
