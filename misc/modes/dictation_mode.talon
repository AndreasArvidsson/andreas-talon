mode: dictation
experiment: anchor-file
-

# Freely dictate text
<user.prose>:   auto_insert(prose)

new line:
    edit.line_insert_down()
    user.dictation_format_reset()

# Switch to command mode and insert a phrase
(command mode | over) [<phrase>]$:
    user.command_mode(phrase or "")

# Insert the actual words
escape words <user.words>$:
    auto_insert(words)
escape words <user.words> over:
    auto_insert(words)