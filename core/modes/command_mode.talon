# Switch to dictation mode
dictate$:                   user.dictation_mode()

# Switch to swedish dictation
swedish$:                   user.swedish_dictation_mode()

# Switch to mixed mode
mixed mode$:                user.mixed_mode()

# Switch to demo mode
demo mode$:                 user.demo_mode()

# Switch to sleep mode
{user.sleep_phrase} [<phrase>]$: user.talon_sleep()

# Just guard so you can always try to break out of dictation mode and it won't do anything weird
command mode$:              skip()
