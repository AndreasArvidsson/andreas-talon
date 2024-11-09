search for <user.phrase>$:
    user.browser_search(phrase)
search for (this | dis | is | ness):
    user.browser_search_selected()
search for line:
    edit.select_line()
    user.browser_search_selected()
search for token:
    edit.select_word()
    user.browser_search_selected()

translate <user.phrase>$:
    user.browser_translate(phrase)
translate (this | dis | is | ness):
    user.browser_translate_selected()
translate line:
    edit.select_line()
    user.browser_translate_selected()
translate token:
    edit.select_word()
    user.browser_translate_selected()

define word <user.word>$:
    user.browser_define(word)
define phrase <user.phrase>$:
    user.browser_define(phrase)
define (this | dis | is | ness):
    user.browser_define_selected()
