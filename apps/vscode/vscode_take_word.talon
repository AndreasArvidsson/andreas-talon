app: vscode
-

# Actions around take word

take <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)

pre <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.left()

post <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.right()

cut <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.cut()

copy <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.copy()

paste to <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.paste()

clear <user.cursorless_target> <user.repeater_phrase>:
    user.vscode_take_word(cursorless_target, repeater_phrase)
    edit.delete()