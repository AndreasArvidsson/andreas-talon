from dataclasses import dataclass
from typing import Callable, Literal, Union
from talon import Module, actions

EditSimpleModifierType = Literal["containingTokenIfEmpty",]


@dataclass
class EditSimpleModifier:
    type: EditSimpleModifierType

    def __str__(self):
        return self.type


@dataclass
class EditContainingScopeModifier:
    type = "containingScope"
    scope_type: str

    def __str__(self):
        return f"{self.type}({self.scope_type})"


@dataclass
class EditExtendThroughModifier:
    type: Literal["extendThroughStartOf", "extendThroughEndOf"]
    scope_type: str

    def __str__(self):
        return f"{self.type}({self.scope_type})"


EditModifier = Union[
    EditSimpleModifier,
    EditContainingScopeModifier,
    EditExtendThroughModifier,
]


mod = Module()
mod.list("edit_scope_type", desc="Scope types for the edit command")


@mod.capture(rule="this | dis")
def edit_modifier_this(m) -> EditSimpleModifier:
    return EditSimpleModifier("containingTokenIfEmpty")


@mod.capture(rule="head | tail")
def edit_modifier_head_tail(m) -> EditExtendThroughModifier:
    if m[0] == "head":
        return EditExtendThroughModifier("extendThroughStartOf", "line")
    return EditExtendThroughModifier("extendThroughEndOf", "line")


@mod.capture(rule="{user.edit_scope_type}")
def edit_modifier_containing_scope(m) -> EditContainingScopeModifier:
    return EditContainingScopeModifier(m.edit_scope_type)


@mod.capture(
    rule="<user.edit_modifier_this> | "
    "<user.edit_modifier_containing_scope> | "
    "<user.edit_modifier_head_tail>"
)
def edit_modifier(m) -> EditModifier:
    return m[0]


modifier_callbacks = {
    "containingTokenIfEmpty": actions.user.select_containing_word_if_empty,
    "extendThroughStartOf(line)": actions.user.select_line_start,
    "extendThroughEndOf(line)": actions.user.select_line_end,
    "containingScope(token)": actions.edit.select_word,
    "containingScope(line)": actions.edit.select_line,
    "containingScope(sentence)": actions.edit.select_sentence,
    "containingScope(paragraph)": actions.edit.select_paragraph,
    "containingScope(document)": actions.edit.select_all,
    "containingScope(surroundingPair)": actions.user.select_surrounding_pair,
    "containingScope(surroundingPairInterior)": actions.user.select_surrounding_pair_interior,
}


def get_modifier_callbacks(modifiers: list[EditModifier]) -> list[Callable]:
    return [get_modifier_callback(modifier) for modifier in modifiers]


def get_modifier_callback(modifier: EditModifier) -> Callable:
    key = str(modifier)

    if key in modifier_callbacks:
        return modifier_callbacks[key]

    raise ValueError(f"Unknown edit modifier: {modifier}")
