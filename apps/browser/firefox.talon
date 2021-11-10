app: firefox
-
tag(): browser
tag(): user.scroll

# Tabs
tab search:
    browser.focus_address()
    insert("% ")
tab search <user.text>$:
    browser.focus_address()
    insert("% {text}")
    key(down)
tab mute:             key(ctrl-m)

# Bitwarden
bitwarden show:       key(ctrl-shift-y)
bitwarden fill:       key(ctrl-shift-l)
bitwarden generate:   key(ctrl-shift-9)


# Vimium

tab back:             key(escape ctrl-alt-N)
tab split:            key(escape ctrl-alt-M)

hunt:
    user.stop_app()
    key(escape ctrl-alt-f)
hunt new:
    user.stop_app()
    key(escape ctrl-alt-F)
hunt open:
    user.stop_app()
    key(escape ctrl-alt-g)