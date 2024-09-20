from talon import Context, Module, actions, resource
from pathlib import Path

mod = Module()
ctx = Context()
mod.list("abbreviation", "Common abbreviation")


@mod.capture(rule="brief {user.abbreviation}")
def abbreviation(m) -> str:
    """Abbreviated words"""
    return m.abbreviation


@resource.watch(Path(__file__).parent / "abbreviation_en.csv")
def abbreviations_update(f):
    csv_dict = actions.user.read_csv_as_dict(f)
    ctx.lists["user.abbreviation"] = {
        **{v: v for v in csv_dict.values()},
        **csv_dict,
    }
