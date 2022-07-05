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

# Vimium
tab split:                  app.tab_detach()

hunting:
    user.stop_app()
    key(escape ctrl-alt-f)
hunting new:
    user.stop_app()
    key(escape ctrl-alt-F)
hunting open:
    user.stop_app()
    key(escape ctrl-alt-g)

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
copy mark address:
    user.rango_command_without_target("copyCurrentTabMarkdownUrl")

hint bigger:
    user.rango_command_without_target("increaseHintSize")
hint smaller:
    user.rango_command_without_target("decreaseHintSize")
hint {user.rango_hint_styles}:
    user.rango_command_without_target("setHintStyle", user.rango_hint_styles)
hint weight {user.rango_hint_weights}:
    user.rango_command_without_target("setHintWeight", user.rango_hint_weights)

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
