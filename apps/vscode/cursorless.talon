app: vscode
-

# Cursorless command without targets
^cursorless use release$:
    user.cursorless_use_release()
^cursorless use develop$:
    user.cursorless_use_develop()
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

# Copy / paste
copy <user.cursorless_target>:
    user.cursorless_command("copyToClipboard", cursorless_target)
    user.clipboard_manager_update()
cut <user.cursorless_target>:
    user.cursorless_command("cutToClipboard", cursorless_target)
    user.clipboard_manager_update()
paste <number_small> [and <number_small>]* <user.cursorless_positional_target>:
    user.clipboard_manager_copy(number_small_list)
    user.cursorless_command("pasteFromClipboard", cursorless_positional_target)

# Git
git open <user.cursorless_target>:
    user.cursorless_command("setSelection", cursorless_target)
    user.git_open_remote_file_url(1)
git copy <user.cursorless_target>:
    user.cursorless_command("setSelection", cursorless_target)
    user.git_copy_remote_file_url(1)
git copy mark [down] <user.cursorless_target>:
    user.cursorless_command("setSelection", cursorless_target)
    user.git_copy_markdown_remote_file_url(0)
git copy mark [down] <user.cursorless_primitive_target> [as <user.cursorless_primitive_target>]:
    user.git_copy_markdown_remote_file_url(cursorless_primitive_target_list)

# Actions around take word
take <user.cursorless_target> <user.repeater_phrase_all>:
    user.vscode_take_word(cursorless_target, repeater_phrase_all)
<user.cursorless_target> <user.repeater_phrase_all>:
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

# Misc
break line <user.cursorless_target>:
    user.cursorless_command("setSelectionBefore", cursorless_target)
    key("enter")

{user.key_symbol} wrap <user.cursorless_target>:
    delimiters = user.as_list(key_symbol, key_symbol)
    user.cursorless_single_target_command_with_arg_list("wrapWithPairedDelimiter", cursorless_target, delimiters)
