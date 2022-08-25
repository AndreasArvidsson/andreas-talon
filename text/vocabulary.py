from talon import Context, Module, app, actions
from typing import Sequence
from .phrase_replacer import PhraseReplacer

mod = Module()

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


mod.list("vocabulary", desc="additional vocabulary words")


# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
def additional_words_en_update(csv_dict: dict):
    ctx_en.lists["user.vocabulary"] = csv_dict


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
    actions.user.watch_csv_as_dict("additional_words_en", additional_words_en_update)
    actions.user.watch_csv_as_dict("words_to_replace_en", words_to_replace_en_update)
    actions.user.watch_csv_as_dict("words_to_replace_sv", words_to_replace_sv_update)


app.register("ready", on_ready)
