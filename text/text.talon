# Formatted code phrase: "camel hello there" -> helloThere
<user.formatters_code> <user.text>:
    user.insert_and_format(text, formatters_code)
<user.formatters_code> <user.text> over:
    user.insert_and_format(text, formatters_code)

# Formatted prose phrase: "sentence hello there" -> Hello there
{user.formatter_prose} <user.text>$:
    user.insert_and_format(text, formatter_prose)
{user.formatter_prose} <user.text> over:
    user.insert_and_format(text, formatter_prose)

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
{user.formatter_word} <user.word>:
    user.insert_and_format(word, formatter_word)
# Single homophone word
{user.formatter_word} <user.ordinals_small> <user.word>:
    homophone = user.homophones_get_by_number(word, ordinals_small)
    user.insert_and_format(homophone, formatter_word)

# Upper case characters
ship <user.letters> [over]:
    user.insert_and_format(letters, "ALL_CAPS")

# Select last
take last:    user.history_select_last_phrase()

# Delete last
chuck last:   user.history_clear_last_phrase()