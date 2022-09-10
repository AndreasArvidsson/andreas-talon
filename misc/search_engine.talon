search for <user.text>$:
    user.browser_open(text)

search for (this | dis | is):
    text = edit.selected_text()
    user.browser_open(text)
