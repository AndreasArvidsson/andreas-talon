not mode: sleep
-

^dictation mode$:
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
    mode.disable("user.gdb")
    app.notify("Dictation mode")

^command mode$:
    mode.disable("dictation")
    mode.enable("command")
    app.notify("Command mode")

^demo mode on$:
    mode.enable("user.demo")
    app.notify("Demo mode on")