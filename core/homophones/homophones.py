from talon import Module, app, actions
import re
import time
from pathlib import Path

# a list of homophones where each line is a comma separated list
# e.g. where,wear,ware
# a suitable one can be found here:
# https://github.com/pimentel/homophones

mod = Module()

homophones_last_used = {}


def update_used(word: str):
    homophones = get_list(word)
    for homophone in homophones:
        homophones_last_used[homophone] = {"word": word, "time": time.monotonic()}


@mod.action_class
class Actions:
    def homophones_get(word: str) -> list[str]:
        """Get homophones for the given word. Used by the phones action in cursorless"""
        homophones = get_list(word)
        # Since this is only used by cursorless we can assume that the next word will be used
        update_used(get_next(word, homophones))
        return homophones

    def homophones_cycle_selected():
        """Cycle homophones if the selected word is a homophone"""
        word = actions.edit.selected_text()
        if not word:
            return

        homophones = get_list(word)
        homophone = get_next(word, homophones)
        update_used(homophone)
        new_word = format_homophone(word, homophone)
        actions.insert(new_word)

    def homophones_replace_words(words: list[str]) -> list[str]:
        """Replace words with recently chosen homophones"""
        for i, word in enumerate(words):
            if word in homophones_last_used:
                used = homophones_last_used[word]
                # Reuse homophones used the last 30 minutes
                if time.monotonic() - used["time"] < 30 * 60:
                    used["time"] = time.monotonic()
                    words[i] = used["word"]
        return words


def get_next(word: str, homophones: list[str]):
    index = (homophones.index(word.lower().strip()) + 1) % len(homophones)
    return homophones[index]


def get_list(word: str):
    word_lower = word.lower().strip()
    if word_lower not in all_homophones:
        msg = f"Found no homophones for: {word.strip()}"
        actions.user.notify(msg)
        raise ValueError(msg)
    homophones = all_homophones[word_lower]
    # This is a word that can be used as a homophone source but not destination/result
    if word_lower not in homophones:
        homophones = [word_lower, *homophones]
    return homophones


def format_homophone(word: str, homophone: str):
    leading_whitespace = re.search(r"^[\s]+", word)
    trailing_whitespace = re.search(r"[\s]+$", word)
    word = word.strip()
    if word.isupper():
        homophone = homophone.upper()
    elif word == word.capitalize():
        homophone = homophone.capitalize()
    if leading_whitespace:
        homophone = leading_whitespace.group() + homophone
    if trailing_whitespace:
        homophone += trailing_whitespace.group()
    return homophone


def homophones_update(values: list[list[str]], headers: list[str]):
    global all_homophones
    homophones = {}
    for row in values:
        # Homophones starting with `$` can't be updated to
        words = sorted([w.lower() for w in row if w[0] != "$"])
        for word in row:
            # Homophones starting with `$` can be a source. ie updated from.
            if word[0] == "$":
                word = word[1:]
            homophones[word.lower()] = words
    all_homophones = homophones


def on_ready():
    actions.user.watch_csv_as_list(
        Path(__file__).parent / "homophones_en.csv",
        homophones_update,
    )


app.register("ready", on_ready)
