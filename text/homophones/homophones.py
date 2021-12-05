from talon import Context, Module, app, imgui, actions, ui, fs
from talon import fs
import os
import re

# a list of homophones where each line is a comma separated list
# e.g. where,wear,ware
# a suitable one can be found here:
# https://github.com/pimentel/homophones

ctx = Context()
mod = Module()
mod.mode("homophones")

cwd = os.path.dirname(os.path.realpath(__file__))
homophones_file = os.path.join(cwd, "homophones.csv")
main_screen = ui.main_screen()


@imgui.open(x=main_screen.x, y=main_screen.y)
def gui(gui: imgui.GUI):
    gui.text("Homophones")
    gui.line()
    index = 1
    global active_word_list
    for word in active_word_list:
        gui.text(f"Choose {index} {word.strip()}")
        index = index + 1
    gui.spacer()
    if gui.button("Hide"):
        actions.user.homophones_hide()


@mod.action_class
class Actions:
    def homophones_get(word: str) -> list[str] or None:
        """Get homophones for the given word"""
        word = word.lower().strip()
        if word in all_homophones:
            return all_homophones[word]
        return None

    def homophones_get_by_number(word: str, number: int) -> str:
        """Get homophone for the given word and number"""
        list = get_list(word).copy()
        list.remove(word)
        list.insert(0, word)
        return get_from_list(list, number)

    def homophones_show_selected():
        """Show homophones selection if the selected word is a homophone"""
        global active_word_list, active_word

        word = actions.edit.selected_text()
        if not word:
            return

        list = get_list(word)
        active_word = word
        active_word_list = format_list(word, list)
        actions.mode.enable("user.homophones")
        gui.show()

    def homophones_cycle_selected():
        """Cycle homophones if the selected word is a homophone"""
        word = actions.edit.selected_text()
        if not word:
            return

        homophones = get_list(word)
        index = (homophones.index(word.lower().strip()) + 1) % len(homophones)
        homophone = homophones[index]
        new_word = format_homophone(word, homophone)
        actions.insert(new_word)

    def homophones_hide():
        """Hides the homophones display"""
        actions.mode.disable("user.homophones")
        gui.hide()

    def homophones_select(number: int) -> str:
        """Selects the alternative by number"""
        global active_word, pad_left, pad_right

        word = get_from_list(active_word_list, number)

        if active_word == word:
            actions.user.homophones_hide()
            return

        actions.user.history_add_phrase(word)
        actions.insert(word)
        actions.user.homophones_hide()


def get_list(word: str) -> list[str]:
    word_lower = word.lower().strip()
    if word_lower not in all_homophones:
        msg = f"Found no homophones for: {word.strip()}"
        actions.user.notify(msg)
        raise ValueError(msg)
    return all_homophones[word_lower]


def get_from_list(list: list[str], number: int) -> str:
    if number < 1 or number > len(list):
        msg = f"Homophones #{number} is out of range (1-{len(list)})"
        actions.user.notify(msg)
        raise ValueError(msg)
    return list[number - 1]


def format_list(word: str, list: list[str]) -> list[str]:
    list = list[:]
    for i in range(len(list)):
        list[i] = format_homophone(word, list[i])
    return list


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


def read_file(name, flags):
    global all_homophones
    if name != homophones_file:
        return

    phones = {}
    with open(homophones_file, "r") as f:
        for line in f:
            words = line.rstrip().split(",")
            for word in words:
                word = word.lower()
                old_words = phones.get(word, [])
                phones[word] = sorted(set(old_words + words))

    all_homophones = phones


def on_ready():
    read_file(homophones_file, None)
    fs.watch(cwd, read_file)


app.register("ready", on_ready)
