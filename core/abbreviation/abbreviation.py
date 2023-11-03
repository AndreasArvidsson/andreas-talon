from talon import Context, Module, app, actions
from pathlib import Path

mod = Module()
ctx = Context()
mod.list("abbreviation", "Common abbreviation")


@mod.capture(rule="brief {user.abbreviation}")
def abbreviation(m) -> str:
    """Abbreviated words"""
    return m.abbreviation


def abbreviations_update(csv_dict: dict):
    ctx.lists["user.abbreviation"] = {
        **{v: v for v in csv_dict.values()},
        **csv_dict,
    }


def on_ready():
    actions.user.watch_csv_as_dict(
        Path(__file__).parent / "abbreviation_en.csv",
        abbreviations_update,
    )


app.register("ready", on_ready)
