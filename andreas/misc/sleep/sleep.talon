# Defines the commands that sleep/wake Talon
mode: command
mode: dictation
-

^talon sleep$: 
    speech.disable()
    user.mouse_sleep()
    app.notify("Sleeping")