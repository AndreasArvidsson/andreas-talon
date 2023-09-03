code.language: java
-
tag(): user.generic_language
tag(): user.c_common
tag(): user.code_operators
tag(): user.comments

# ----- Java additional -----

new {user.code_data_type}:
    user.code_new_instance(code_data_type)

new <user.text>:
    format = user.code_get_class_format()
    name = user.format_text(text, format)
    user.code_new_instance(name)
