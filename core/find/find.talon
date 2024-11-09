tag: user.find
-

scout for clip:             edit.find(clip.text())
scout [<user.phrase>]$:     edit.find(phrase or "")

scout all for clip:         user.find_everywhere(clip.text())
scout all [<user.phrase>]$: user.find_everywhere(phrase or "")

replace [<user.phrase>]$:   user.find_replace(phrase or "")
replace all [<user.phrase>]$: user.find_replace_everywhere(phrase or "")

scout case:                 user.find_toggle_match_by_case()
scout word:                 user.find_toggle_match_by_word()
scout expression:           user.find_toggle_match_by_regex()
replace case:               user.find_replace_toggle_preserve_case()

scout last:                 edit.find_previous()
scout (next | mixed):       edit.find_next()

scout hide:
    edit.find("")
    sleep(100ms)
    key(escape)

replace confirm:            user.find_replace_confirm()
replace confirm all:        user.find_replace_confirm_all()

scout file for clip:        user.find_file(clip.text())
scout (file | files | filed) [<user.filename>]$:
    user.find_file(filename or "")

# TODO:
# pop <user.phrase>$:
#     edit.find(phrase)
#     key(enter)

pop (file | files | filed) <user.filename>$:
    user.find_file(filename)
    sleep(300ms)
    key(enter)
