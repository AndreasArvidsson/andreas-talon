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
snip command:               user.code_insert_snippet("voiceCommandDeclaration")

# ----- Function call -----
call {user.code_function}:  user.code_call_function(code_function)
