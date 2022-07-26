from talon import Context, Module, app, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
language: en_US
"""

mod.list("vocabulary", desc="additional vocabulary words")


# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
def additional_words_update(csv_dict: dict):
    ctx.lists["user.vocabulary"] = csv_dict


# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.
def words_to_replace_update(csv_dict: dict):
    ctx.settings["dictate.word_map"] = csv_dict


def on_ready():
    actions.user.watch_csv_as_dict("additional_words", additional_words_update)
    actions.user.watch_csv_as_dict("words_to_replace", words_to_replace_update)


app.register("ready", on_ready)
