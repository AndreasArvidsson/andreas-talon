code.language: java
-
tag(): user.code_generic_language
tag(): user.code_operators
tag(): user.code_comments

# ----- Java additional -----

new {user.code_data_type}:
    user.code_new_instance(code_data_type)

new <user.phrase>:
    format = user.code_get_class_format()
    name = user.format_text(phrase, format)
    user.code_new_instance(name)
