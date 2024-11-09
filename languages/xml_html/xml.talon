code.language: xml
code.language: html
code.language: javascriptreact
code.language: typescriptreact
-
tag(): user.code_comments
tag(): user.code_inserts

element {user.code_tag}:
    user.code_insert_element(code_tag)
element <user.phrase>:
    user.code_insert_element(phrase)

tag {user.code_tag}:        "<{code_tag}>"
tag <user.phrase>:          "<{phrase}>"

closed tag {user.code_tag}: "<{code_tag}/>"
closed tag <user.phrase>:   "<{phrase}/>"

close tag | tag close:      user.code_close_tag()

attribute <user.phrase>:
    text = user.format_text(phrase, "CAMEL_CASE")
    user.code_insert_attribute(text)
