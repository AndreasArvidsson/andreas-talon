tag: user.code_comments
-

comment:
    code.toggle_comment()

snip comment <user.text>$:
    user.code_comment_insert(text)

snip block comment <user.text>$:
    user.code_comment_insert_block(text)

snip dock (comment | string) <user.text>:
    user.code_comment_insert_docstring(text)
