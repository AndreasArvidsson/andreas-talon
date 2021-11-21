mode: command
and mode: user.python

mode: command
and mode: user.auto_lang
and code.language: python
-
tag(): user.generic_language
tag(): user.comments

# ----- Python additional -----

(op | is) in:   " in "

format string:
    'f""'
    key(left)