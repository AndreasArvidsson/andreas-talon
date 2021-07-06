mode: dictation
-

# Freely dictate text
<user.text_dictation>:               auto_insert(text_dictation)

# Switch to command mode and insert a phrase
(command mode | over) [<phrase>]$:   user.command_mode(phrase or "")

# Insert the actual word "over"
word over:                           auto_insert("over")