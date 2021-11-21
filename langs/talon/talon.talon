mode: command
and mode: user.talon

mode: command
and mode: user.auto_lang
and code.language: talon
-
tag(): user.operators
tag(): user.comments

# Context requirements
require win:     "os: windows\n"
require mac:     "os: mac\n"
require linux:   "os: linux\n"
require title:   "title: "
require app:     "app: "
require tag:     "tag: "

make tag:        "tag(): "
make new line:   "\\n"

make key:
    "key()"
    key(left)

make print:
    "print()"
    key(left)