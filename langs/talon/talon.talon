tag: user.talon
-
tag(): user.operators
tag(): user.comments

# Generic
make print:
    user.insert_snippet("print($0)")

# Context requirements
require win:     "os: windows\n"
require mac:     "os: mac\n"
require linux:   "os: linux\n"
require title:   "title: "
require app:     "app: "
require tag:     "tag: "

make tag:        "tag(): "
make true:       "1"
make false:      "0"

make key:
    user.insert_snippet("key($0)")