^force see sharp$:        user.code_set_language_mode("csharp")
^force see plus plus$:    user.code_set_language_mode("cplusplus")
^force java$:             user.code_set_language_mode("java")
^force java script$:      user.code_set_language_mode("javascript")
^force type script$:      user.code_set_language_mode("typescript")
^force markdown$:         user.code_set_language_mode("markdown")
^force python$:           user.code_set_language_mode("python")
^force talon [script]$:   user.code_set_language_mode("talon")
^force html$:             user.code_set_language_mode("html")

^clear language mode$:
    user.code_clear_language_mode()
    user.notify("Cleared language modes")