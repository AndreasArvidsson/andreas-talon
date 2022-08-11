^force {user.code_language}$:
    user.code_set_language_mode(code_language)

^clear language mode$:
    user.code_clear_language_mode()
    user.notify("Cleared language modes")
