from talon import Context, Module, app, actions

mod = Module()

ctx_en = Context()

ctx_sv = Context()
ctx_sv.matches = r"""
language: sv
"""

mod.list("vocabulary", desc="additional vocabulary words")


# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
def additional_words_update(csv_dict: dict):
    ctx_en.lists["user.vocabulary"] = csv_dict


# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.


def words_to_replace_en_update(csv_dict: dict):
    ctx_en.settings["dictate.word_map"] = csv_dict


def words_to_replace_sv_update(csv_dict: dict):
    ctx_sv.settings["dictate.word_map"] = csv_dict


def on_ready():
    actions.user.watch_csv_as_dict("additional_words_en", additional_words_update)
    actions.user.watch_csv_as_dict("words_to_replace_en", words_to_replace_en_update)
    actions.user.watch_csv_as_dict("words_to_replace_sv", words_to_replace_sv_update)


app.register("ready", on_ready)
