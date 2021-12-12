tag: user.html
-
tag(): user.comments

block tag {user.code_tag}:
    user.insert_snippet("<{code_tag}>\n\t$0\n</{code_tag}>")
block tag <user.variable_name>:
    user.insert_snippet("<{variable_name}>\n\t$0\n</{variable_name}>")

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
    user.insert_snippet(" {text}=$0")

make doctype:                     "<!DOCTYPE html>\n"
make blank:                       "&nbsp;"