tag: user.java
-
tag(): user.generic_language
tag(): user.operators
tag(): user.comments

# ----- Java additional -----

make arrow function:
    user.insert_snippet("() -> {\n\t$0\n}")

new {user.code_data_type}:
    user.insert_snippet("new {code_data_type}($0);")

new <user.variable_name>:
    format = user.code_get_class_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    user.insert_snippet("new {name}($0);")