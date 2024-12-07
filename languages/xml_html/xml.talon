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
    name = user.format_text(phrase, "CAMEL_CASE")
    user.code_insert_element(name)

tag {user.code_tag}:
    insert("<{code_tag}>")
tag <user.phrase>:
    name = user.format_text(phrase, "CAMEL_CASE")
    insert("<{name}>")

closed tag {user.code_tag}:
    insert("<{code_tag}/>")
closed tag <user.phrase>:
    name = user.format_text(phrase, "CAMEL_CASE")
    insert("<{name}/>")

close tag | tag close:      user.code_close_tag()

attribute <user.phrase>:
    name = user.format_text(phrase, "CAMEL_CASE")
    user.code_insert_attribute(name)
