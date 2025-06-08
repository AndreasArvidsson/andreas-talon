code.language: java
-
tag(): user.code_generic_language
tag(): user.code_operators
tag(): user.code_comments

settings():
    user.code_class_formatter = "PASCAL_CASE"
    user.code_function_formatter = "CAMEL_CASE"
    user.code_variable_formatter = "CAMEL_CASE"

# ----- Java additional -----

new {user.code_data_type}:
    user.code_new_instance(code_data_type)

new <user.prose>:
    format = user.code_get_class_format()
    name = user.format_text(prose, format)
    user.code_new_instance(name)
