app: diablo3
-

settings():
    user.scroll_speed = 2

^diablo mode$:
    mode.disable("command")
    mode.enable("user.diablo3")
