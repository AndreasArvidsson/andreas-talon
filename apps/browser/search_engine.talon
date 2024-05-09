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

translate <user.text>$:
    user.browser_translate(text)
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
define phrase <user.text>$:
    user.browser_define(text)
define (this | dis | is | ness):
    user.browser_define_selected()
