app: firefox
-
tag(): browser
tag(): user.scroll

tab search:
    browser.focus_address()
    insert("% ")

tab search <user.words>$:
    browser.focus_address()
    insert("% {text}")
    key(down)

# Vimium
hunt:        key(escape ctrl-alt-f)
hunt new:    key(escape ctrl-alt-F)
hunt open:   key(escape ctrl-alt-g)