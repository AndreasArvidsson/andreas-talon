# Switch to dictation mode and insert a phrase
dictate [<phrase>]$:   user.dictation_mode(phrase or "")

# Switch to swedish dictation mode and insert a phrase
swedish [<phrase>]$:   user.swedish_mode(phrase or "")

# Just guard so you can always try to break out of dictation mode and it won't do anything weird
command mode:          skip()