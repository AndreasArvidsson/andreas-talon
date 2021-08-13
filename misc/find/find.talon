tag: user.find
-

find [<user.text>]$:          edit.find(text or "")
find all [<user.text>]$:      user.find_everywhere(text or "")
replace [<user.text>]$:       user.find_replace(text or "")
replace all [<user.text>]$:   user.find_replace_everywhere(text or "")

find case:                    user.find_toggle_match_by_case()
find word:                    user.find_toggle_match_by_word()
find expression:              user.find_toggle_match_by_regex()
replace case:                 user.find_replace_toggle_preserve_case()

find last:                    edit.find_previous()
find next:                    edit.find_next()

replace confirm:              user.find_replace_confirm()
replace confirm all:          user.find_replace_confirm_all()

find dock [<user.text>] [<user.extension>]$:
    text = text or ""
    extension = extension or ""
    user.find_file(text + extension)

pop <user.text>$:
    edit.find(text)
    key(enter)

pop dock <user.text> [<user.extension>]$:
    extension = extension or ""
    user.find_file(text + extension)
    sleep(300ms)
    key(enter)