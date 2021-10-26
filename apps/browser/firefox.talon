app: firefox
-
tag(): browser
tag(): user.scroll

tab search:
    browser.focus_address()
    insert("% ")
tab search <user.words>$:
    browser.focus_address()
    insert("% {words}")
    key(down)
tab mute:    key(ctrl-m)

tab back:    key(escape ctrl-alt-N)
tab split:   key(escape ctrl-alt-M)

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