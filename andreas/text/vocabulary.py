from talon import Context, Module

mod = Module()
ctx = Context()
mod.list("vocabulary", desc="additional vocabulary words")


# Default words that will need to be capitalized (particularly under w2l).
# NB. These defaults and those later in this file are ONLY used when
# auto-creating the corresponding settings/*.csv files. Those csv files
# determine the contents of user.vocabulary and dictate.word_map. Once they
# exist, the contents of the lists/dictionaries below are irrelevant.
capitalize_defaults = [
    "I",
    "I'm",
    "I've",
    "I'll",
    "I'd",
    "Monday",
    "Mondays",
    "Tuesday",
    "Tuesdays",
    "Wednesday",
    "Wednesdays",
    "Thursday",
    "Thursdays",
    "Friday",
    "Fridays",
    "Saturday",
    "Saturdays",
    "Sunday",
    "Sundays",
    "January",
    "February",
    # March omitted because it's a regular word too
    "April",
    # May omitted because it's a regular word too
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Default words that need to be remapped.
word_map_defaults = {
    # "some": "sum"
}
word_map_defaults.update({word.lower(): word for word in capitalize_defaults})

# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.
ctx.settings["dictate.word_map"] = word_map_defaults

# Default words that should be added to Talon's vocabulary.
simple_default_vocabulary = [
    "admin", "vpn", "dns", "exe", "linux",
    "array", "html", "url", "vscode", "json", "api", "http", "css"
]
# Defaults for different pronounciations of words that need to be added to Talon's vocabulary.
default_vocabulary = {
    # "N map": "nmap"
}
default_vocabulary.update({word.lower(): word for word in simple_default_vocabulary})

# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
ctx.lists["user.vocabulary"] = default_vocabulary
