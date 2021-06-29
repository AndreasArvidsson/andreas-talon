# Switch to dictation mode and insert a phrase
(dictation mode | prose) [<phrase>]$:   user.dictation_mode(phrase or "")

^demo mode$:
	mode.enable("user.demo")
	app.notify("Demo mode on")