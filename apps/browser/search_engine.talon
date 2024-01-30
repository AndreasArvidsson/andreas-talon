search for <user.text>$:
    user.browser_search(text)

search for (this | dis | is | ness):
    user.browser_search_selected()
search for line:
    edit.select_line()
    user.browser_search_selected()
search for token:
    edit.select_word()
    user.browser_search_selected()

define word <user.word>$:
    user.browser_define(word)
define phrase <user.text>$:
    user.browser_define(text)
define (this | dis):
    user.browser_define_selected()
