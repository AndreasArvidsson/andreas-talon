code.language: cpp
-

new {user.code_data_type}:
    user.code_new_instance(code_data_type)

new <user.prose>:
    format = user.code_get_class_format()
    name = user.format_text(prose, format)
    user.code_new_instance(name)
