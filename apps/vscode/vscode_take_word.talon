app: vscode
-

# Actions around take word

take <user.cursorless_target> <user.repeater_phrase_all>:
    user.vscode_take_word(cursorless_target, repeater_phrase_all)

pre <user.cursorless_target> <user.repeater_phrase_all>:
    user.vscode_take_word(cursorless_target, repeater_phrase_all)
    edit.left()

post <user.cursorless_target> <user.repeater_phrase_all>:
    user.vscode_take_word(cursorless_target, repeater_phrase_all)
    edit.right()

cut <user.cursorless_target> <user.repeater_phrase_all>:
    user.vscode_take_word(cursorless_target, repeater_phrase_all)
    edit.cut()

copy <user.cursorless_target> <user.repeater_phrase_all>:
    user.vscode_take_word(cursorless_target, repeater_phrase_all)
    edit.copy()

paste to <user.cursorless_target> <user.repeater_phrase_all>:
    user.vscode_take_word(cursorless_target, repeater_phrase_all)
    edit.paste()

clear <user.cursorless_target> <user.repeater_phrase_all>:
    user.vscode_take_word(cursorless_target, repeater_phrase_all)
    edit.delete()