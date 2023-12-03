code.language: xml
code.language: html
code.language: javascriptreact
code.language: typescriptreact
-
tag(): user.code_comments
tag(): user.code_inserts

element {user.code_tag}:
    user.code_insert_element(code_tag)
element <user.text>:
    user.code_insert_element(text)

tag {user.code_tag}:        "<{code_tag}>"
tag <user.text>:            "<{text}>"

closed tag {user.code_tag}: "<{code_tag}/>"
closed tag <user.text>:     "<{text}/>"

close tag | tag close:      user.code_close_tag()

attribute <user.text>:
    text = user.format_text(text, "CAMEL_CASE")
    user.code_insert_attribute(text)
