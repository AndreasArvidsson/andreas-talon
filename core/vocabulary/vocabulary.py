from talon import Context, Module, actions, resource
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


phrase_replacer_en = PhraseReplacer({})
phrase_replacer_sv = PhraseReplacer({})


@ctx_en.action_class("dictate")
class DictateActionsEn:
    @staticmethod
    def replace_words(words: Sequence[str]) -> Sequence[str]:
        return phrase_replacer_en.replace(words)


@ctx_sv.action_class("dictate")
class DictateActionsSv:
    @staticmethod
    def replace_words(words: Sequence[str]) -> Sequence[str]:
        return phrase_replacer_sv.replace(words)


# Words to replace is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries don't change the priority with which Talon
# recognizes some words over others.
@resource.watch(Path(__file__).parent / "words_to_replace_en.csv")
def words_to_replace_en_update(f):
    global phrase_replacer_en
    csv_dict = actions.user.read_csv_as_dict(f)
    phrase_replacer_en = PhraseReplacer(csv_dict)


@resource.watch(Path(__file__).parent / "words_to_replace_sv.csv")
def words_to_replace_sv_update(f):
    global phrase_replacer_sv
    csv_dict = actions.user.read_csv_as_dict(f)
    phrase_replacer_sv = PhraseReplacer(csv_dict)
