from talon import Context, Module, app, clip, cron, imgui, actions, ui, fs
from talon import fs
import os

# ########################################################################
# # global settings
# ########################################################################

# a list of alternatives where each line is a comma separated list
# e.g. where,wear,ware
# a suitable one can be found here:
# https://github.com/pimentel/homophones

ctx = Context()
mod = Module()
mod.mode("alternatives")

cwd = os.path.dirname(os.path.realpath(__file__))
alternatives_file = os.path.join(cwd, "alternatives.csv")

def read_file(name, flags):
    if name != alternatives_file:
        return

    phones = {}
    canonical_list = []
    with open(alternatives_file, "r") as f:
        for line in f:
            words = line.rstrip().split(",")
            canonical_list.append(words[0])
            for word in words:
                word = word.lower()
                old_words = phones.get(word, [])
                phones[word] = sorted(set(old_words + words))

    global all_alternatives
    all_alternatives = phones

read_file(alternatives_file, None)
fs.watch(cwd, read_file)

main_screen = ui.main_screen()

@imgui.open(x=0, y=main_screen.y)
def gui(gui: imgui.GUI):
    gui.text("Alternatives")
    gui.line()
    index = 1
    global active_word_list
    for word in active_word_list:
        gui.text("Alt {}: {} ".format(index, word))
        index = index + 1
    gui.line()
    if gui.button("Hide"):
        actions.user.alternatives_hide()

def update_alternatives(word, last):
    global active_word_list, active_word, is_last, pad_left, pad_right

    pad_left = word.startswith(" ")
    pad_right = word.endswith(" ")
    word = word.strip()
    active_word = word
    is_capitalized = word == word.capitalize()
    is_upper = word.isupper()
    word = word.lower()

    if word not in all_alternatives:
        if gui.showing:
            actions.user.alternatives_hide()
        return False

    is_last = last
    active_word_list = all_alternatives[word]

    if active_word_list[0].lower() != word:
        active_word_list = active_word_list[:]
        active_word_list.remove(word)
        active_word_list.insert(0, word)

    if is_capitalized or is_upper:
        active_word_list = active_word_list[:]
        for i in range(len(active_word_list)):
            if is_capitalized:
                active_word_list[i] = active_word_list[i].capitalize()
            elif is_upper:
                active_word_list[i] = active_word_list[i].upper()

    actions.mode.enable("user.alternatives")
    gui.show()
    return True

@mod.action_class
class Actions:
    def alternatives_selected(word: str):
        """Show alternatives if the given word is a homophone"""
        found = update_alternatives(word, False)
        if not found:
            app.notify("Found no alternatives for:\n{}".format(word))

    def alternatives_last(word: str or None):
        """Show alternatives if the last historical word is a homophone"""
        if not word:
            word = actions.user.history_get_last_phrase()
        update_alternatives(word, True)

    def alternatives_hide():
        """Hides the alternatives display"""
        actions.mode.disable("user.alternatives")
        gui.hide()

    def alternatives_select(number: int, formatter: str) -> str:
        """selects the alternative by number"""
        global active_word, pad_left, pad_right

        if number < 1 or number > len(active_word_list):
            error = "Alternatives index {} is out of range (1-{})".format(
                number, len(active_word_list)
            )
            app.notify(error)
            return

        word = active_word_list[number - 1]

        if formatter != "None":
            word = actions.user.formatted_text(word, formatter)

        if active_word == word:
            actions.user.alternatives_hide()
            return

        if pad_left:
            word = " " + word

        if pad_right:
            word = word + " "

        global is_last
        # Last word written
        if is_last:
            # Select last word
            for _ in active_word:
                actions.edit.extend_left()
            # Last word in history. Replace it.
            if active_word == actions.user.history_get_last_phrase():
                actions.user.history_replace_last_phrase(word)
            # Last word not in history. Just add it.
            else:
                actions.user.history_add_phrase(word)
        # Selected text. Not last
        else:
            actions.user.history_add_phrase(word)

        actions.insert(word)
        actions.user.alternatives_hide()
