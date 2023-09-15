app: vscode
-
tag(): user.cursorless_custom_number_small

# Cursorless command without targets
^cursorless use release$:
    user.c_use_release()
^cursorless use develop$:
    user.c_use_develop()
^cursorless record$:
    user.vscode("cursorless.recordTestCase")
^cursorless record highlight$:
    argument = user.as_dict("isDecorationsTest", 1)
    user.vscode("cursorless.recordTestCase", argument)
^cursorless record error$:
    argument = user.as_dict("recordErrors", 1)
    user.vscode("cursorless.recordTestCase", argument)
^cursorless record pause$:
    user.vscode("cursorless.pauseRecording")
^cursorless record resume$:
    user.vscode("cursorless.resumeRecording")

# Git
git open <user.cursorless_target>:
    user.cursorless_command("setSelection", cursorless_target)
    user.git_open_remote_file_url(true, false)
git copy <user.cursorless_target>:
    user.cursorless_command("setSelection", cursorless_target)
    user.git_copy_remote_file_url(true, false)
git copy mark [down] <user.cursorless_target>:
    user.git_copy_markdown_remote_file_url(cursorless_target_list)
git copy mark [down] <user.cursorless_target> [as <user.cursorless_target>]:
    user.git_copy_markdown_remote_file_url(cursorless_target_list)

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

# Text insertion
place ({user.symbol} | <user.text>) <user.cursorless_destination>:
    user.cursorless_insert(cursorless_destination, symbol or text)

snip {user.snippet_insert} <user.cursorless_destination>:
    user.c_insert_snippet(snippet_insert, cursorless_destination)

{user.symbol} wrap <user.cursorless_target>:
    user.c_wrap_with_symbol(cursorless_target, symbol)

{user.snippet_wrap} wrap <user.cursorless_target>:
    user.c_wrap_with_snippet(cursorless_target, snippet_wrap)

# Misc
break line <user.cursorless_target>:
    user.cursorless_command("setSelectionBefore", cursorless_target)
    key("enter")

search for <user.cursorless_target>:
    user.c_browser_open_target(cursorless_target)
