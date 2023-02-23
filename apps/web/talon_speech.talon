tag: browser
app: talon_speech
-

settings():
    user.foot_switch_timeout = false

key(left):
    key(space)

key(right):
    key(space)
    sleep(300ms)
    key(down)
