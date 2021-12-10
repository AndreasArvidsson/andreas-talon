app: vscode
-

# Actions around take word

pre <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.left()

post <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.right()

take <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)

cut <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.cut()

copy <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.copy()

paste to <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.paste()

(chuck | clear) <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.delete()