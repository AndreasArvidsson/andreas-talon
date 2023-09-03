tag: user.code_comments
-

comment:
    code.toggle_comment()

snip comment <user.text>$:
    user.comment_insert(text)

snip block comment <user.text>$:
    user.comment_insert_block(text)

snip dock comment <user.text>:
    user.comment_insert_docstring(text)
