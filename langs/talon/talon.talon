mode: user.talon
mode: user.auto_lang
and code.language: talon
-
tag(): user.operators


# Context requirements
require win:      "os: windows\n"
require mac:      "os: mac\n"
require linux:    "os: linux\n"
require title:    "title: "
require app:      "app: "
require tag:      "tag: "

state tag:        "tag(): "
state new line:   "\\n"
state comment [<user.text>]:
    text = user.format_text(text or "", "CAPITALIZE_FIRST_WORD")
    "# {text}"

state key:
    "key()"
    key(left)