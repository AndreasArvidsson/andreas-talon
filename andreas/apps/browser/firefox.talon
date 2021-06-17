app: firefox
-
tag(): browser

tab search:
    browser.focus_address()
    insert("% ")

tab search <user.words>$:
    browser.focus_address()
    insert("% {text}")
    key(down)