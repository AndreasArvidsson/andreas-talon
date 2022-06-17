tag: user.comments
-

comment:              code.toggle_comment()
make comment:         user.comments_insert()

make comment <user.text>$:
    text = user.format_text(text, "CAPITALIZE_FIRST_WORD")
    user.comments_insert(text)

make block comment:   user.comments_insert_block()

make block comment <user.text>$:
    text = user.format_text(text, "CAPITALIZE_FIRST_WORD")
    user.comments_insert_block(text)

make dock string:     user.comments_insert_docstring()