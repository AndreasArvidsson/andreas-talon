mode: user.talon
mode: user.auto_lang
and code.language: talon
-

# Assignment operator
op (equals | assign):   " = "

# Boolean operators
op or:                  " or "

# Context requirements
require win:            "os: windows\n"
require mac:            "os: mac\n"
require linux:          "os: linux\n"
require title:          "title: "
require app:            "app: "
require tag:            "tag: "

state and:              "and "
state tag:              "tag(): "
state new line:         "\\n"
state comment:          "# "

state key:
	"key()"
	key(left)


# Show immediately without need for additional character after
caret:                  "^ "
dollar:                 "$"
pipe:                   "|"