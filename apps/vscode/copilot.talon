app: vscode
-

pilot [jest]:               user.vscode("editor.action.inlineSuggest.trigger")
pilot next:                 user.vscode("editor.action.inlineSuggest.showNext")
pilot last:                 user.vscode("editor.action.inlineSuggest.showPrevious")
pilot yes:                  user.vscode("editor.action.inlineSuggest.commit")
pilot [yes] word:           user.vscode("editor.action.inlineSuggest.acceptNextWord")
pilot undo:                 user.vscode("editor.action.inlineSuggest.undo")
pilot stop:                 user.vscode("editor.action.inlineSuggest.hide")
pilot block last:           user.vscode("workbench.action.chat.previousCodeBlock")
pilot block next:           user.vscode("workbench.action.chat.nextCodeBlock")

pilot chat [<user.prose>]$: user.copilot_chat(prose or "")
pilot make [<user.prose>]$: user.copilot_inline_chat("", prose or "")

pilot {user.copilot_command} <user.cursorless_target> [with <user.prose>]$:
    user.cursorless_command("setSelection", cursorless_target)
    user.copilot_inline_chat(copilot_command, prose or "")
