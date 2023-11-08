from talon import Context, Module, app, actions
from typing import Sequence
from pathlib import Path
from .phrase_replacer import PhraseReplacer

mod = Module()

mod.list("vocabulary", "Additional vocabulary words")

ctx_en = Context()

ctx_sv = Context()
ctx_sv.matches = r"""
language: sv
"""


phrase_replacer_en = None
phrase_replacer_sv = None


@ctx_en.action_class("dictate")
class DictateActionsEn:
    def replace_words(words: Sequence[str]) -> Sequence[str]:
        return phrase_replacer_en.replace(words)


@ctx_sv.action_class("dictate")
class DictateActionsSv:
    def replace_words(words: Sequence[str]) -> Sequence[str]:
        return phrase_replacer_sv.replace(words)


@mod.action_class
class Actions:
    def edit_words_to_replace():
        """Edit words to replace csv"""
        file = Path(__file__).parent / "words_to_replace_en.csv"
        actions.user.edit_text_file(file.absolute())

    def edit_vocabulary():
        """Edit vocabulary Talon list"""
        file = Path(__file__).parent / "vocabulary_en.talon-list"
        actions.user.edit_text_file(file.absolute())


# Words to replace is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries don't change the priority with which Talon
# recognizes some words over others.
def words_to_replace_en_update(csv_dict: dict):
    global phrase_replacer_en
    phrase_replacer_en = PhraseReplacer(csv_dict)


def words_to_replace_sv_update(csv_dict: dict):
    global phrase_replacer_sv
    phrase_replacer_sv = PhraseReplacer(csv_dict)


def on_ready():
    dir = Path(__file__).parent
    actions.user.watch_csv_as_dict(
        dir / "words_to_replace_en.csv",
        words_to_replace_en_update,
    )
    actions.user.watch_csv_as_dict(
        dir / "words_to_replace_sv.csv",
        words_to_replace_sv_update,
    )


app.register("ready", on_ready)
