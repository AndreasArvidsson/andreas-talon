mode: dictation
-

# Everything here should call auto_insert to preserve the state to correctly auto-capitalize/auto-space.
<user.text_dictation>:              auto_insert(text_dictation)

cap <user.word>:
	result = user.formatted_text(word, "CAPITALIZE_FIRST_WORD")
	auto_insert(result)

# Escape, type things that would otherwise be commands/symbols
^escape <user.words>$:              auto_insert(user.words)

# Phoneticly spell word with alphabet letters
#spell {user.key_alphabet}+$:       user.insert_characters(key_alphabet_list)

# Reformat
^format it as <user.formatters>$:   user.formatters_reformat_selection(formatters)

# Select last
^select last$:                      user.history_select_last_phrase()