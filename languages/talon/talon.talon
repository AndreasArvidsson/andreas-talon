tag: user.talon
-
tag(): user.operators
tag(): user.comments

# Context requirements
require win:                "os: windows\n"
require mac:                "os: mac\n"
require linux:              "os: linux\n"
require title:              "title: "
require app:                "app: "
require tag:                "tag: "

# Generic
make tag:                   "tag(): "
make true:                  "true"
make false:                 "false"
make key:                   user.insert_snippet("key($0)")
make print:                 user.insert_snippet("print($0)")
make command:               user.insert_snippet('$0: user.vscode("$CLIPBOARD")')
