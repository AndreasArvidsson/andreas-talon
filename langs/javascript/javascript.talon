tag: user.javascript
-
tag(): user.generic_language
tag(): user.operators
tag(): user.comments

# ----- JavaScript additional -----

convert to arrow:   user.arrowify_line()

make arrow function <user.variable_name>:
    format = user.code_get_function_format()
    name = user.format_text(variable_name, format)
    user.history_add_phrase(name)
    user.insert_snippet("const {name} = ($1) => {{\n$0\n}}")