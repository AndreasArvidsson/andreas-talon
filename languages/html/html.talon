tag: user.html
-
tag(): user.comments

element {user.code_tag}:
    user.insert_snippet("<{code_tag}>\n\t$0\n</{code_tag}>")
element <user.text>:
    user.insert_snippet("<{text}>\n\t$0\n</{text}>")

tag {user.code_tag}:
    "<{code_tag}>"
    user.code_push_tag_name(code_tag)
tag <user.text>:
    "<{text}>"
    user.code_push_tag_name(text)

closed tag {user.code_tag}: "<{code_tag}/>"
closed tag <user.text>:     "<{text}/>"

close tag | tag close:      user.code_close_tag()

attr <user.text>:
    user.insert_snippet(" {text}=$0")

make doctype:               "<!DOCTYPE html>\n"
make blank:                 "&nbsp;"
