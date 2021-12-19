tag: user.java
-
tag(): user.generic_language
tag(): user.c_common
tag(): user.operators
tag(): user.comments

# ----- Java additional -----

new {user.code_data_type}:
    user.insert_snippet("new {code_data_type}($0);")

new <user.text>:
    format = user.code_get_class_format()
    name = user.format_text(text, format)
    user.insert_snippet("new {name}($0);")