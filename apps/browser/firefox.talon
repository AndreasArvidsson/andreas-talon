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
hunt:
    user.stop_app()
    key(escape ctrl-alt-f)
hunt new:
    user.stop_app()
    key(escape ctrl-alt-F)
hunt open:
    user.stop_app()
    key(escape ctrl-alt-g)