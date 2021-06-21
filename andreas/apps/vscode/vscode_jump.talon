# hunt <user.text_symbol>:   user.vscode("andreas.jumpSearch", text_symbol)
# hunt word <word>:          user.vscode("andreas.jumpSearch", word)
# hunt clear:                user.vscode("andreas.jumpCancel")
# {user.vscode_actions} <user.letters>:
# 	user.vscode("andreas.jumpAction", vscode_actions, letters)
# replace <user.letters> with <word>:
# 	user.vscode("andreas.jumpAction", "replace", letters, word)
# insert <word> at <user.letters>:
# 	user.vscode("andreas.jumpAction", "insert", letters, word)