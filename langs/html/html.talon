mode: command
and mode: user.html

mode: command
and mode: user.auto_lang
and code.language: html

mode: command
and tag: user.html
-
tag(): user.comments

block tag {user.code_tag}:
    "<{code_tag}>\n\n</{code_tag}>"
    key(up tab)
block tag <user.variable_name>:
    "<{variable_name}>\n\n</{variable_name}>"
    key(up tab)

tag {user.code_tag}:
    "<{code_tag}>"
    user.code_push_tag_name(code_tag)
tag <user.variable_name>:
    "<{variable_name}>"
    user.code_push_tag_name(variable_name)

closed tag {user.code_tag}:       "<{code_tag}/>"
close tag <user.variable_name>:   "<{variable_name}/>"

close tag:                        user.code_close_tag()

attr <user.text>:
    ' {text}=""'
    key(left)

make doctype:                     "<!DOCTYPE html>\n"
make blank:                       "&nbsp;"