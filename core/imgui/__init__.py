from typing import Callable

from talon.screen import Screen

from .gui import GUI


def open(
    *,
    screen: Screen | None = None,
    x: float | None = None,
    y: float | None = None,
    width: float | None = None,
    height: float | None = None,
):
    def open_inner(draw: Callable[[GUI], None]):
        return GUI(
            draw,
            screen=screen,
            x=x,
            y=y,
            width=width,
            height=height,
        )

    return open_inner
