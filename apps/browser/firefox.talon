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

rango explicit:
    user.rango_disable_direct_clicking()
rango direct:
    user.rango_enable_direct_clicking()

copy address:
    user.rango_command_without_target("copyLocationProperty", "href")

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
