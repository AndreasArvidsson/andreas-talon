tag: user.javascript
-
tag(): user.generic_language
tag(): user.c_common
tag(): user.operators
tag(): user.comments

# ----- JavaScript additional -----

(op | is) in:               " in "

convert to arrow:           user.js_arrowify_line()

snip arrow funk <user.text>:
    user.js_arrow_function(text)
