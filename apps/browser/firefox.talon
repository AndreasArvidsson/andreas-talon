app: firefox
-
tag(): browser
tag(): user.scroll

# Tabs
tab search:
    browser.focus_address()
    insert("% ")
tab search <user.prose>$:
    browser.focus_address()
    insert("% {prose}")
    sleep(100ms)
    key(tab enter)
tab mute:                   key(ctrl-m)

# Bitwarden
(bitwarden | bit warden) show:
    key(ctrl-shift-y)
login fill:
    key(ctrl-shift-l)
password generate:
    key(ctrl-shift-9)

# Rango
{user.rango_with_target_action} <user.rango_target>:
    user.rango_command_with_target(rango_with_target_action, rango_target)
{user.rango_without_target_action}:
    user.rango_command_without_target(rango_without_target_action)

# Miscellaneous
copy image:
    mouse_click(1)
    sleep(100ms)
    key(y)
copy image source:
    mouse_click(1)
    sleep(100ms)
    key(o:2 enter)
copy video:
    mouse_click(1)
    sleep(100ms)
    key(o:2 enter)
