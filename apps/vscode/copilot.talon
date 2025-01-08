app: vscode
-

pilot [jest]:               user.run_rpc_command("editor.action.inlineSuggest.trigger")
pilot next:                 user.run_rpc_command("editor.action.inlineSuggest.showNext")
pilot last:                 user.run_rpc_command("editor.action.inlineSuggest.showPrevious")
pilot yes:                  user.run_rpc_command("editor.action.inlineSuggest.commit")
pilot [yes] word:           user.run_rpc_command("editor.action.inlineSuggest.acceptNextWord")
pilot undo:                 user.run_rpc_command("editor.action.inlineSuggest.undo")
pilot stop:                 user.run_rpc_command("editor.action.inlineSuggest.hide")
pilot block last:           user.run_rpc_command("workbench.action.chat.previousCodeBlock")
pilot block next:           user.run_rpc_command("workbench.action.chat.nextCodeBlock")

pilot chat [<user.prose>]$: user.copilot_chat(prose or "")
pilot make [<user.prose>]$: user.copilot_inline_chat("", prose or "")

pilot {user.copilot_command} <user.cursorless_target> [with <user.prose>]$:
    user.cursorless_command("setSelection", cursorless_target)
    user.copilot_inline_chat(copilot_command, prose or "")
