# Text: formatters + words, punctuation, numbers
<user.format_text>$:              user.insert_string(format_text)
<user.format_text> over:          user.insert_string(format_text)

# Only words, no symbols or numbers
escape words <user.words>$:       user.insert_string(words)
escape words <user.words> over:   user.insert_string(words)

# Single word
word <user.word>:                 user.insert_string(word)
cap word <user.word>:             user.insert_formatted(word, "CAPITALIZE_FIRST_WORD")

# Select last
select last:                      user.history_select_last_phrase()

# Delete last
chuck last:                       user.history_clear_last_phrase()

# Show alternatives for selected
phones this:                      user.homophones_selected()

phones word:
    edit.select_word()
    user.homophones_selected()