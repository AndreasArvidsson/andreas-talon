from talon import Module, Context, ctrl
from typing import Optional


def mouse_move(x: float, y: float, dx: Optional[float] = 0, dy: Optional[float] = 0):
    global _x, _y, _dx, _dy
    _x, _y, _dx, _dy = x, y, dx, dy

    if not frozen:
        callback(x, y, dx=dx, dy=dy)


_x = _y = _dx = _dy = 0
callback = ctrl.mouse_move
ctrl.mouse_move = mouse_move
frozen = False
mod = Module()
ctx = Context()

mod.tag(
    "mouse_frozen",
    "Indicates that the mouse cursor is frozen and will not update position",
)


@mod.action_class
class Actions:
    def mouse_freeze_toggle(
        freeze: Optional[bool] = None, tag: Optional[str] = "user.mouse_frozen"
    ):
        """Toggle to freeze position updates of the mouse cursor"""
        global frozen

        if freeze == None:
            freeze = not frozen

        # Went from frozen to unfrozen. Set latest position.
        if frozen and not freeze:
            callback(_x, _y, dx=_dx, dy=_dy)

        frozen = freeze

        if freeze and tag:
            ctx.tags = [tag]
        else:
            ctx.tags = []
