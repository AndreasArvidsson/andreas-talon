# Switch to dictation mode and insert a phrase
dictate [<user.prose>]$:    user.dictation_mode(prose or "")

# Switch to swedish dictation
swedish$:                   user.swedish_dictation_mode()

# Switch to mixed mode and insert a phrase
mixed mode [<user.prose>]$: user.mixed_mode(prose or "")

# Switch to demo mode
demo mode$:                 user.demo_mode()

# Switch to sleep mode
{user.sleep_phrase} [<phrase>]$: user.talon_sleep()

# Just guard so you can always try to break out of dictation mode and it won't do anything weird
command mode$:              skip()
