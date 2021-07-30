from talon import Context, Module, app, clip, cron, imgui, actions, ui, fs
from talon import fs
import os

# a list of homophones where each line is a comma separated list
# e.g. where,wear,ware
# a suitable one can be found here:
# https://github.com/pimentel/homophones

ctx = Context()
mod = Module()
mod.mode("homophones")

cwd = os.path.dirname(os.path.realpath(__file__))
homophones_file = os.path.join(cwd, "homophones.csv")


def read_file(name, flags):
    if name != homophones_file:
        return

    phones = {}
    canonical_list = []
    with open(homophones_file, "r") as f:
        for line in f:
            words = line.rstrip().split(",")
            canonical_list.append(words[0])
            for word in words:
                word = word.lower()
                old_words = phones.get(word, [])
                phones[word] = sorted(set(old_words + words))

    global all_homophones
    all_homophones = phones


read_file(homophones_file, None)
fs.watch(cwd, read_file)

main_screen = ui.main_screen()


@imgui.open(x=0, y=main_screen.y)
def gui(gui: imgui.GUI):
    gui.text("Homophones")
    gui.line()
    index = 1
    global active_word_list
    for word in active_word_list:
        gui.text("Choose {}: {} ".format(index, word))
        index = index + 1
    gui.line()
    if gui.button("Hide"):
        actions.user.homophones_hide()


def get_homophones(word):
    is_upper = word.isupper()
    is_capitalized = word == word.capitalize()
    word = word.lower()

    if word not in all_homophones:
        return None

    homophones = all_homophones[word]

    if is_upper or is_capitalized:
        homophones = homophones[:]
        for i in range(len(homophones)):
            if is_upper:
                homophones[i] = homophones[i].upper()
            elif is_capitalized:
                homophones[i] = homophones[i].capitalize()

    return homophones


def update_homophones(word, last):
    global active_word_list, active_word, is_last, pad_left, pad_right
    pad_left = word.startswith(" ")
    pad_right = word.endswith(" ")
    word = word.strip()
    active_word = word
    active_word_list = get_homophones(word)

    if not active_word_list:
        if gui.showing:
            actions.user.homophones_hide()
        return False

    is_last = last
    actions.mode.enable("user.homophones")
    gui.show()
    return True


@mod.action_class
class Actions:
    def homophones_get(word: str) -> [str] or None:
        """Get homophones for the given word"""
        word = word.lower()
        if word in all_homophones:
            return all_homophones[word]
        return None

    def homophones_selected():
        """Show homophones if the given word is a homophone"""
        word = actions.edit.selected_text()
        if not word:
            return
        found = update_homophones(word, False)
        if not found:
            app.notify("Found no homophones for:\n{}".format(word))

    def homophones_last(word: str or None):
        """Show homophones if the last historical word is a homophone"""
        if not word:
            word = actions.user.history_get_last_phrase()
        update_homophones(word, True)

    def homophones_hide():
        """Hides the homophones display"""
        actions.mode.disable("user.homophones")
        gui.hide()

    def homophones_select(number: int, formatter: str) -> str:
        """selects the alternative by number"""
        global active_word, pad_left, pad_right

        if number < 1 or number > len(active_word_list):
            error = "homophones index {} is out of range (1-{})".format(
                number, len(active_word_list)
            )
            app.notify(error)
            return

        word = active_word_list[number - 1]

        if formatter != "None":
            word = actions.user.format_text(word, formatter)

        if active_word == word:
            actions.user.homophones_hide()
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
        actions.user.homophones_hide()
