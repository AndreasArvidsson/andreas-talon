tag: user.find
-

find [<user.text>]$:          edit.find(text or "")
find all [<user.text>]$:      user.find_all(text or "")

find dock [<user.text>] [<user.extension>]$:
    text = text or ""
    extension = extension or ""
    user.find_file(text + extension)

find sesh [<user.text>]$:     user.find_recent(text or "")


pop <user.text>$:
    edit.find(text)
    key(enter)

pop dock <user.text> [<user.extension>]$:
    extension = extension or ""
    user.find_file(text + extension)
    sleep(300ms)
    key(enter)

pop sesh <user.text>$:
    user.find_recent(text)
    key(enter)


find (previous | prev):       edit.find_previous()
find next:                    edit.find_next()
find replace [<user.text>]:   user.find_replace(text or "")
replace word:                 user.find_replace_word()
replace all:                  user.find_replace_all()