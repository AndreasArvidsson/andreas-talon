# Formatted text: "camel hello there" -> helloThere
<user.formatters> <user.text_and_immune>$:
    user.insert_and_format(text_and_immune, formatters)
<user.formatters> <user.text_and_immune> over:
    user.insert_and_format(text_and_immune, formatters)

# Reformat
<user.formatters> (this | dis):
    user.reformat_selection(formatters)
<user.formatters> last:
    user.reformat_last(formatters)
<user.formatters> word:
    edit.select_word()
    user.reformat_selection(formatters)

# Only words, no symbols or numbers
escape words <user.words>$:
    user.insert_string(words)
escape words <user.words> over:
    user.insert_string(words)

# Single word
word <user.word>:    user.insert_string(word)
proud <user.word>:   user.insert_and_format(word, "CAPITALIZE_FIRST_WORD")

# Select last
take last:           user.history_select_last_phrase()

# Delete last
chuck last:          user.history_clear_last_phrase()