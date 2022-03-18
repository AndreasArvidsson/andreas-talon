app: firefox
-
tag(): browser
tag(): user.scroll

# Tabs
tab search:
    browser.focus_address()
    "% "
tab search <user.text>$:
    browser.focus_address()
    "% {text}"
    key(down)
tab mute:    key(ctrl-m)

# Bitwarden
(bitwarden | bit warden) show:
    key(ctrl-shift-y)
(bitwarden | bit warden) fill:
    key(ctrl-shift-l)
(bitwarden | bit warden) generate:
    key(ctrl-shift-9)

# Vimium
tab split:   app.tab_detach()

hunt:
    user.stop_app()
    key(escape ctrl-alt-f)
hunt new:
    user.stop_app()
    key(escape ctrl-alt-F)
hunt open:
    user.stop_app()
    key(escape ctrl-alt-g)

# Miscellaneous
copy image:
    mouse_click(1)
    sleep(0.1)
    key(y)
    sleep(0.1)
    user.clipboard_manager_update()
copy video:
    mouse_click(1)
    sleep(0.1)
    key(o:2 enter)
    sleep(0.1)
    user.clipboard_manager_update()
