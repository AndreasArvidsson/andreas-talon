mode: user.game
tag: user.game_speech
-

^command mode$:
    mode.disable("user.game")
    mode.enable("command")

^game mode$:                skip()
