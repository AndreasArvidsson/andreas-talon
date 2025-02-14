app: vscode
-
# tag(): user.cursorless_use_community_snippets
# tag(): user.private_cursorless_literal_mark_no_prefix

# Cursorless command without targets
^cursorless use release$:
    user.c_use_release()
^cursorless use develop$:
    user.c_use_develop()
^cursorless record$:
    user.run_rpc_command("cursorless.recordTestCase")
^cursorless record highlight$:
    argument = user.as_dict("isDecorationsTest", 1)
    user.run_rpc_command("cursorless.recordTestCase", argument)
^cursorless record error$:
    argument = user.as_dict("recordErrors", 1)
    user.run_rpc_command("cursorless.recordTestCase", argument)
^cursorless record pause$:
    user.run_rpc_command("cursorless.pauseRecording")
^cursorless record resume$:
    user.run_rpc_command("cursorless.resumeRecording")

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
place ({user.symbol} | <user.prose>) <user.cursorless_destination>:
    user.cursorless_insert(cursorless_destination, symbol or prose)

# {user.symbol} wrap <user.cursorless_target>:
#     user.c_wrap_with_symbol(cursorless_target, symbol)

# Format action
<user.formatters> {user.cursorless_reformat_action} <user.cursorless_target>:
    user.cursorless_reformat(cursorless_target, formatters)

# llm
model fix <user.cursorless_target>:
    text = user.cursorless_get_text(cursorless_target)
    fixed_text = user.model_process_text("fix", text)
    destination = user.cursorless_create_destination(cursorless_target)
    user.cursorless_insert(destination, "{fixed_text}")

# Search
scout file for <user.cursorless_target>:
    user.c_search_file(cursorless_target)

search for <user.cursorless_target>:
    user.c_browser_search_target(cursorless_target)
