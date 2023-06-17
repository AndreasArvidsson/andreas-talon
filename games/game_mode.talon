mode: user.game
tag: user.game_voip_muted
-

^command mode$:             user.game_mode_disable()

^game mode$:                skip()

{user.sleep_phrase} [<phrase>]$:
    user.talon_sleep()
